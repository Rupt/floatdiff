// WIP testing of go implementation
// TODO standard tests
// TODO header
package floatdiff

import (
	"math"
	"testing"
)

func TestBits(t *testing.T) {
	check := func(x, want float64) {
		out := Bits(x)
		if out != want {
			t.Errorf("Bits(%g) != %g; got %g", x, want, out)
		}
	}

	check(1-math.Pow(2, -53), 1)
}

func TestFloatdiff(t *testing.T) {
}
