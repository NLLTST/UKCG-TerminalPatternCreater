#this code was made to work for a quick demonstration, dont use it for more than that
#it will break and take forever to run

from PIL import Image
import math
import os
import cv2
import time

def averagelist(toavg):
    if True:
        avg = 0
        for a in toavg:
            avg += a
        return avg/len(toavg)

def doframe(filename):
    img = Image.open("frame.png")
    imglist = list(img.resize([64,48]).getdata())
    img.close()
    avglist = []
    for i in imglist:
        avglist.append(averagelist(i))

    for f in range(15): #one loop per pattern on a page
        x, y = f%5, math.floor(f/5)
        name = "data/"+str((filename*1000)+f+1000000000000)+".cgp"
        cpg = open(name,"w")
        if x == 0:
            for yy in range(16): #one for the y axis
                cpg.write("(-10)"*8)
                for xx in avglist[((yy+(y*16))*64)+(x*16):((yy+(y*16))*64)+(x*16)+8]:
                    cpg.write("("+str(math.floor(xx/12.2)-10)+")")
                cpg.write("\n")
        elif x == 4:
            for yy in range(16):
                for xx in avglist[((yy+(y*16))*64)+(x*16)-8:((yy+(y*16))*64)+(x*16)]:
                    cpg.write("("+str(math.floor(xx/12.2)-10)+")")
                cpg.write("(-10)"*8)
                cpg.write("\n")
        else:
            for yy in range(16):
                for xx in avglist[((yy+(y*16))*64)+(x*16)-8:((yy+(y*16))*64)+(x*16)+8]:
                    cpg.write("("+str(math.floor(xx/12.2)-10)+")")
                cpg.write("\n")
        cpg.write("""
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000""")
        cpg.close()



cam = cv2.VideoCapture("badapple.mp4")
try:
    if not os.path.exists("data"):
        os.makedirs("data")
except OSError:
    print("directory failed")

curframe = 0
while True:
    ret,frame = cam.read()
    if ret:
        cv2.imwrite("frame.png", frame)
        if curframe % 12 == 0:
            doframe(curframe)
            print(str(curframe)+" "+str(curframe/12))
        curframe += 1
    else:
        break

time = time.process_time()
print("\nTook " + str(time) + " Seconds")
