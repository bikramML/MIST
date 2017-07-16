#!/usr/bin/python
from struct import *
import math
## Calculating error ,  we compere targeted value with expected ### value
def error_fun(t,out,cl):
 total=0.0
 print("-----------come to error_fun()---------------")

 e=[]
 #e=[0.5*((t[i]-out[i])*(t[i]-out[i]))for i in range(0,cl,1)]
 #e=[if(out[i]!=0.0): -t[i]*(math.log(out[i]) else:-t[i]) for i in range(0,cl,1)]
 for i in range(0,cl,1):
   e.append(-t[i]*(math.log(out[i])))
 #print(e)
 print("-----------return from error_fun()---------------")
 return e

def error_svm(t,out,cl):
 total=0.0
 print("-----------come to error_svm()---------------")
 e=[]
 for i in range(0,cl,1):
  for j in range(0,cl,1):
   if(i==j):
    continue
  # print(i,j)
   total =total+ max(0,out[j]-t[i]+100)
  e.append(total)
 #print(e)
 print("-----------return from error_svm()---------------")
 return e



def dirivation_error_svm(t,out,cl):
 print("-----------come to dirivation_error()---------------")
 dedout=[]
 total = 0.0
 e=error_svm(t,out,cl)
 for i in range(0,cl,1):
  for j in range(0,cl,1):
   if(i==j):
    continue
   if(e[j]>0):
    dedout.append(-out[i]*e[j])
 print("-----------return from dirivation_error()---------------")
 return dedout 






## Derivation of error with respect to out put
def dirivation_error(t,out,cl):
 print("-----------come to dirivation_error()---------------")
 dedout=[]
 for i in range(0,cl,1):
  dedout.append(t[i]-out[i])
 print("-----------return from dirivation_error()---------------")
 return dedout

## Derivation of softmax with respect to input 
def derivation_softmax(s,x,cl):
 print("-----------come to derivation_softmax(s,x,cl)---------------")
 dsdf=[0.0 for i in range(cl)]
 for i in range(0,cl,1):
   for j in range (0,cl,1):
    if(i==j):
     dsdf[i] =dsdf[i]+ s[i]*(1-s[i])
    else:
     dsdf[i]=dsdf[i]-s[i]*s[j]
 print("-----------return from derivation_softmax(s,x,cl)---------------")
 return dsdf


### Derivation of convolutional function 
def convolutional_fun_output_layer(c,n,m):
 ## out put layer gradient
 print("-----------come to convolutional_fun_output_layer()---------------")
 dcdx=[[c[i][j]*(1-c[i][j]) for j in range(0,m,1)] for i in range(0,n,1)]
 #print(dcdx)
 print("-----------return from convolutional_fun_output_layer()---------------")
 return dcdx 
### Calculate derivation of input net layer with respected to weight 
def convolutional_fun_input_layer(x,icr,w_r,w_c,i_n,i_m):
 print("-----------come to convolutional_fun_input_layer()---------------")
 dodw=[[0.0 for i in range((i_m-w_c+1)/icr)] for j in range((i_m-w_c+1)/icr)]
 
 #print(w,x,icr,w_r,w_c,i_n,i_m)
 for i in range(0,i_n-w_r+1,icr):
  for j in range(0,i_m-w_c+1,icr):
   for k in range(i,i+w_r,1):
    for p in range(j,j+w_c,1):
     dodw[i][j]=dodw[i][j] + x[k][p]
     
 #print(dodw,icr,w_r,w_c,i_n,i_m)
 print("-----------return from convolutional_fun_input_layer()---------------")
 return dodw



#### calculate derivation error with respected to weight function
def derivation_error_with_rpc_weight(w,w_r,w_c,l,f,t,ex,dodw,dcdx,s,i_s,sl):
 print("-----------come to derivation_error_with_rpc_weight()---------------")
 dedout=dirivation_error(t,s,f[l-1]) #dirivation_error_svm(t,s,f[l-1])
 dsdf=derivation_softmax(s,ex,f[l-1])
 
 dw = [[[[0.0 for m in range(w_c[i])] for k in range(w_r[i])]for j in range(f[i])] for i in range(l)]
 
 for i in range(0,l,1):
  dfsum=0.0
  if(i==0): ###fully connected layer        
   for x in range(f[l-i-1]):
    dfsum = dfsum+ dsdf[x]*dedout[x]
   
  else:
   for j in range(0,f[l-i-1],1):
    if(w_r[l-i-1]!=0):
     for k in range(0,w_r[l-i-1],1):
      for p in range(0,w_c[l-i-1],1):    
       if(i==1):
        dw[l-i-1][j][k][p]=dfsum
       else: 
        dwsum=0.0
        for x in range(0,w_r[l-i-1],sl):
         for y in range(0,w_c[l-i-1],sl):
          if(((k-x)<0 or(p-y)<0)and((i_s[l-i-1]-x-k)<0 or(i_s[l-i-1]-y-p)<0)):
           break
          else:
           
           if(w_r[l-i-1+1]==0):       #################### Pooling Layer ####################
            dwsum=dwsum+ dw[l-i-2+1][j][(k-x)/2][(p-y)/2]
            x=x+1
            y=y+1
           else:
            dwsum=dwsum+ dw[l-i-1+1][j][k-x][p-y]
        #print(w_r[l-i-1],dodw[l-i-1][j],l,i,j,k,p)
        dw[l-i-1][j][k][p]=dodw[l-i-1][j][k][p]*dcdx[l-i-1][j][k][p]*dwsum
 print("-----------return from derivation_error_with_rpc_weight()---------------")
 #print(dw)
 return dw


## Change the weight 
def chenge_weight(w,w_r,w_c,l,f,dedw,lr):
 print("-----------come to chenge_weight()---------------")
 for i in range(0,l,1):
  for j in range(0,f[i],1):
   if(w_r[i]!=0):
    for k in range(0,w_r[i],1):
     for p in range(0,w_c[i],1):
      w[i][j][k][p] = w[i][j][k][p]-lr*dedw[i][j][k][p] 
      if(not(dedw[i][j][k][p]==0)):
       print("error ",dedw[i][j][k][p])
 print("-----------return chenge_weight()---------------")





