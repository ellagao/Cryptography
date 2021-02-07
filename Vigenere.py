with open( "Plaintext1.txt", "r" ) as f:    #打开文件
    plaintext = f.read( )   #读取文件
with open( "SecretKey.txt", "r" ) as f:    #打开文件
    secretkey = f.read( )   #读取文件
def VigenereEncrypt ( code,key ): #明文为小写字母，密钥为小写字母，密文为大写字母，输出密文
    result = ''
    for i in range( 0,len( code ) ):
        asc1 = ord( key[ i % len( key ) ] ) - ord( 'a' )
        asc2 = ord( code[ i ] ) - ord( 'a' )
        temp = ( asc1 + asc2 ) % 26 + ord( 'A' )
        result = result + chr( temp )
    return( result )
with open( "Ciphertext.txt","w" ) as f:
    f.write( VigenereEncrypt( plaintext,secretkey ) )  #任务一完成，输出密文到Ciphertext.txt中
PlainText = [ ]    #存放两个明文
with open( "Plaintext.txt", "r" ) as f:    #打开明文文件
    for code1 in f.readlines( ):
        code1 = code1.strip( '\n' )  #去掉列表中每一个元素的换行符
        PlainText.append( code1 )

if PlainText[ 0 ].isalpha( ) == False or PlainText[ 1 ].isalpha( ) == False : #检查两个明文是否只包含字母
    print( "The plaintexts inputted are not invalid!" )
    exit( 0 )
if len( PlainText[ 0 ] ) != len( PlainText[ 1 ] ):  #检查两个明文长度是否相同
    print( "The plaintexts inputted are not invalid!" )
    exit( 0 )
TextA = PlainText[ 0 ].lower( )
TextB = PlainText[ 1 ].lower( )
asclist = [ ]
key1 = [ ]
key2 = [ ]
finalkey1 = ''
finalkey2 = ''
cipher1 = ''
cipher2 = ''
for i in range( 0,len( TextA ) ):
    asc = ord( TextA[ i ] ) - ord( TextB[ i ] )
    asc = ( asc + 26 ) % 26
    asclist.append( asc )
length = len( asclist )
#定义用欧几里得算法求最大公约数函数
def seekGCD ( x,y ):
    #找较大的数
    if x > y:
        max,min = x, y
    else:
        max,min = y, x
    while( min != 0 ):
        max = max % min
        if max < min:
            max,min = min,max
    return( max )
