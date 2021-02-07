with open( "Input.txt", "r" ) as f:    #打开文件
    input = f.read( )   #读取文件
if len( input ) < 10 or len( input ) > 1048576:   #判断输入合法性 1048576=1024*1024
    print( "Input is invalid!" )
    exit( 0 )
CD = [ 1 ]
TD = [ 1 ]
BD = [ 1 ]
s = [ ]
L,m = 0,0
for j in range( 0,len( input ) ):
    s.append( int( input[ j ] ) )
for j in range( 0,len(s) ):
    d = 0
    for i in range( 0,L + 1 ):
        while( len( CD ) < i + 1 ):
            CD.append( 0 )
        temp = ( s[ j - i ] * CD[ i ] ) % 2
        d = ( d + temp ) % 2
    m = m + 1
    if d != 0:
        TD = CD
        BBD = [ ]
        for i in range( 0,m ):
            BBD.append( 0 )
        BBD = BBD + BD
        if len( TD ) > len( BBD ):
            while( len( TD ) > len( BBD ) ):
                BBD.append( 0 )
        else:
            while( len( TD ) < len( BBD ) ):
                TD.append( 0 )
        CD = [ ]
        for i in range( 0,len( TD ) ):
            temp = ( TD[ i ] + BBD[ i ] ) % 2
            CD.append( temp )
        if L <= j / 2:
            L = j + 1 - L
            if L>10000:
                print("The linear complexity is more than 10000!")
                exit(0)
            BD = [ ]
            for i in range( 0,len( TD ) ):     #BD=TD
                BD.append( TD[ i ] )
            m = 0
print("The linear complexity is",end=' ')
print(L)
#输出联结多项式
for i in range(len(CD)-1,0,-1):
    if CD[i]==1:
        print("D^",i,"+",sep='',end='')
print('1')
