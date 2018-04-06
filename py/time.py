import time
sec = int(input('COUNTDOWN TIMER:How many seconds?'))

for i in range(sec,0,-1):     
    print (i,end="")                 #该语句写在这里即把数字先输出
    for star in range(0,i):   #这里也可以直接写成range(i)
        print ("*",end="")            #注意逗号，表示转行了                  
    time.sleep(1)
    print()
print ("BLAST OFF!")
