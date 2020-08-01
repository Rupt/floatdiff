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


/* Portable arithmetic right shift. For constants only. */
#define dulpsar(x, n) ((x) < 0 ? ~(~(x) >> (n)) : (x) >> (n))


double dulp(double x, double y);
double dulpf(float x, float y);

int64_t dulpval(double x);
int32_t dulpvalf(float x);

double dulpdif(int64_t vx, int64_t vy);
double dulpdiff(int32_t vx, int32_t vy);

double dulpbits(double d);


double
dulp(double x, double y)
{
    int64_t vx, vy;
    vx = dulpval(x);
    vy = dulpval(y);
    return dulpdif(vx, vy);
}


double
dulpf(float x, float y)
{
    int32_t vx, vy;
    vx = dulpvalf(x);
    vy = dulpvalf(y);
    return dulpdiff(vx, vy);
}


int64_t
dulpval(double x)
{
    const int64_t mask = ((uint64_t)1 << 63) - 1;
    union {double f64; int64_t i64;} word;
    word.f64 = x;
    return dulpsar(word.i64, 63) ^ (word.i64 & mask);
}


int32_t
dulpvalf(float x)
{
    const int32_t mask = ((uint32_t)1 << 31) - 1;
    union {float f32; int32_t i32;} word;
    word.f32 = x;
    return dulpsar(word.i32, 31) ^ (word.i32 & mask);
}


double
dulpdif(int64_t vx, int64_t vy)
{
    const int64_t shift = 32;
    const int64_t mask = ((int64_t)1 << shift) - 1;
    const double scale = mask + 1;
    int64_t hi, lo;
    hi = dulpsar(vy, shift) - dulpsar(vx, shift);
    lo = (vy & mask) - (vx & mask);
    return scale*hi + lo;
}


double
dulpdiff(int32_t vx, int32_t vy)
{
    return (int64_t)vy - (int64_t)vx;
}


double dulpbits(double d)
{
    return log2(fabs(d) + 1.);
}
