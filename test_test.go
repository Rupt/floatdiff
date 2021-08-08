// WIP testing of go implementation
// TODO standard tests
// TODO header
package floatdiff

import (
	"math"
	"testing"
)

const (
	smallestNormalFloat64 = 2.2250738585072014e-308
	smallestNormalFloat32 = 1.1754944e-38
)

func TestBits(t *testing.T) {
	check_eq := func(arg, want float64) {
		got := Bits(arg)
		if got != want {
			t.Errorf("Bits(%g) != %g; got %g", arg, want, got)
		}
	}

	check_lt := func(arg, want float64) {
		got := Bits(arg)
		if !(got < want) {
			t.Errorf("!(Bits(%g) < %g); got %g", arg, want, got)
		}
	}

	check_gt := func(arg, want float64) {
		got := Bits(arg)
		if !(got > want) {
			t.Errorf("!(Bits(%g) > %g); got %g", arg, want, got)
		}
	}

	check_eq(0, 0)
	check_eq(1, 1)
	check_eq(7, 3)
	check_eq(0, 0)
	check_eq(Floatdiff(.5, .7), Bits(Floatdiff(.7, .5)))

	check_lt(8, 4)
	check_lt(Floatdiff(math.Inf(-1), math.Inf(+1)), 64)

	check_gt(8, 3)
}

func TestFloatdiff(t *testing.T) {
	check_eq := func(x, y, want float64) {
		got := Floatdiff(x, y)
		if got != want {
			t.Errorf("Floatdiff(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	zero := 0.0

	check_eq(1-math.Pow(2, -53), 1, 1)
	check_eq(1.5, 1.5+math.Pow(2, -52), 1)
	check_eq(0, 5e-324, 1)
	check_eq(5e-324, 1e-323, 1)
	check_eq(smallestNormalFloat64-5e-324, smallestNormalFloat64, 1)
	check_eq(-zero, 0, 1)
	check_eq(math.MaxFloat64, math.Inf(+1), 1)

	check_eq(1, 1.5, 1<<51)

	check_sym := func(x, y float64) {
		left := Floatdiff(x, y)
		right := -Floatdiff(y, x)
		if left != right {
			t.Errorf("Floatdiff(%g, %g) != -Floatdiff(%g, %g); got %g, %g",
				x, y, y, x, left, right)
		}

		right2 := -Floatdiff(-x, -y)
		if left != right2 {
			t.Errorf("Floatdiff(%g, %g) != -Floatdiff(%g, %g); got %g, %g",
				x, y, -x, -y, left, right2)
		}
	}

	check_sym(.5, .7)

	check_eq(math.NaN(), math.NaN(), 0)
}

func TestFloatdiff32(t *testing.T) {
	check_eq := func(x, y float32, want float64) {
		got := Floatdiff32(x, y)
		if got != want {
			t.Errorf("Floatdiff32(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	check_eq(1-float32(math.Pow(2, -24)), 1, 1)
}

func TestRank(t *testing.T) {
}

func TestRank32(t *testing.T) {
}

func TestDiff(t *testing.T) {
}

func TestDiff32(t *testing.T) {
}
