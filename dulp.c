/* dulp measures order distances between floating point numbers

TODO explanation

Assumed context:
stdint.h
    uint64_t int64_t uint32_t int32_t

*/

uint64_t
dulpval(double x)
{
    union word64 {double f; uint64_t u;} w;
    w.f = x;
    return -(w.u >> 63) ^ (w.u | 1llu << 63);
}


float
dulp(double x, double y)
{
    uint64_t vx, vy;
    float lo, hi;
    vx = dulpval(x);
    vy = dulpval(y);
    lo = (int)(vy & 1) - (int)(vx & 1);
    hi = (int64_t)(vy >> 1) - (int64_t)(vx >> 1);
    return lo + hi + hi;
}


uint32_t
dulpvalf(float x)
{
    union word32 {float f; uint32_t u;} w;
    w.f = x;
    return -(w.u >> 31) ^ (w.u | 1lu << 31);
}


float
dulpf(float x, float y)
{
    uint32_t vx, vy;
    float lo, hi;
    vx = dulpvalf(x);
    vy = dulpvalf(y);
    lo = (int)(vy & 1) - (int)(vx & 1);
    hi = (int32_t)(vy >> 1) - (int32_t)(vx >> 1);
    return lo + hi + hi;
}
