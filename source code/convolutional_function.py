#!/usr/bin/python
from struct import *
import math

####################### This is convolutional function used in CNN #################
###################### in this function x is the input images , w[l][k] is the weight of the lth layer's kth future and b[l][k] ###################### is the baise of lth layer kthe future  
###################### in_s_x,in_s_y is the input starting location ,
###################### in_c_size colum size and in_r_size is the row size  
def convolutional_fun(w_r,w_c,swipt_size,in_c_size,in_r_size,l,k,x,w,b):
 ##################### calculatining convolution function #####################
  sum_f=0
  #print("-----------come convolutional function ---------------")
  for in_s_x in range(0,in_r_size-w_r+1, swipt_size):
   for in_s_y in range(0,in_c_size-w_c+1 , swipt_size): 
    sum_w=0
    for i in range(in_s_x,in_s_x+w_r,1):
     for j in range(in_s_y,in_s_y+w_c,1):
      sum_f = x[i][j]*w[l][k][(i%w_r)][(j%w_c)]
      ##print(i,j)
      sum_w=sum_w+w[l][k][i%w_r][j%w_c]
      ###### Add baise ##############
    if((sum_f!=0)and(sum_w!=0)):
     x[in_s_x][in_s_y] = sum_f/sum_w + b[l]
    else:
     x[in_s_x][in_s_y] =b[l]
      ######### use activation function ReLU ##############
    #x[in_s_x][in_s_y]=max(0,x[in_s_x][in_s_y])
    x[in_s_x][in_s_y]=1/(1+math.exp(-x[in_s_x][in_s_y]))
  #print("-----------return convolutional function ---------------")
   # #print(x[in_s_x][in_s_y])
   # in_s_y =in_s_y+w_c-1
   #in_s_x =in_s_x+w_r-1
