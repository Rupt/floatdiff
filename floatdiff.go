// WIP implementation in go
// TODO comments
// TODO header
package floatdiff

import (
	"math"
)

func Bits(delta float64) float64 {
	return math.Log2(math.Abs(delta) + 1)
}

func Floatdiff(x, y float64) float64 {
	valx := Rank(x)
	valy := Rank(y)
	return Diff(valx, valy)
}

func Rank(x float64) int64 {
	const mask = (1 << 63) - 1
	ibits := int64(math.Float64bits(x))
	return -int64(ibool(ibits < 0)) ^ (ibits & mask)
}

func Rank32(x float32) int32 {
	const mask = (1 << 31) - 1
	ibits := int32(math.Float32bits(x))
	return -int32(ibool(ibits < 0)) ^ (ibits & mask)
}

func Diff(valx, valy int64) float64 {
	const shift = 32
	const scale = 1 << 32
	const mask = (1 << 32) - 1

	hi := (valx >> shift) - (valy >> shift)
	lo := (valy & mask) - (valx & mask)
	return scale*float64(hi) + float64(lo)
}

func Diff32(valx, valy int32) float64 {
	return float64(int64(valy) - int64(valx))
}

func ibool(b bool) (i int) {
	if b {
		i++
	}
	return
}
