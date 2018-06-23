#include <iostream>
#include <math.h>

int add(int n, float *x, float *y)
{
    for (int i = 0; i < n; i++)
        y[i] = x[i] + y[i];
}

int main(void) 
{
    int N = 1<<20;
    float *x = new float[N];
    float *y = new float[N];

    //init x, y arrs on host
    for (int i = 0; i < N ; i++ )
    {
        x[i] = 1.0f;
        y[i] = 2.0f;
    }

    // Run kernel on 1M elements on GPU 
    add(N,x,y);

    // Free mem 
    delete [] x;
    delete [] y;

    return 0;
}