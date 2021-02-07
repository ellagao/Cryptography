# Import libraries
from matplotlib import pyplot as plt
from matplotlib.image import imread
from PIL import Image
import numpy as np
import os
import cv2
import struct
import random

#Read File
fname = 'Source.bmp'
fkey = 'secretkey.txt'
file_image = open( fname, "rb" )
head = file_image.read( 54 ) 
width = struct.unpack( "<i", head[ 18:22 ] )[ 0 ]  
height = struct.unpack( "<i", head[ 22:26 ] )[ 0 ]

#Input Bytes
img = plt.imread( fname )
matrix = np.array( img, dtype='int' )
temp = matrix.flatten( )
temp_int_1_list = list( map( lambda x:int( x ),temp ) )  #np.int to int
if( len( temp_int_1_list ) % 16 != 0 ): 
    exit(0)

#generate Vigenere secretkey
keylen = random.randint( 4,32 )
keylist = [ ]
keylist_bytes = [ ]
for i in range( keylen ):
    byte = random.randint( 0,255 )
    byte2 = byte.to_bytes( 1,byteorder='little' )
    keylist.append( byte )
    keylist_bytes.append( str( byte2 ) )
with open( "Secretkey.txt","w" ) as f:
    f.write( ''.join( keylist_bytes ) )
    f.write( ''.join( str(keylist) ) )

#VigenereEncrypt
def VigenereEncrypt ( code,keylist ): 
    result = [ ]
    for i in range( 0,len( code ) ):
        key = keylist[ i % len( keylist ) ]
        temp = ( code[ i ] + key) % 256
        result.append( temp )
    return( result )

def VigenereDeEncrypt ( code,keylist ): 
    result = [ ]
    for i in range( 0,len( code ) ):
        key = keylist[ i % len( keylist ) ]
        temp = ( code[ i ] +256 - key) % 256
        result.append( temp )
    return( result )

