#!/usr/bin/python
from struct import *
import timeit
import math
import convolutional_function as cun_fn
import poolig_layer as pool
import fully_connectted as full_conn
import back_propogation as back
import random
def no_layer():
 return 6
def sliding_size_for_weight():
 return 1
def sliding_size_for_pool():
 return 2
def Gaussian(w,x,y,z,d):
 return 1/(4*(math.pi)*(math.pi)*d*d*d*d)*(math.exp(-(w*w+x*x+y*y+z*z)/(2*d*d)))
e=[]
s=[]
i_s=[]
test_i_array=[]
test_l_array=[]
lr=0.5
l=no_layer()
w,w_r,w_c,f,b,d=[],[5,0,5,0,4,0],[5,0,5,0,4,0],[10 for i in range(0,l,1)],[1 for i in range(0,l,1)],1.0
dodw=[]
dcdx=[]
start_time_training=0
start_time_testing=0
end_time_training=0
end_time_testing=0


tr_i_array =[] # Training Image 
tr_l_array=[]  # Training level
dw=[]
# defining image file and level file 

source_folder = "../source_data/"#"/home/my_project/deep_learing/source_data/"
train_image_file =source_folder+"train-images.idx3-ubyte"
train_level_file =source_folder+"train-labels.idx1-ubyte"
#loading image and level file 

tifp = open(train_image_file,"rb")
tlfp = open(train_level_file,"rb")
# seeking magic number
tifp.seek(4,0)
tlfp.seek(4,0)
# load size , row size , colum size of image matix and lebel matrix 

ti_nm = unpack('>I',tifp.read(4))[0] # load size of image file 
ti_nm_row =unpack('>I',tifp.read(4))[0] # load size of row of image 
ti_nm_colum= unpack('>I',tifp.read(4))[0] # load size of colum of image
############################################################################# 
## Loading image in mamory 
print("--------------------Loading image  of the training file into memory----------------------------")

for i in range(0,ti_nm,1):
 tr_i_array.append([])
 for j in range(0,ti_nm_row,1):
  tr_i_array[i].append([])
  for k in range(0,ti_nm_colum,1):
   v=unpack('>B',tifp.read(1))[0]
   tr_i_array[i][j].append(v)

## load training level

tl_nm=unpack('>I',tlfp.read(4))[0] # load the size of lebel 
tl_nm_row=tl_nm # load the size of lebel row
tl_nm_colum=1 # load size of lebel colum
## Loading Lavel of the training image 
print("--------------------Loading level of the training file into memory----------------------------")
for i in range(0,tl_nm,1):
 v=unpack('>B',tlfp.read(1))[0]
 tr_l_array.append(v)
###########################
# initialize weight for  training

print("--------------------Inatialize weight----------------------------")
in_size = [28,24,12,8,4,1]
for i in range(0,l,1):   ##### Layer waish future initialization 
 w.append([])
 for j in range(0,f[i],1): 
  w[i].append([])
  if(w_r[i]!=0):
   for k in range(0,w_r[i],1):
    w[i][j].append([])
    for p in range(0,w_c[i],1):
     w[i][j][k].append(1)
     w[i][j][k][p]=random.randint(0,in_size[i]) * math.sqrt(2.0/in_size[i])#Gaussian(i,j,k,p,d)
###############################
## call convolutional function 
#print((f[0]))
#for i in range(0,l,1):   ##### Layer waish future initialization 
# w.append([])
# for j in range(0,f[i],1): 
 # w[i].append([])
 # for k in range(0,w_n[i],1):
  # w[i][j].append([])
 #  for p in range(0,w_n[i],1):
   # w[i][j][k].append(1)
 #   print(w[i][j][k][p])
print("--------------------start training ----------------------------")
start_time_training=timeit.default_timer() 

ti_nm=1
for k in range(0,ti_nm,1):######ti_nm
 t=[]
 image_size =ti_nm_row
 for i_t in range(f[l-1]):
  if(i_t==tr_l_array[k]):
   t.append(1.0)
  else:
   t.append(0.0)

 #dodw = [[[] for j in range(f[i])] for i in range(l)]
 #dcdx=[[[] for j in range(f[i])] for i in range(l)]
 dodw=[]
 dcdx=[]
 for i in range(0,l,1):
  dodw.append([])
  dcdx.append([])
  if(k==1 and i==0):
   print(dodw[i],i,l,j,k,w_r)
  if(w_r[i]!=0):
   for j in range(0,f[i],1):
    cun_fn.convolutional_fun(w_r[i],w_c[i],sliding_size_for_weight(),image_size,image_size,i,j,tr_i_array[k],w,b)
    dodw[i].append(back.convolutional_fun_input_layer(tr_i_array[k],sliding_size_for_weight(),w_r[i],w_c[i],image_size,image_size))
    dcdx[i].append(back.convolutional_fun_output_layer(tr_i_array[k],image_size,image_size))
   
   image_size=image_size-w_r[i]+1
  else:
   if(i!=5):
    pool.max_poolin(tr_i_array[k],image_size,sliding_size_for_pool())
    image_size=image_size/2
    i_s.append(image_size)
    dodw[i].append([])
    dcdx[i].append([])
   else:
    s=full_conn.fully_connection_by_softmax(f[l-1],tr_i_array[k])#fully_connection_by_svm(f[l-1],tr_i_array[k])
    dodw[i].append([])
    dcdx[i].append([])
  i_s.append(image_size)
  
 
 dw=back.derivation_error_with_rpc_weight(w,w_r,w_c,l,f,t,tr_i_array[k][0],dodw,dcdx,s,i_s,1)
 back.chenge_weight(w,w_r,w_c,l,f,dw,lr)
 #del dodw[:]
 #del dcdx[:]
