#!/usr/bin/python
from struct import *

### I used max pooling ### 

def max_poolin(x,in_size,slid_size):
   max_v = 0
   #print("-----------come to pooling function ---------------")
   for i in range(0,in_size,slid_size):
    for j in range(0,in_size,slid_size):
     for k in range(i,(slid_size+i),1):
      for n in range(j,(slid_size+j),1):
       max_v=max(max_v,x[k][n])
     x[i/slid_size][j/slid_size]=max_v
   #print("-----------return from pooling function---------------")
