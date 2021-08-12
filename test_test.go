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
	checkEq := func(arg, want float64) {
		if got := Bits(arg); got != want {
			t.Errorf("Bits(%g) != %g; got %g", arg, want, got)
		}
	}

	checkLt := func(arg, want float64) {
		if got := Bits(arg); !(got < want) {
			t.Errorf("!(Bits(%g) < %g); got %g", arg, want, got)
		}
	}

	checkGt := func(arg, want float64) {
		if got := Bits(arg); !(got > want) {
			t.Errorf("!(Bits(%g) > %g); got %g", arg, want, got)
		}
	}

	checkEq(0, 0)
	checkEq(1, 1)
	checkEq(7, 3)
	checkEq(0, 0)
	checkEq(Floatdiff(.5, .7), Bits(Floatdiff(.7, .5)))

	checkLt(8, 4)
	checkLt(Floatdiff(math.Inf(-1), math.Inf(+1)), 64)

	checkGt(8, 3)
}

func TestFloatdiff(t *testing.T) {
	checkEq := func(x, y, want float64) {
		if got := Floatdiff(x, y); got != want {
			t.Errorf("Floatdiff(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	zero := float64(0)

	checkEq(1-math.Pow(2, -53), 1, 1)
	checkEq(1.5, 1.5+math.Pow(2, -52), 1)
	checkEq(1.5, math.Nextafter(1.5, 2), 1)
	checkEq(0, 5e-324, 1)
	checkEq(0, math.Nextafter(0, 1), 1)
	checkEq(5e-324, 1e-323, 1)
	checkEq(smallestNormalFloat64-5e-324, smallestNormalFloat64, 1)
	checkEq(-zero, 0, 1)
	checkEq(math.MaxFloat64, math.Inf(+1), 1)

	checkEq(1, 1.5, 1<<51)

	checkSym := func(x, y float64) {
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

	checkSym(.5, .7)

	checkEq(math.NaN(), math.NaN(), 0)

	// shown in readme
	checkEq(1, 1+math.Pow(2, -52), 1)
	checkEq((1+math.Sqrt(5))/2, 1.6180339887, -224707)
}

func TestFloatdiff32(t *testing.T) {
	checkEq := func(x, y float32, want float64) {
		if got := Floatdiff32(x, y); got != want {
			t.Errorf("Floatdiff32(%g, %g) != %g; got %g", x, y, want, got)
		}
	}

	zero := float32(0)

	checkEq(1-float32(math.Pow(2, -24)), 1, 1)
	checkEq(1.5, math.Nextafter32(1.5, 2), 1)
	checkEq(0, math.Nextafter32(0, 2), 1)
	checkEq(1e-45, math.Nextafter32(1e-45, 2), 1)
	checkEq(math.Nextafter32(smallestNormalFloat32, 0), smallestNormalFloat32, 1)
	checkEq(-zero, 0, 1)
	checkEq(math.MaxFloat32, float32(math.Inf(+1)), 1)

	checkEq(1, 1.5, 1<<22)

	checkSym := func(x, y float32) {
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

	checkSym(.5, .7)

	checkEq(float32(math.NaN()), float32(math.NaN()), 0)

	// shown in readme
	checkEq(-zero, 0, 1)
}

func TestRank(t *testing.T) {
	checkLt := func(x, y float64) {
		if rankx, ranky := Rank(x), Rank(y); !(rankx < ranky) {
			t.Errorf("!(Rank(%g) < Rank(%g)); got %d, %d",
				x, y, rankx, ranky)
		}
	}

	checkLt(.5, .7)
	checkLt(-.3, .3)
	checkLt(0, 5e-324)
	checkLt(math.Inf(-1), math.Inf(+1))
}

func TestRank32(t *testing.T) {
	checkLt := func(x, y float32) {
		if rankx, ranky := Rank32(x), Rank32(y); !(rankx < ranky) {
			t.Errorf("!(Rank32(%g) < Rank32(%g)); got %d, %d",
				x, y, rankx, ranky)
		}
	}

	checkLt(.5, .7)
	checkLt(-.3, .3)
	checkLt(0, 1e-45)
	checkLt(float32(math.Inf(-1)), float32(math.Inf(+1)))
}
