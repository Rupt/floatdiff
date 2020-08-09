/* dulp measures order distances between floating point numbers
 * 
 * 
 * TODO explanation
 * 
 * Assumed context:
 * 
 * math.h
 *     fabs, log2
 * 
 * stdint.h
 *     int32_t int64_t uint32_t uint64_t
 * 
 */


double dulp(double x, double y);
double dulpf(float x, float y);

int64_t dulpval(double x);
int32_t dulpvalf(float x);

double dulpdif(int64_t valx, int64_t valy);
double dulpdiff(int32_t valx, int32_t valy);

double dulpbits(double delta);

int64_t dulpsar(int64_t m, uint_fast8_t n);


double
dulp(double x, double y)
{
    int64_t valx = dulpval(x);
    int64_t valy = dulpval(y);
    return dulpdif(valx, valy);
}


double
dulpf(float x, float y)
{
    int32_t valx = dulpvalf(x);
    int32_t valy = dulpvalf(y);
    return dulpdiff(valx, valy);
}


int64_t
dulpval(double x)
{
    const int64_t mask = ((uint64_t)1 << 63) - 1;
    union {double f64; int64_t i64;} word = {x};
    return -(word.i64 < 0) ^ (word.i64 & mask);
}


int32_t
dulpvalf(float x)
{
    const int32_t mask = ((uint32_t)1 << 31) - 1;
    union {float f32; int32_t i32;} word = {x};
    return -(word.i32 < 0) ^ (word.i32 & mask);
}


double
dulpdif(int64_t valx, int64_t valy)
{
    const int64_t shift = 32;
    const int64_t mask = ((int64_t)1 << shift) - 1;
    const double scale = mask + 1;
    int64_t hi = dulpsar(valy, shift) - dulpsar(valx, shift);
    int64_t lo = (valy & mask) - (valx & mask);
    return scale*hi + lo;
}


double
dulpdiff(int32_t valx, int32_t valy)
{
    return (int64_t)valy - valx;
}


double dulpbits(double delta)
{
    return log2(fabs(delta) + 1.);
}


/* Portable arithmetic right shift. */
int64_t
dulpsar(int64_t m, uint_fast8_t n)
{
    const int logical = (((int64_t)-1) >> 1) > 0;
    uint64_t fixu = -(logical & (m < 0));
    int64_t fix = *(int64_t*)&fixu;
    return (m >> n) | (fix ^ (fix >> n));
}
