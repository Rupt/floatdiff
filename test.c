#include <assert.h>
#include <stdint.h>
#include "dulp.c"


#define INFINITY 1./0.
#define NAN 0./0.
#define DBL_MAX 1.7976931348623157e+308
#define DBL_MIN 2.2250738585072014e-308
#define FLT_MAX 3.4028235e+38f
#define FLT_MIN 1.1754944e-38f


/* fun local 2**x for |x| <= 1023 */
double
pow2(int x)
{
    union {double f; uint64_t u;} w;
    w.u = (uint64_t)(x + 1023) << 52;
    return w.f;
}


void
testdulp()
{
    /* increment */
    assert(dulp(1. - pow2(-53), 1.) == 1.);
    assert(dulp(1.5, 1.5 + pow2(-52)) == 1.);
    assert(dulp(0., 5e-324) == 1.);
    assert(dulp(5e-324, 1e-323) == 1.);
    assert(dulp(DBL_MIN - 5e-324, DBL_MIN) == 1.);
    assert(dulp(-0., 0.) == 1.);
    assert(dulp(DBL_MAX, INFINITY) == 1.);
    
    /* jump */
    assert(dulp(1., 1.5) == pow2(51));

    /* antisymmetry */
    assert(dulp(.5, .7) == -dulp(.7, .5));
    assert(dulp(.5, .7) == -dulp(-.5, -.7));

    /* nan */
    assert(dulp(NAN, NAN) == 0.);
}


void
testval()
{
    /* order */
    assert(dulpval(0.5) < dulpval(0.7));
    assert(dulpval(-0.3) < dulpval(0.3));
    assert(dulpval(0.) < dulpval(5e-324));
    assert(dulpval(-INFINITY) < dulpval(INFINITY));
}


void
testdulpf()
{
    /* increment */
    assert(dulpf(1. - pow2(-24), 1) == 1);
    assert(dulpf(1.5, 1.5 + pow2(-23)) == 1);
    assert(dulpf(0., 1e-45) == 1.);
    assert(dulpf(1e-45, 3e-45) == 1.);
    assert(dulpf(FLT_MIN - 1e-45, FLT_MIN) == 1.);
    assert(dulpf(-0., 0.) == 1.);
    assert(dulpf(FLT_MAX, INFINITY) == 1.);
    
    /* jump */
    assert(dulpf(1., 1.5) == pow2(22));

    /* antisymmetry */
    assert(dulpf(.5, .7) == -dulpf(.7, .5));
    assert(dulpf(.5, .7) == -dulpf(-.5, -.7));

    /* nan */
    assert(dulpf(NAN, NAN) == 0.);
}


void
testvalf()
{
    /* order */
    assert(dulpvalf(0.5) < dulpvalf(0.7));
    assert(dulpvalf(-0.3) < dulpvalf(0.3));
    assert(dulpvalf(0.) < dulpvalf(1e-45));
    assert(dulpvalf(-INFINITY) < dulpvalf(INFINITY));
}


int
main()
{
    testval();
    testdulp();
    testvalf();
    testdulpf();
}
