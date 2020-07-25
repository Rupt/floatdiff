/* dulp measures order distances between floating point numbers

TODO explanation

Assumed context:
stdint.h
    uint64_t int64_t uint32_t int32_t

*/

float dulp(double x, double y);
float dulpf(float x, float y);

uint64_t dulpval(double x);
uint32_t dulpvalf(float x);

float dulpdif(uint64_t vx, uint64_t vy);
float dulpdiff(uint32_t vx, uint32_t vy);


float
dulp(double x, double y)
{
    uint64_t vx, vy;
    vx = dulpval(x);
    vy = dulpval(y);
    return dulpdif(vx, vy);
}


uint64_t
dulpval(double x)
{
    union {double f; uint64_t u;} w;
    w.f = x;
    return -(w.u >> 63) ^ (w.u | (uint64_t)1 << 63);
}


float
dulpdif(uint64_t vx, uint64_t vy)
{
    float lo, hi;
    hi = (int64_t)(vy >> 1) - (int64_t)(vx >> 1);
    lo = (int)(vy & 1) - (int)(vx & 1);
    return hi + hi + lo;
}


float
dulpf(float x, float y)
{
    uint32_t vx, vy;
    vx = dulpvalf(x);
    vy = dulpvalf(y);
    return dulpdiff(vx, vy);
}


uint32_t
dulpvalf(float x)
{
    union {float f; uint32_t u;} w;
    w.f = x;
    return -(w.u >> 31) ^ (w.u | (uint32_t)1 << 31);
}


float
dulpdiff(uint32_t vx, uint32_t vy)
{
    return (int64_t)vy - (int64_t)vx;
}
