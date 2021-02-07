#读取密钥，存放在key中
import math
import numpy as np
key = np.loadtxt( "Input.txt",dtype=int,delimiter=' ' )
keylen = len( key )

#初始化
S = [ ]
T = [ ]
for i in range( 0,256 ):
    S.append( i )
    T.append( key[ i % keylen ] )

#S的初始置换
j = 0
for i in range( 0,256 ):
    j = ( j + S[ i ] + T[ i ] ) % 256
    #swap(S[i],S[j])
    temp = S[ i ]
    S[ i ] = S[ j ]
    S[ j ] = temp

#读取比特流
with open( "bitstream.txt", "r" ) as f:    #打开文件
    bitstream = f.read( )   #读取文件
M = list( bitstream )
MM = list( map( int, M ) )
if len(MM)!=256*8:
    print("ERROR")
    exit(0)
Message=[]
Cipher=[0]*256
for i in range(0,256):
    split=MM[i*8:i*8+8]
    for j in range(0,len(split)):
        temp=temp+math.pow(2,7-j)
    Message.append(temp)

i = j = 0
for p in range(0,256):
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    #swap(S[i],S[j])
    temp = S[ i ]
    S[ i ] = S[ j ]
    S[ j ] = temp
    t = (S[i] + S[j]) % 256
    Cipher[i] = MM[i] ^ S[t]
Ciphertext=[]
for i in range(0,256):
    temp=str(bin(Cipher[i]))
    temp1=temp[2:]
    Ciphertext.append(temp1)
result="".join(Ciphertext)
#输出密文到Ciphertext.txt中
with open( "Ciphertext.txt","w" ) as f:
    f.write( result )  

