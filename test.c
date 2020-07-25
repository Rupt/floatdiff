#include <assert.h>
#include <math.h>
#include <float.h>
#include <stdint.h>
#include "dulp.c"

// TODO remove header dependencies
// TODO passert macro (pass warning)
void
testdulp()
{
    /* increment */
    assert(dulp(1., 1. + pow(2., -52.)) == 1.);
    assert(dulp(1.5, 1.5 + pow(2., -52.)) == 1.);
    
    /* jump */
    assert(log2f(dulp(1., 1.5)) == 51.);

    /* antisym */
    assert(dulp(.5, .7) == -dulp(.7, .5));
    assert(dulp(.5, .7) == -dulp(-.5, -.7));

    /* zero */
    assert(dulp(-0., 0.) == 1.);

    /* denormal */
    assert(dulp(0., 5e-324) == 1.);
    assert(dulp(5e-324, 1e-323) == 1.);
    assert(dulp(DBL_MIN - 5e-324, DBL_MIN) == 1.);

    /* nan, infinity */
    assert(dulp(NAN, NAN) == 0.);
    assert(dulp(INFINITY, INFINITY) == 0.);
    assert(dulp(DBL_MAX, INFINITY) == 1.);
}


void
testval()
{
    /* order */
    assert(dulpval(0.5) < dulpval(0.7));
    assert(dulpval(-0.3) < dulpval(0.3));
    assert(dulpval(0.) < dulpval(1e-323));
    assert(dulpval(-INFINITY) < dulpval(INFINITY));
}


void
testdulpf()
{
    /* increment */
    assert(dulpf(1, 1 + powf(2, -23)) == 1);
    assert(dulpf(1.5, 1.5 + powf(2, -23)) == 1);
    
    /* jump */
    assert(log2f(dulpf(1., 1.5)) == 22.);

    /* antisym */
    assert(dulpf(.5, .7) == -dulpf(.7, .5));
    assert(dulpf(.5, .7) == -dulpf(-.5, -.7));

    /* zero */
    assert(dulpf(-0., 0.) == 1.);

    /* denormal */
    assert(dulpf(0., powf(2., -149.)) == 1.);
    assert(dulpf(powf(2., -149.), powf(2., -148.)) == 1.);
    assert(dulpf(FLT_MIN - powf(2., -149.), FLT_MIN) == 1.);

    /* nan, infinity */
    assert(dulpf(NAN, NAN) == 0.);
    assert(dulpf(INFINITY, INFINITY) == 0.);
    assert(dulpf(FLT_MAX, INFINITY) == 1.);
}


void
testvalf()
{
    /* order */
    assert(dulpvalf(0.5) < dulpvalf(0.7));
    assert(dulpvalf(-0.3) < dulpvalf(0.3));
    assert(dulpvalf(0) < dulpvalf(powf(2, -149)));
    assert(dulpvalf(-INFINITY) < dulpvalf(INFINITY));
}

int main() {
    testval();
    testdulp();
    testvalf();
    testdulpf();
}
