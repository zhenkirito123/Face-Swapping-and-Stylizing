import os
N = 15
for i in range(15):
    src = 'data/{}.jpg'.format(i)
    for j in range(1):
        dst = 'data/{}.jpg'.format(j)
        out = 'result/{}'.format(i*15+j)
        res = os.system('python work.py {} {} {}'.format(src,dst,out))
        if(res!=0):
            print("Error in image{} or {}".format(i,j))