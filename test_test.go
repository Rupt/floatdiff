// WIP testing of go implementation
// TODO standard tests
// TODO header
package floatdiff

import (
	"testing"
)

func TestBits(t *testing.T) {
	a := Bits(3)
	if a != 2 {
		t.Errorf("Bits(3) == %f; want 2", a)
	}
}

func TestFloatdiff(t *testing.T) {
}
