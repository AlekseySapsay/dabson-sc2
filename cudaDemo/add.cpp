#include <iostream>
#include <math.h>

// le kernel
__global__
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

    // Allocate Unified memory - accessible from CPU or GPU
    cudaMallocManaged(&x, N*sizeof(float));
    cudaMallocManaged(&y, N*sizeof(float));

    //init x, y arrs on host
    for (int i = 0; i < N ; i++ )
    {
        x[i] = 1.0f;
        y[i] = 2.0f;
    }

    // Run kernel on 1M elements on the PU 
    add<<<1, 1>>>(N,x,y);

    // Run kernel on 1M elements on CPU 
    //add(N,x,y);

    // Wait for GPU to finish before accessing on host 
    cudaDeviceSynchronize();

    // Free mem 
    cudaFree(x);
    cudaFree(y);
    // delete [] x;
    // delete [] y;

    return 0;
}