package another

import (
	"testing"
	"time"
)

func TestAnother(t *testing.T) {
	start := time.Now()
	time.Sleep(1 * time.Second)

	if time.Since(start) < 1*time.Second {
		t.Error("1秒経ってない！")
	}
}