#定义求最小公倍数函数
def seekLCM ( x,y ):
    gcd = seekGCD( x,y )
    return( x * y // gcd )
#判断数组是否循环，并且返回循环的最小单位，若不循环则返回明文长度
def cycle ( asclist ):
    import operator
    length = len( asclist )
    count = asclist.count( asclist[ 0 ] )
    if count == 1: #第一个元素只出现了一次
        return( length )
    if count == 2: #第一个元素出现两次
        loca = asclist.index( asclist[ 0 ],1 )
        if operator.eq( asclist[ 0:( length - loca ) ],asclist[ loca: ] ):
            return( loca )
        else:
            return( length )
    if count > 2: #第一个元素出现超过两次
        indexlist = [ ] #第一个元素出现位置列表
        loca = 0
        for i in range( 0,count - 1 ):
            loca = asclist.index( asclist[ 0 ],loca + 1 )
            indexlist.append( loca )
        for i in range( 0,len( indexlist ) ):
            flag = True
            loca = indexlist[ i ]
            judge = asclist[ 0: loca ]
            while loca < length - len( judge ):
                if not operator.eq( judge,asclist[ loca:( loca + len( judge ) ) ] ):
                    flag = False
                    break  #此loca无效
                else:
                    loca = loca + len( judge ) #可能成功，loca继续
            if flag == False:
                continue
            if operator.eq( judge[ 0:( length - loca ) ],asclist[ loca: ] ): #最后一轮不完整的判断
                return( indexlist[ i ] )
            else:
                i = i + 1
        return( length )
    return( 0 ) #ERROR
cyclenum = cycle( asclist )
if cyclenum == 0: #ERROR终止程序
    exit( 0 )
def searchkey ( asclist,cyclenum ):
    import random
    import operator
    import copy
    global key1
    global key2
    global finalkey1
    global finalkey2
    global cipher1
    global cipher2
    if cyclenum <= length // 2:  #循环小于等于密钥最大长度，密钥长度=循环
        key1 = [ 0 ] * cyclenum
        key2 = [ 0 ] * cyclenum
        for i in range( 0,cyclenum ):
            key1[ i ] = chr( random.randint( 0,25 ) + ord( 'a' ) )
            key2[ i ] = chr( ( ord( key1[ i ] ) - ord( 'a' ) + asclist[ i ] ) % 26 + ord( 'a' ) )
        finalkey1 = "".join( key1 )
        finalkey2 = "".join( key2 )
        cipher1 = VigenereEncrypt( TextA,finalkey1 )
        cipher2 = VigenereEncrypt( TextB,finalkey2 )
        if operator.eq( cipher1,cipher2 ):
            return( 1 )  #找到密钥
    else:  #循环大于密钥长度
        for i in range( 1,length // 2 + 1 ):  #i表示secretkey1长度
            for j in range( i + 1,length // 2 + 1 ): #j表示secretkey2长度
                if seekLCM( i,j ) == cyclenum or seekLCM( i,j ) >= length :
                    key1 = [ 0 ] * i  #初始化secretkey1列表
                    expand1 = [ 0 ] * i  #初始化secretkey1是否被扩展过，如果被扩展为1，未被扩展为0
                    sure1 = [ 0 ] * i   #初始化secretkey1值是否确定，如果不确定为0，确定为1
                    key2 = [ 0 ] * j  #初始化secretkey2列表
                    expand2 = [ 0 ] * j  #初始化secretkey2是否被扩展过，如果被扩展为1，未被扩展为0
                    sure2 = [ 0 ] * j   #初始化secretkey2值是否确定，如果不确定为0，确定为1
                    turn,flag = 0,1 #turn表示当前扩展key1还是key2，0代表key1,1代表key2，flag表示成功的可能性
                    sure1[ 0 ] = 1  #设定secretkey1第一个字符为'a'
                    while ( expand1.count( 0 ) != 0 or expand2.count( 0 ) != 0 ) and flag == 1:
                        if turn == 0 and expand1.count( 0 ) != 0: 
                            for t in range( 0,i ):  #找最小未扩展
                                if sure1[ t ] == 1 and expand1[ t ] == 0:
                                    break
                            expand1[ t ] = 1
                            for p in range( t,length,i ):
                                q = p % j
                                alpha = ( key1[ t ] + asclist[ p ] + 26 ) % 26
                                if sure2[ q ] == 0:  #判断冲突
                                    key2[ q ] = alpha
                                    sure2[ q ] = 1
                                else:
                                    if key2[ q ] != alpha:
                                        flag = 0
                                        break  #break for
                        if flag == 0:
                            break    #break while
                        if turn == 1 and expand2.count( 0 ) != 0: 
                            for t in range( 0,j ):  #找最小未扩展
                                if sure2[ t ] == 1 and expand2[ t ] == 0:
                                    break
                            expand2[ t ] = 1
                            for p in range( t,length,j ):
                                q = p % i
                                alpha = ( key2[ t ] - asclist[ p ] + 26 ) % 26
                                if sure1[ q ] == 0:  #判断冲突
                                    key1[ q ] = alpha
                                    sure1[ q ] = 1
                                else:
                                    if key1[ q ] != alpha:
                                        flag = 0
                                        break    #break for
                        if flag == 0:
                            break     #break while
                        turn = ( turn + 1 ) % 2
                    if flag == 1:
                        for i in range( 0,len( key1 ) ):
                            key1[ i ] = chr( key1[ i ] + ord( 'a' ) )
                        for j in range( 0,len( key2 ) ):
                            key2[ j ] = chr( key2[ j ] + ord( 'a' ) )
                        finalkey1 = "".join( key1 )
                        finalkey2 = "".join( key2 )
                        cipher1 = VigenereEncrypt( TextA,finalkey1 )
                        cipher2 = VigenereEncrypt( TextB,finalkey2 )
                        if operator.eq( cipher1,cipher2 ):
                             return( 1 )  #找到密钥
    return( 0 )  #找不到密钥
with open( "Secret.txt","w" ) as f:
    if searchkey( asclist,cyclenum ) == 1:
        f.write( "The secretkeys are successfully found!\n" )
        f.write( "The first plaintext is:\n" + TextA + '\n' + "The first secretkey is:\n" + finalkey1 + '\n' + "The first ciphertext is:\n" + cipher1 + '\n' )
        f.write( "The second plaintext is:\n" + TextB + '\n' + "The second secretkey is:\n" + finalkey2 + '\n' + "The second ciphertext is:\n" + cipher2 + '\n' )
    else :
        f.write( "The secretkeys are not found!\n" )
        f.write( "The first plaintext is:\n" + TextA + '\n' )
        f.write( "The second plaintext is:\n" + TextB + '\n' )
