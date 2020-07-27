/* dulp measures order distances between floating point numbers

TODO explanation

Assumed context:
stdint.h
    int32_t int64_t uint32_t uint64_t

*/

double dulp(double x, double y);
double dulpf(float x, float y);

uint64_t dulpval(double x);
uint32_t dulpvalf(float x);

double dulpdif(uint64_t vx, uint64_t vy);
double dulpdiff(uint32_t vx, uint32_t vy);


double
dulp(double x, double y)
{
    uint64_t vx, vy;
    vx = dulpval(x);
    vy = dulpval(y);
    return dulpdif(vx, vy);
}


double
dulpf(float x, float y)
{
    uint32_t vx, vy;
    vx = dulpvalf(x);
    vy = dulpvalf(y);
    return dulpdiff(vx, vy);
}


uint64_t
dulpval(double x)
{
    union {double f; uint64_t u;} w;
    w.f = x;
    return -(w.u >> 63) ^ (w.u | (uint64_t)1 << 63);
}


uint32_t
dulpvalf(float x)
{
    union {float f; uint32_t u;} w;
    w.f = x;
    return -(w.u >> 31) ^ (w.u | (uint32_t)1 << 31);
}


double
dulpdif(uint64_t vx, uint64_t vy)
{
    const uint64_t shift = 32;
    const uint64_t mask = ((uint64_t)1 << shift) - 1;
    const double scale = mask + 1;
    int64_t hi, lo;
    hi = (vy >> shift) - (vx >> shift);
    lo = (vy & mask) - (vx & mask);
    return scale*hi + lo;
}


double
dulpdiff(uint32_t vx, uint32_t vy)
{
    return (int64_t)vy - (int64_t)vx;
}
