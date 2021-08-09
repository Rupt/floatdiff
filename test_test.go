// Tests to look for flaws in Floatdiff functions.
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
		if got := Bits(arg); got != want {
			t.Errorf("Bits(%g) != %g; got %g", arg, want, got)
		}
	}

	check_lt := func(arg, want float64) {
		if got := Bits(arg); !(got < want) {
			t.Errorf("!(Bits(%g) < %g); got %g", arg, want, got)
		}
	}

	check_gt := func(arg, want float64) {
		if got := Bits(arg); !(got > want) {
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
		if got := Floatdiff(x, y); got != want {
			t.Errorf("Floatdiff(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	zero := float64(0)

	check_eq(1-math.Pow(2, -53), 1, 1)
	check_eq(1.5, 1.5+math.Pow(2, -52), 1)
	check_eq(1.5, math.Nextafter(1.5, 2), 1)
	check_eq(0, 5e-324, 1)
	check_eq(0, math.Nextafter(0, 1), 1)
	check_eq(5e-324, 1e-323, 1)
	check_eq(smallestNormalFloat64-5e-324, smallestNormalFloat64, 1)
	check_eq(-zero, 0, 1)
	check_eq(math.MaxFloat64, math.Inf(+1), 1)

	check_eq(1, 1.5, 1<<51)

	check_sym := func(x, y float64) {
		left := Floatdiff(x, y)
		if right := -Floatdiff(y, x); left != right {
			t.Errorf("Floatdiff(%g, %g) != -Floatdiff(%g, %g); got %g, %g",
				x, y, y, x, left, right)
		}

		if right := -Floatdiff(-x, -y); left != right {
			t.Errorf("Floatdiff(%g, %g) != -Floatdiff(%g, %g); got %g, %g",
				x, y, -x, -y, left, right)
		}
	}

	check_sym(.5, .7)

	check_eq(math.NaN(), math.NaN(), 0)

	// shown in readme
	check_eq(1, 1+math.Pow(2, -52), 1)
	check_eq((1+math.Sqrt(5))/2, 1.6180339887, -224707)
}

func TestFloatdiff32(t *testing.T) {
	check_eq := func(x, y float32, want float64) {
		if got := Floatdiff32(x, y); got != want {
			t.Errorf("Floatdiff32(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	zero := float32(0)

	check_eq(1-float32(math.Pow(2, -24)), 1, 1)
	check_eq(1.5, math.Nextafter32(1.5, 2), 1)
	check_eq(0, math.Nextafter32(0, 2), 1)
	check_eq(1e-45, math.Nextafter32(1e-45, 2), 1)
	check_eq(math.Nextafter32(smallestNormalFloat32, 0), smallestNormalFloat32, 1)
	check_eq(-zero, 0, 1)
	check_eq(math.MaxFloat32, float32(math.Inf(+1)), 1)

	check_eq(1, 1.5, 1<<22)

	check_sym := func(x, y float32) {
		left := Floatdiff32(x, y)
		if right := -Floatdiff32(y, x); left != right {
			t.Errorf("Floatdiff32(%g, %g) != -Floatdiff32(%g, %g); got %g, %g",
				x, y, y, x, left, right)
		}

		if right := -Floatdiff32(-x, -y); left != right {
			t.Errorf("Floatdiff32(%g, %g) != -Floatdiff32(%g, %g); got %g, %g",
				x, y, -x, -y, left, right)
		}
	}

	check_sym(.5, .7)

	check_eq(float32(math.NaN()), float32(math.NaN()), 0)

	// shown in readme
	check_eq(-zero, 0, 1)
}

func TestRank(t *testing.T) {
	check_lt := func(x, y float64) {
		if rankx, ranky := Rank(x), Rank(y); !(rankx < ranky) {
			t.Errorf("!(Rank(%g) < Rank(%g)); got %d, %d",
				x, y, rankx, ranky)
		}
	}

	check_lt(.5, .7)
	check_lt(-.3, .3)
	check_lt(0, 5e-324)
	check_lt(math.Inf(-1), math.Inf(+1))
}

func TestRank32(t *testing.T) {
	check_lt := func(x, y float32) {
		if rankx, ranky := Rank32(x), Rank32(y); !(rankx < ranky) {
			t.Errorf("!(Rank32(%g) < Rank32(%g)); got %d, %d",
				x, y, rankx, ranky)
		}
	}

	check_lt(.5, .7)
	check_lt(-.3, .3)
	check_lt(0, 1e-45)
	check_lt(float32(math.Inf(-1)), float32(math.Inf(+1)))
}
