#this code was made to work for a quick demonstration, dont use it for more than that
#it will break and take forever to run

#if you want to know why its so terrible, this is my first time doing anything more complex than math in python
#also the V1 is somehow even worse, so please dont ask about it

from PIL import Image
import math
import os
import cv2
import time

def averagelist(toavg):
    avg = 0
    for a in toavg:
        avg += a
    return avg/len(toavg)

def doframe(filename):
    img = Image.open("frame.png")
    imglist = list(img.resize([64,48]).getdata()) #resize image to 64x48 pixels and turn it into a list of RGB values
    img.close()
    avglist = []
    for i in imglist:
        avglist.append(averagelist(i)) #average colors to make image greyscale

    for f in range(15): #one loop per pattern on a page
        x, y = f%5, math.floor(f/5)
        name = "data/"+str((filename*1000)+f+1000000000000)+".cgp" #make sure all file names are the same length, the order gets messed up if you dont
        cpg = open(name,"w")
        if x == 0: #this is a horrible approach, im hopefully going to redo this eventually
            for yy in range(16):
                cpg.write("(-10)"*8)
                for xx in avglist[((yy+(y*16))*64)+(x*16):((yy+(y*16))*64)+(x*16)+8]: #i couldnt tell you how this works
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
0000000000000000"""*16) #write 16 lines of blank prefab data
        cpg.close()



cam = cv2.VideoCapture("video.mp4") #video file name goes here!
try:
    if not os.path.exists("data"):
        os.makedirs("data")
except OSError:
    print("directory failed")

curframe = 0
while True: #replace with "while curframe < number" to limit the number of frames to number
    ret,frame = cam.read()
    if ret:
        cv2.imwrite("frame.png", frame)
        doframe(curframe)
        print("performing frame: "+str(curframe)) #hopefully going to add an ETA timer eventually
        curframe += 1
    else:
        break

time = time.process_time()
print("\nTook " + str(time) + " Seconds") #it orignally told you how many minutes, but for some reason it always said 0

#if you understood this, congrats, your probably smarter than me
