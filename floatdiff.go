// Package floatdiff finds differences between floating point numbers.
//
// Measure directed differences between floating point numbers by enumerating
// the discrete spaces between them.
//
// This distance was proposed by an anonymous reviewer to
// "On the definition of ulp(x)" (JM Muller 2005).
//
// Floatdiff(1., 1. + Pow(2, -52)); // 1.
// Floatdiff((1. + Sqrt(5))/2, 1.6180339887); // -224707.
// Floatdiff32(-0., 0.) // 1.
//
// Each float gets an integer valuation Rank(x) which satisfies
//     Rank(0) == 0
// and
//     Rank(Nextafter(x)) == Rank(x) + 1 .
//
// Floats almost have this naturally when reinterpreted as integers, but are
// reversed for negative numbers.
//
// We just reverse negative numbers' order.
//
// The directed distance from x to y equals Rank(y) - Rank(x), in float64
// precision for coverage of small and large distances.
//
// Bits converts the distance to a bits-precision equivalent.
package floatdiff

import (
	"math"
)

// Bits returns a bits-equivalent measure of float diff.
//
// It satisfies
//  Bits(0) == 0
//  Bits(1) == 1
//  Bits(0b111) == 3               (0b111 == 7)
// with interpolation such that
//  3 < bits(0b1000) < 4          (0b1000 == 8)
// and so on.
func Bits(delta float64) float64 {
	return math.Log2(math.Abs(delta) + 1)
}

// Floatdiff returns the directed float64 rank difference from x to y
func Floatdiff(x, y float64) float64 {
	return Diff(Rank(x), Rank(y))
}

// Floatdiff32 returns the directed float32 rank difference from x to y
func Floatdiff32(x, y float32) float64 {
	return Diff32(Rank32(x), Rank32(y))
}

// Rank returns the int64 index of x in the universe of ordered float64.
//
// It satisfies
//  Rank(0) == 0
// and
//  Rank(Nextafter(x)) == Rank(x) + 1
func Rank(x float64) int64 {
	const mask = (1 << 63) - 1
	ibits := int64(math.Float64bits(x))
	return (ibits >> 63) ^ (ibits & mask)
}

// Rank32 returns the int32 index of x in the universe of ordered float32.
//
// It satisfies
//  Rank32(0) == 0
// and
//  Rank32(Nextafter32(x)) == Rank32(x) + 1
func Rank32(x float32) int32 {
	const mask = (1 << 31) - 1
	ibits := int32(math.Float32bits(x))
	return (ibits >> 31) ^ (ibits & mask)
}

// Diff returns the difference of ranks as a float64.
//
// Since the difference of general int64 numbers cannot be represented as int64,
// the return value is rounded to float64.
func Diff(rankx, ranky int64) float64 {
	const shift = 32
	const scale = 1 << 32
	const mask = (1 << 32) - 1
	hi := (ranky >> shift) - (rankx >> shift)
	lo := (ranky & mask) - (rankx & mask)
	return scale*float64(hi) + float64(lo)
}

// Diff32 returns the difference of int32 ranks as a float64.
//
// The return type is chosen for consistency with Diff.
func Diff32(rankx, ranky int32) float64 {
	return float64(int64(ranky) - int64(rankx))
}
