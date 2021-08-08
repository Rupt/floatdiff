/*
 * Floating point differences --- dulp
 *
 * dulp`_ measures directed differences between floating point numbers
 * by counting the discrete spaces between them.
 *
 * This distance was proposed by an anonymous reviewer to
 * "On the definition of ulp(x)" (JM Muller 2005).
 *
 *
 * #include <stdint.h>
 * #include "dulp.c"
 *
 * dulp(1., 1. + pow(2, -52)); // 1.
 * dulp((1. + sqrt(5))/2, 1.6180339887); // -224707.
 * dulpf(-0., 0.) // 1.f
 *
 *
 * Each float or double gets an integer valuation val(x) which satisfies
 *     val(0.) == 0
 * and
 *     val(nextafter(x)) == val(x) + 1
 *
 * Floats almost have this naturally when reinterpreted as integers,
 * but are reversed for negative numbers.
 * We just reverse negative numbers' order.
 *
 * The dulp directed distance from x to y equals val(y) - val(x), in
 * double precision for convenience with small and large distances.
 *
 * dulpbits converts the dulp distance to a bits-precision equivalent.
 *
 *
 * Assumes IEEE 764 binary64 and binary32 for doubles and floats.
 *
 * Context:
 *
 * math.h
 *     fabs, log2
 *
 * stdint.h
 *     int64_t, int32_t
 */

static inline double dulpbits(double delta);

static inline double dulp(double x, double y);
static inline double dulpf(float x, float y);

static inline int64_t dulpval(double x);
static inline int32_t dulpvalf(float x);

static inline double dulpdif(int64_t valx, int64_t valy);
static inline double dulpdiff(int32_t valx, int32_t valy);

static inline int64_t dulpsar(int64_t m, char n);


/*
 * Bits-equivalent of dulp distance delta.
 *
 * Specified such that
 *     bits(0) == 0
 *     bits(1) == 1
 *     bits(0b111) == 3               (0b111 == 7)
 * with interpolation such that
 *     3 < bits(0b1000) < 4          (0b1000 == 8)
 * and so on.
 */
static inline double
dulpbits(double delta)
{
    return log2(fabs(delta) + 1.);
}


/*
 * Directed distances for double and float.
 *
 * Returns double since 53 bits of precision are plenty, and the inexact
 * representation allows signed differences between 64 bit integers.
 */
static inline double
dulp(double x, double y)
{
    int64_t valx = dulpval(x);
    int64_t valy = dulpval(y);
    return dulpdif(valx, valy);
}


static inline double
dulpf(float x, float y)
{
    int32_t valx = dulpvalf(x);
    int32_t valy = dulpvalf(y);
    return dulpdiff(valx, valy);
}


/*
 * Integer valuations of double and float.
 *
 * The binary representation naturally has negative numbers in reverse.
 * This bit-twiddle re-reverses the order of negative values, while leaving
 * others unchanged.
 *
 * Equivalent to
 * if (i < 0)
 *     return -((uint) 1 << (bits - 1)) - i - 1;
 * else
 *     return i;
 */
static inline int64_t
dulpval(double x)
{
    const int64_t mask = (1llu << 63) - 1;
    union {double f64; int64_t i64;} word = {x};
    return -(word.i64 < 0) ^ (word.i64 & mask);
}


static inline int32_t
dulpvalf(float x)
{
    const int32_t mask = (1lu << 31) - 1;
    union {float f32; int32_t i32;} word = {x};
    return -(word.i32 < 0) ^ (word.i32 & mask);
}


/*
 * Find the difference of valuations and cast to double.
 *
 * Lacking signed types larger than 64 bits, we split into high and low
 * 32-bit parts and recombine them as doubles.
 */
static inline double
dulpdif(int64_t valx, int64_t valy)
{
    const int shift = 32;
    const int64_t mask = (1llu << shift) - 1;
    const double scale = mask + 1;
    int64_t hi = dulpsar(valy, shift) - dulpsar(valx, shift);
    int64_t lo = (valy & mask) - (valx & mask);
    return scale*hi + lo;
}


static inline double
dulpdiff(int32_t valx, int32_t valy)
{
    return (int64_t) valy - valx;
}


/*
 * Portable arithmetic right shift
 * From github.com/Rupt/c-arithmetic-right-shift
 */
static inline int64_t
dulpsar(int64_t m, char n)
{
    const int logical = (-1llu >> 1) > 0;
    uint64_t fixu = -(logical & (m < 0));
    /* Cast type punning is defined for signed/unsigned pairs */
    int64_t fix = *(int64_t*) &fixu;
    return (m >> n) | (fix ^ (fix >> n));
}
