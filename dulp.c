/* dulp measures order distances between floating point numbers 
 
Assumes a context with stdint.h included
*/


uint64_t
dulpval(double x)
{
    union {double f; uint64_t i;} u = {x};
    return -(u.i >> 63) ^ (u.i | 1llu << 63);
}


double
dulp(double x, double y)
{
    const uint64_t shift = 32;
    const uint64_t mask = (1llu << shift) - 1;
    uint64_t vx, vy;
    long long hi, lo;
    vx = dulpval(x);
    vy = dulpval(y);
    hi = (vy >> shift) - (vx >> shift);
    lo = (vy & mask) - (vx & mask);
    return (double)(mask + 1)*hi + lo;
}


uint32_t
dulpvalf(float x)
{
    union {float f; uint32_t i;} u = {x};
    return -(u.i >> 31) ^ (u.i | 1lu << 31);
}


float
dulpf(float x, float y)
{
    const uint32_t shift = 16;
    const uint32_t mask = (1lu << shift) - 1;
    uint32_t vx, vy;
    int32_t hi, lo;
    vx = dulpvalf(x);
    vy = dulpvalf(y);
    hi = (vy >> shift) - (vx >> shift);
    lo = (vy & mask) - (vx & mask);
    return (float)(mask + 1)*hi + lo;
}