##############################
## printing the image 
#my_str=''
#for i in range(0,1,1):
# for j in range(0,ti_nm_row,1):
#  for k in range(0,ti_nm_colum,1):
#   my_str= my_str +" "+ str(tr_i_array[i][j][k])
#  print(my_str)
#  my_str=''
# print(tr_l_array[i])
#tr_i_array[0][0][0]
## printing the image leve 
#for i in range(0,tl_nm,1):
# print(tr_l_array[i])
end_time_training=timeit.default_timer() 
print("--------------------Traing is complited----------------------------")
#del tr_i_array[:]
###################### Testing #####################

testing_image_file = source_folder+"t10k-images.idx3-ubyte"
testing_level_file = source_folder+"t10k-labels.idx1-ubyte"
testifp =open(testing_image_file,"rb") # open testing image file ##############
testlfp =open(testing_level_file,"rb") # open testing file level #############
testifp.seek(4,0) ######## Seeking the magiz no ##########
testlfp.seek(4,0) ######## Seeking the magic no ##########

################## For testing #####################################
testifp_nm = unpack('>I',testifp.read(4))[0] # load size of testing  image file
testifp_nm_row = unpack('>I',testifp.read(4))[0] # load size of row testing  image 
testifp_nm_colum = unpack('>I',testifp.read(4))[0] # load size of colum of testing image 
#################### Loading testing image in memory ##############################
print("--------------------Loading image of the testing file into memory----------------------------")
st=[]
for i in range(0,testifp_nm,1):
 test_i_array.append([])
 for j in range(0,testifp_nm_row,1):
  test_i_array[i].append([])
  for k in range(0,testifp_nm_colum,1):
   v=unpack('>B',testifp.read(1))[0]
   test_i_array[i][j].append(v)
############ 
testlfp_nm = unpack('>I',testlfp.read(4))[0] # load size of image file
testlfp_nm_row = testlfp_nm # load size of row image file
testlfp_nm_colum = 1 # load size of colum of image file    
print("--------------------Loading level of the testing file into memory----------------------------")
for i in range(0,testlfp_nm,1):
 v=unpack('>B',testlfp.read(1))[0]
 test_l_array.append(v)
print("--------------------Start testing ----------------------------")

start_time_testing=timeit.default_timer() 
testlfp_nm=1
for k in range(testlfp_nm):
 image_size =testifp_nm_row
 t=[]
 for i_t in range(f[l-1]):
  if(i_t==test_l_array[k]):
   t.append(1.0)
  else:
   t.append(0.0)
 for i in range(0,l,1):
   if(w_r[i]!=0):
    for j in range(0,f[i],1):
     cun_fn.convolutional_fun(w_r[i],w_c[i],sliding_size_for_weight(),testifp_nm_colum,testifp_nm_row,i,j,test_i_array[k],w,b)
     image_size=image_size-w_r[i]+1
 # i_s.append(image_size)  
   else:
    if(i!=5):
     pool.max_poolin(test_i_array[k],image_size,sliding_size_for_pool())
     image_size=image_size/2
    else:
     st.append([])
     st[k]=full_conn.fully_connection_by_softmax(f[l-1],test_i_array[k])#fully_connection_by_svm(f[l-1],test_i_array[k])
 e.append([])
 e[k]=back.error_fun(t,st[k],f[l-1]) #error_svm(t,st[k],f[l-1])
end_time_testing=timeit.default_timer() 
print("--------------------Testing is completed ----------------------------")
#####################################################
#print(e)
#for k in range(0,testlfp_nm,1):
# for m in range(0,f[l-1],1):
#  print("level l = ",test_l_array[k],"for class level ",m,"error =",e[k][m])
  #print(" the out put error is ",e[k][m]," and Softmax s =",st[k][m])

for k in range(0,testlfp_nm,1):
 e_sum=0.0
 for m in range(0,f[l-1],1):
  e_sum=e_sum+e[k][m]
 print " level is ",test_l_array[k]," mach found ",(1-(e_sum/f[l-1]))*100," percentage "
# print "Total error for level l = ",test_l_array[k],"is ",(e_sum/f[l-1])

print "total training time ",(end_time_training-start_time_training)
print "total testing time ",(end_time_testing-start_time_testing)
tifp.close()
tlfp.close()
