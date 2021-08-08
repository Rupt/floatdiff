// WIP testing of go implementation
// TODO standard tests
// TODO header
package floatdiff

import (
	"math"
	"testing"
)

func TestBits(t *testing.T) {
	// equality checks
	check_eq := [][]float64{
		{0, 0},
		{1, 1},
		{7, 3},
		{Floatdiff(.5, .7), Bits(Floatdiff(.7, .5))},
	}

	for _, pair := range check_eq {
		x, want := pair[0], pair[1]
		got := Bits(x)
		if got != want {
			t.Errorf("Bits(%g) != %g; got %g", x, want, got)
		}
	}

	// inequality checks (down)
	check_lt := [][]float64{
		{8, 4},
		{Floatdiff(math.Inf(-1), math.Inf(+1)), 64},
	}

	for _, pair := range check_lt {
		x, want := pair[0], pair[1]
		got := Bits(x)
		if !(got < want) {
			t.Errorf("!(Bits(%g) < %g); got %g", x, want, got)
		}
	}

	// inequality checks (up)
	check_gt := [][]float64{
		{8, 3},
	}

	for _, pair := range check_gt {
		x, want := pair[0], pair[1]
		got := Bits(x)
		if !(got > want) {
			t.Errorf("!(Bits(%g) > %g); got %g", x, want, got)
		}
	}
}
