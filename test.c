#include <assert.h>
#include <float.h>
#include <math.h>
#include <stdint.h>
#include "floatdiff.c"


void
test_floatdiff()
{
    /* increment */
    assert(floatdiff(1. - pow(2, -53), 1.) == 1.);
    assert(floatdiff(1.5, 1.5 + pow(2, -52)) == 1.);
    assert(floatdiff(0., 5e-324) == 1.);
    assert(floatdiff(5e-324, 1e-323) == 1.);
    assert(floatdiff(DBL_MIN - 5e-324, DBL_MIN) == 1.);
    assert(floatdiff(-0., 0.) == 1.);
    assert(floatdiff(DBL_MAX, INFINITY) == 1.);

    /* jump */
    assert(floatdiff(1., 1.5) == pow(2, 51));

    /* antisymmetry */
    assert(floatdiff(.5, .7) == -floatdiff(.7, .5));
    assert(floatdiff(.5, .7) == -floatdiff(-.5, -.7));

    /* nan */
    assert(floatdiff(NAN, NAN) == 0.);
}


void
test_rank()
{
    /* order */
    assert(floatdiff_rank(0.5) < floatdiff_rank(0.7));
    assert(floatdiff_rank(-0.3) < floatdiff_rank(0.3));
    assert(floatdiff_rank(0.) < floatdiff_rank(5e-324));
    assert(floatdiff_rank(-INFINITY) < floatdiff_rank(INFINITY));
}


void
test_floatdifff()
{
    /* increment */
    assert(floatdifff(1. - pow(2, -24), 1) == 1);
    assert(floatdifff(1.5, 1.5 + pow(2, -23)) == 1);
    assert(floatdifff(0., 1e-45) == 1.);
    assert(floatdifff(1e-45, 3e-45) == 1.);
    assert(floatdifff(FLT_MIN - 1e-45, FLT_MIN) == 1.);
    assert(floatdifff(-0., 0.) == 1.);
    assert(floatdifff(FLT_MAX, INFINITY) == 1.);

    /* jump */
    assert(floatdifff(1., 1.5) == pow(2, 22));

    /* antisymmetry */
    assert(floatdifff(.5, .7) == -floatdifff(.7, .5));
    assert(floatdifff(.5, .7) == -floatdifff(-.5, -.7));

    /* nan */
    assert(floatdifff(NAN, NAN) == 0.);
}


void
test_rankf()
{
    /* order */
    assert(floatdiff_rankf(0.5) < floatdiff_rankf(0.7));
    assert(floatdiff_rankf(-0.3) < floatdiff_rankf(0.3));
    assert(floatdiff_rankf(0.) < floatdiff_rankf(1e-45));
    assert(floatdiff_rankf(-INFINITY) < floatdiff_rankf(INFINITY));
}


void
test_bits()
{
    /* _bits */
    assert(floatdiff_bits(0.) == 0.);
    assert(floatdiff_bits(1.) == 1.);
    assert(floatdiff_bits(7) == 3.);
    assert(floatdiff_bits(8) < 4.);
    assert(floatdiff_bits(8) > 3.);
    assert(floatdiff_bits(floatdiff(-INFINITY, INFINITY)) < 64.);

    /* absolute */
    assert(floatdiff_bits(floatdiff(.5, .7)) == floatdiff_bits(floatdiff(.7, .5)));
}


void
test_readme()
{
    assert(floatdiff(1., 1. + pow(2, -52)) == 1.);
    assert(floatdiff((1 + sqrt(5))/2, 1.6180339887) == -224707.);
    assert(floatdifff(-0., 0.) == 1.f);
}


int
main()
{
    test_floatdiff();
    test_rank();
    test_floatdifff();
    test_rankf();
    test_bits();
    test_readme();
    return 0;
}
