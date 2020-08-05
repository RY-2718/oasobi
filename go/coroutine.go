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

	// Async の開始を通達
	c.Yield <- struct{}{}

	// Done を待つだけだと Async Func が終了した瞬間に Async() がリターンし
	// コルーチンによって処理の中断を制御できなくなる
	// コルーチンによって Async() の次の行の同期的な処理の再開を
	// block の操作（close）によって制御する
	<-c.block
}

// c.block channel に値を入力すると Async のブロックが解除されAsync() が返却される
// coroutine.f の処理は Async() でブロックされているため、 Async() を返却することで処理が再開される
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
		done := make(chan struct{})
		go func() {
			defer close(done)
			c.f(c.ctx)
		}()
		c.done = done
		c.isRunning = true
	} else {
		c.ctx.TerminateAsync()
	}

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
			if !cc.Next() {
				go func() {
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
			log.Printf("c1 start async (take about 0.5 seconds), t = %d, expects t ~ 0", time.Now().Sub(start).Nanoseconds()/1e6)
			time.Sleep(500 * time.Millisecond)
			log.Printf("c1 end async, t = %d, expects t ~ 500", time.Now().Sub(start).Nanoseconds()/1e6)
		})

		log.Printf("c1 mid, t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)

		f := func(ctx *Context) {
			log.Printf("c3 start, t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)

			time.Sleep(150 * time.Millisecond)

			log.Printf("c3 end, t = %d, expects t ~ 750", time.Now().Sub(start).Nanoseconds()/1e6)
		}
		l.AddCoroutine(NewCoroutine(NewContext(), f))

		ctx.Async(func() {
			log.Printf("c1 start async(2) (take about 0.5 seconds), t = %d, expects t ~ 600", time.Now().Sub(start).Nanoseconds()/1e6)
			time.Sleep(500 * time.Millisecond)
			log.Printf("c1 end async(2), t = %d, expects t ~ 700", time.Now().Sub(start).Nanoseconds()/1e6)
		})

		log.Printf("c1 end, t = %d, expects t ~ 750", time.Now().Sub(start).Nanoseconds()/1e6)
	}
	ctx := NewContext()
	l.AddCoroutine(NewCoroutine(ctx, f))

	for i := 1; i < 4; i++ {
		n := i
		f := func(ctx *Context, num int) {
			log.Printf("c2-%d start, t = %d, expects t ~ %d", num, time.Now().Sub(start).Nanoseconds()/1e6, 50*num*(num-1))

			time.Sleep(time.Duration(num) * 100 * time.Millisecond)

			log.Printf("c2-%d end, t = %d, expects t ~ %d", num, time.Now().Sub(start).Nanoseconds()/1e6, 50*num*(num+1))
		}
		ctx := NewContext()
		l.AddCoroutine(NewCoroutine(ctx, func(ctx *Context) {
			f(ctx, n)
		}))
	}

	time.Sleep(1000 * time.Millisecond)
}
