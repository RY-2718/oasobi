package parallel

import (
	"testing"
	"time"
)

// func TestOne(t *testing.T) {
// 	start := time.Now()
// 	time.Sleep(1 * time.Second)
//
// 	if time.Since(start) < 1*time.Second {
// 		t.Error("1秒経ってない！")
// 	}
// }

func TestParallel(t *testing.T) {
	cases := []struct {
		name string
		d    time.Duration
	}{
		{name: "one", d: 500 * time.Millisecond},
		{name: "two", d: 1500 * time.Millisecond},
	}

	for _, c := range cases {
		cc := c
		t.Run(cc.name, func(t *testing.T) {
			t.Parallel()

			start := time.Now()
			time.Sleep(cc.d)

			if time.Since(start) < cc.d {
				t.Errorf("%v 経ってない！", cc.d)
			}
		})
	}
}
