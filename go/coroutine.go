package main

import (
	"log"
	"time"
)

type Context struct {
	block chan struct{}
	Done  chan struct{}
	Yield chan struct{}
}

func NewContext() *Context {
	return &Context{
		Yield: make(chan struct{}),
	}
}

func (c *Context) Async(f func()) {
	done := make(chan struct{})
	block := make(chan struct{})
	go func() {
		defer close(done)
		f()
	}()
	c.Done = done
	c.block = block

	// Async の開始を通達する
	// coroutine.Next() で受信することでコルーチンの中断を実現
	c.Yield <- struct{}{}

	// Done を待つだけだと Async Func が終了した瞬間に Async() がリターンしてしまうので
	// coroutine.f は勝手に走り出し、コルーチンによって処理の中断を制御できなくなる
	// Async() を終了しないままにしておけば coroutine.f はブロックできるので、 c.block で Async() を終了しないようブロックしておく
	// Context.TerminateAsync() で block を操作（close）することで Async() の終了を制御
	<-c.block
}

// c.block channel に値を入力すると Async() が返却される
// coroutine.f の処理は Async() でブロックされているため、 Async() を返却することで中断していた continue.f が再開される
func (c *Context) TerminateAsync() {
	c.block <- struct{}{}
}

type Coroutine struct {
	ctx       *Context
	f         func(*Context)
	isRunning bool
	done      chan struct{}
}

func NewCoroutine(ctx *Context, f func(ctx *Context)) *Coroutine {
	return &Coroutine{
		ctx:       ctx,
		f:         f,
		isRunning: false,
	}
}

func (c *Coroutine) Next() bool {
	if !c.isRunning {
		// coroutine.f を開始していない場合は開始
		done := make(chan struct{})
		go func() {
			defer close(done)
			c.f(c.ctx)
		}()
		c.done = done
		c.isRunning = true
	} else {
		// coroutine.f が開始されていて終了していない場合、 coroutine.f は Async func のブロックで中断させられている
		// Async func のブロックを解除して Async() を終了させることで coroutine.f の実行を再開
		c.ctx.TerminateAsync()
	}

	// 同期処理の中断は Async()（非同期処理）の開始による yield か関数の終了の2択
	// それぞれを select で待つことで空ループを回避
	select {
	case <-c.ctx.Yield:
		// Async() が呼ばれたときに Yield channel に値が入力される
		// Async() が呼ばれた＝処理は終わってないけど他の coroutine の処理を開始可能
		return false
	case <-c.done:
		// Async() が呼ばれずに関数が終了
		return true
	}
}

func (c *Coroutine) WaitAsyncDone() {
	<-c.ctx.Done
}

type CoroutineLooper struct {
	coroutines chan *Coroutine
}

func NewCoroutineLooper(size int) *CoroutineLooper {
	return &CoroutineLooper{
		coroutines: make(chan *Coroutine, size),
	}
}

func (l *CoroutineLooper) Loop() {
	go func() {
		for c := range l.coroutines {
			cc := c
			// cc.Next == true のとき、 cc.f は終了している
			if !cc.Next() {
				go func() {
					// cc.Next == false のとき、cc.f は Async func を実行している
					// cc.f での Async func の終了を待って l.coroutines（ループの queue）へ cc を追加
					cc.WaitAsyncDone()
					l.AddCoroutine(cc)
				}()
			}
		}
	}()
}

func (l *CoroutineLooper) AddCoroutine(c *Coroutine) {
	l.coroutines <- c
}

func main() {
	start := time.Now()

	l := NewCoroutineLooper(100)
	go l.Loop()

	f := func(ctx *Context) {
		log.Printf("c1 start, t = %d, expects t ~ 0", time.Now().Sub(start).Nanoseconds()/1e6)

		ctx.Async(func() {
			// すぐ実行するはずなので t ~ 0 のはず
			log.Printf("c1 start async (take about 500 msec), t = %d, expects t ~ 0", time.Now().Sub(start).Nanoseconds()/1e6)
			time.Sleep(500 * time.Millisecond)
			// t ~ 0 から 500 msec 待つのだから t ~ 500 のはず
			log.Printf("c1 end async, t = %d, expects t ~ 500", time.Now().Sub(start).Nanoseconds()/1e6)
		})

		// c2-3 の開始が t ~ 300 < 500 なので c2-3 の終了 t ~ 600 まで待つべき
		log.Printf("c1 mid, t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)

		// c-1 の中間地点で coroutine を追加することで、1つの関数の中での2回目の Async の前に coroutine が追加された状況を再現
		f := func(ctx *Context) {
			// coroutine をループに登録する処理のあと、すぐに Async() を実行するため t ~ 600 のはず
			log.Printf("c3 start, t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)

			time.Sleep(150 * time.Millisecond)

			log.Printf("c3 end, t = %d, expects t ~ 750", time.Now().Sub(start).Nanoseconds()/1e6)
		}
		l.AddCoroutine(NewCoroutine(NewContext(), f))

		ctx.Async(func() {
			log.Printf("c1 start async(2) (take about 150 msec), t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)
			time.Sleep(150 * time.Millisecond)
			log.Printf("c1 end async(2), t = %d, expects t ~ 700", time.Now().Sub(start).Nanoseconds()/1e6)
		})

		// Async を待っている間に c3 が実行されるはず
		// Async 実行が終わっても c3 の実行が終わるまでは待つべきなので c3 の終了 t ~ 750 までは待つべき
		log.Printf("c1 end, t = %d, expects t ~ 750", time.Now().Sub(start).Nanoseconds()/1e6)
	}
	ctx := NewContext()
	l.AddCoroutine(NewCoroutine(ctx, f))

	for i := 1; i < 4; i++ {
		n := i
		f := func(ctx *Context, num int) {
			// c2-n の開始時刻の概算は階差数列を用いて求めることができます……
			// 0, 100, 300 となるはず
			// わざわざ c2 の待ち時間を伸ばす必要はありませんでしたね……
			log.Printf("c2-%d start, t = %d, expects t ~ %d", num, time.Now().Sub(start).Nanoseconds()/1e6, 50*num*(num-1))

			time.Sleep(time.Duration(num) * 100 * time.Millisecond)

			// c2-n の開始時刻の概算は階差数列を用いて求めることができます……
			// 100, 300, 600 となるはず
			log.Printf("c2-%d end, t = %d, expects t ~ %d", num, time.Now().Sub(start).Nanoseconds()/1e6, 50*num*(num+1))
		}
		ctx := NewContext()
		l.AddCoroutine(NewCoroutine(ctx, func(ctx *Context) {
			f(ctx, n)
		}))
	}

	time.Sleep(1000 * time.Millisecond)
}
