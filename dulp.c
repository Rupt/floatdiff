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
    return -(w.u >> 63) ^ (w.u | (uint64_t)1 << 63);
}


float
dulpdif(uint64_t vx, uint64_t vy)
{
    float lo, hi;
    lo = (int)(vy & 1) - (int)(vx & 1);
    hi = (int64_t)(vy >> 1) - (int64_t)(vx >> 1);
    return lo + hi + hi;
}


float
dulp(double x, double y)
{
    return dulpdif(dulpval(x), dulpval(y));
}


uint32_t
dulpvalf(float x)
{
    union word32 {float f; uint32_t u;} w;
    w.f = x;
    return -(w.u >> 31) ^ (w.u | (uint32_t)1 << 31);
}


float
dulpdiff(uint32_t vx, uint32_t vy)
{
    float lo, hi;
    lo = (int)(vy & 1) - (int)(vx & 1);
    hi = (int32_t)(vy >> 1) - (int32_t)(vx >> 1);
    return lo + hi + hi;
}


float
dulpf(float x, float y)
{
    return dulpdiff(dulpvalf(x), dulpvalf(y));
}