#VigenereEncrypt
temp_int_2_list=VigenereEncrypt(temp_int_1_list,keylist)
temp_int_3_matrix =np.matrix(list( map( lambda x:np.int( x ),temp_int_2_list ) ))
matrix_cipher=temp_int_3_matrix.reshape(height,width)
#Output
image_output_cipher = Image.fromarray( matrix_cipher )
plt.imshow( image_output_cipher,cmap='Greys_r' )
plt.imsave( "CipherPicture.bmp",image_output_cipher,cmap='Greys_r' )
#VigenereDeEncrypt
temp_int_3_list=VigenereDeEncrypt(temp_int_2_list,keylist)
temp_int_4_matrix =np.matrix(list( map( lambda x:np.int8( x ),temp_int_3_list ) ))
matrix_plain=temp_int_4_matrix.reshape(height,width)
#Output
image_output_plain = Image.fromarray( matrix_plain )
plt.imshow( image_output_plain,cmap='Greys_r' )
plt.imsave( "PlainPicture.bmp",image_output_plain,cmap='Greys_r' )
#AES ECB
S=[[0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
   [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
   [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
   [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
   [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
   [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
   [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
   [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
   [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
   [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
   [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
   [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
   [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
   [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
   [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
   [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]]

Inv_S=[[0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb],
       [0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb],
       [0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e],
       [0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25],
       [0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92],
       [0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84],
       [0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06],
       [0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b],
       [0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73],
       [0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e],
       [0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b],
       [0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4],
       [0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f],
       [0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef],
       [0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61],
       [0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d]]

def SubBytes(x):
    row=x//16
    col=x%16
    return(S[row][col])

def Inv_SubBytes(x):
    row=x//16
    col=x%16
    return(Inv_S[row][col])

def XOR(a,b):
    if(len(a)!=len(b)):
        exit(0)
    else:
        c=[]
        for i in range(len(a)):
            c.append(a[i]^b[i])
    return(c)

def T(a,col):
    if(len(a)!=4):
        exit(0)
    Rcon=[[0x01,0x00,0x00,0x00],[0x02,0x00,0x00,0x00],
          [0x04,0x00,0x00,0x00],[0x08,0x00,0x00,0x00],
          [0x10,0x00,0x00,0x00],[0x20,0x00,0x00,0x00],
          [0x40,0x00,0x00,0x00],[0x80,0x00,0x00,0x00],
          [0x1b,0x00,0x00,0x00],[0x36,0x00,0x00,0x00]]
    #Bytes Cycle
    cycle=[a[1],a[2],a[3],a[0]]
    for i in range(len(cycle)):    # Bytes Replacing
        cycle[i]=SubBytes(cycle[i])
    #Rcon XOR
    result=XOR(cycle,Rcon[col//4-1])
    return(result)

def ExtendKey(KeyArray):
    for col in range(4):
        w[col]=KeyArray[col]
    for col in range(4,44):
        if (col%4==0):
            temp=T(w[col-1],col)
            w[col]=XOR(w[col-4],temp)
        else:
            w[col]=XOR(w[col-4],w[col-1])

def LeftLoop4(row,step):
    temp=[]
    for i in range(4):
        temp.append(row[i])       #temp=row
    for i in range(4):
        row[i]=temp[(i+step)%4]

def ShiftRows(pArray):
    row_2, row_3, row_4=[],[],[]
    for i in range(4):
        row_2.append(pArray[i][1]) #row_2=pArray[:,1]
        row_3.append(pArray[i][2]) #row_3=pArray[:,2]
        row_4.append(pArray[i][3]) #row_4=pArray[:,3]
    LeftLoop4(row_2,1)
    LeftLoop4(row_3,2)
    LeftLoop4(row_4,3)
    for i in range(4):
        pArray[i][1]=row_2[i]
        pArray[i][2]=row_3[i]
        pArray[i][3]=row_4[i]

def inv_LeftLoop4(inv_row,step):
    temp=[]
    for i in range(4):
        temp.append(inv_row[i])       #temp=inv_row
    for i in range(4):
        inv_row[i]=temp[(i-step+4)%4]

def inv_ShiftRows(pArray):
    inv_row_2, inv_row_3, inv_row_4=[],[],[]
    for i in range(4):
        inv_row_2.append(pArray[i][1]) #inv_row_2=pArray[:,1]
        inv_row_3.append(pArray[i][2]) #inv_row_3=pArray[:,2]
        inv_row_4.append(pArray[i][3]) #inv_row_4=pArray[:,3]
    inv_LeftLoop4(inv_row_2,1)
    inv_LeftLoop4(inv_row_3,2)
    inv_LeftLoop4(inv_row_4,3)
    for i in range(4):
        pArray[i][1]=inv_row_2[i]
        pArray[i][2]=inv_row_3[i]
        pArray[i][3]=inv_row_4[i] 

def Mul2(x):
    a=(x<<1)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def Mul3(x):
    a=((x<<1)^x)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def Mul9(x):
    a=((x<<3)^x)
    if(a//1024==1):
        a=a^(0x11b*0x4)
    if(a//512==1):
        a=a^(0x11b*0x2)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def MulB(x):
    a=((x<<3)^(x<<1)^x)
    if(a//1024==1):
        a=a^(0x11b*0x4)
    if(a//512==1):
        a=a^(0x11b*0x2)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def MulD(x):
    a=((x<<3)^(x<<2)^x)
    if(a//1024==1):
        a=a^(0x11b*0x4)
    if(a//512==1):
        a=a^(0x11b*0x2)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def MulE(x):
    a=((x<<3)^(x<<2)^(x<<1))
    if(a//1024==1):
        a=a^(0x11b*0x4)
    if(a//512==1):
        a=a^(0x11b*0x2)
    if(a//256==1):
        a=a^(0x11b)
    return(a)

def Fast_MixCol(pArray,KeyArray):
    T1,T2,T3=[],[],[]
    for i in range(4):
        T1.append(pArray[i])
        T2.append(pArray[i])
        T3.append(pArray[i])
    for col in range(4):
        for row in range(4):
            T2[col][row]=Mul2(T2[col][row])
            T3[col][row]=Mul3(T2[col][row])
    for col in range(4):
        pArray[col][0]=T2[col][0]^T3[(col+1)%4][1]^T1[(col+2)%4][2]^T1[(col+3)%4][3]^KeyArray[col][0]
        pArray[col][1]=T1[col][0]^T2[(col+1)%4][1]^T3[(col+2)%4][2]^T1[(col+3)%4][3]^KeyArray[col][1]
        pArray[col][2]=T1[col][0]^T1[(col+1)%4][1]^T2[(col+2)%4][2]^T3[(col+3)%4][3]^KeyArray[col][2]
        pArray[col][3]=T3[col][0]^T1[(col+1)%4][1]^T1[(col+2)%4][2]^T2[(col+3)%4][3]^KeyArray[col][3]

def Inv_MixCol(pArray):
    T1,T2,T3,T4=[],[],[],[]
    for i in range(4):
        T1.append(pArray[i])
        T2.append(pArray[i])
        T3.append(pArray[i])
        T4.append(pArray[i])
    for col in range(4):
        for row in range(4):
            T1[col][row]=Mul9(T1[col][row])
            T2[col][row]=MulB(T2[col][row])
            T3[col][row]=MulD(T3[col][row])
            T4[col][row]=MulE(T4[col][row])
    for col in range(4):
        pArray[col][0]=T4[col][0]^T2[col][1]^T3[col][2]^T1[col][3]
        pArray[col][1]=T1[col][0]^T4[col][1]^T2[col][2]^T3[col][3]
        pArray[col][2]=T3[col][0]^T1[col][1]^T4[col][2]^T2[col][3]
        pArray[col][3]=T2[col][0]^T3[col][1]^T1[col][2]^T4[col][3]

def AddRoundKey(pArray,KeyArray):
    for col in range(4):
        for row in range(4):
            pArray[col][row]=pArray[col][row]^KeyArray[col][row]
#Read AES_Secretkey
with open( "AES_Secretkey.txt","r" ) as f:
    keystr=f.read()
    keylist_1=keystr.split(',')
#Process AES_Secretkey 
keylist_2=list(map(lambda x:(int(x))%256,keylist_1))
if(len(keylist_2)!=16):
    exit(0)
#Put AES_Secretkey into Matrix
KeyArray=[]
for i in range(4):
    KeyArray.append(keylist_2[4*i:4*i+4])
#Create W Matrix
w=[[0 for row in range(4)] for col in range(44)]
ExtendKey(KeyArray)
#AES_ECB
def AESEncrypt(pArray):
    AddRoundKey(pArray,w[0:4])       #The 1st round AddRoundKey
    for i in range(9):               #9 times single round encryption
        for col in range(4):         #Bytes Substitution
            for row in range(4):
                pArray[col][row]=SubBytes(pArray[col][row])
        Fast_MixCol(pArray,w[4*(i+1):4*(i+2)])        #Fast Completion: ShiftRows & MixCol & AddRoundKey
    for col in range(4):             #The 10th single round encryption & Bytes Substitution
        for row in range(4):
            pArray[col][row]=SubBytes(pArray[col][row])
    ShiftRows(pArray)
    AddRoundKey(pArray,w[40:44])

#Inv_AES_ECB
def Inv_AESEncrypt(pArray):
    AddRoundKey(pArray,w[40:44])       #The 1st round AddRoundKey
    for i in range(9):               #9 times single round encryption
        inv_ShiftRows(pArray)        
        for col in range(4):
            for row in range(4):
                pArray[col][row]=Inv_SubBytes(pArray[col][row])
        AddRoundKey(pArray,w[4*(9-i):4*(10-i)])
        Inv_MixCol(pArray)       
    inv_ShiftRows(pArray) 
    for col in range(4):
        for row in range(4):
            pArray[col][row]=Inv_SubBytes(pArray[col][row])
    AddRoundKey(pArray,w[0:4])

temp_matrix=[]
for i in range(len(temp_int_1_list)//4):
    temp_matrix.append(temp_int_1_list[4*i:4*i+4])
for i in range(len(temp_matrix)//4):
    AESEncrypt(temp_matrix[4*i:4*i+4])
cipher=[]
for i in range(len(temp_matrix)):
    cipher=cipher+temp_matrix[i]

cipher_matrix_AES =np.matrix(list( map( lambda x:np.int( x ),cipher ) ))
matrix_cipher_AES=cipher_matrix_AES.reshape(height,width)
#Output
image_AES_cipher = Image.fromarray( matrix_cipher_AES )
plt.imshow( image_AES_cipher,cmap='Greys_r' )
plt.imsave( "AESCipher.bmp",image_AES_cipher,cmap='Greys_r' )

for i in range(len(temp_matrix)//4):
    Inv_AESEncrypt(temp_matrix[4*i:4*i+4])
plain=[]
for i in range(len(temp_matrix)):
    plain=plain+temp_matrix[i]

plain_matrix_AES =np.matrix(list( map( lambda x:np.float( x/256 ),plain ) ))
matrix_plain_AES=plain_matrix_AES.reshape(height,width)
#Output
image_AES_plain = Image.fromarray( matrix_plain_AES )
plt.imshow( image_AES_plain,cmap='Greys_r' )
plt.imsave( "AESPlain.bmp",image_AES_plain,cmap='Greys_r' )
