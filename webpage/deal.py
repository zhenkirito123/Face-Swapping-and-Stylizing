import time,os
if __name__=='__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    ganPy=os.path.join(basedir, '../FSGAN/fsgan/inference/swap.py')
    possionPy=os.path.join(basedir,'../POSSION/work.py')
    targetDir=os.path.join(basedir, './static')
    targetDir2=os.path.join(basedir, './static/b')
    
    while True:
        try:
            with open("file.txt","r+") as f:
                str=f.read()
                if(str==""):
                    continue
                source=str.split()[0]
                target=str.split()[1]
                os.system("python {} {} {} {}".format(possionPy,source,target,targetDir2))
                os.system("python {} {} -t {} -o {}".format(ganPy,source,target,targetDir))

            with open("file.txt","r+") as f:
                f.truncate()
        except:
            time.sleep(0.1)
            continue
        time.sleep(0.1)