import os
import sys

dir = os.getcwd() #C:\Users\User\Documents\IHDIA_cloud_vision\gocr
#print(dir)
bookName = 'ATHARVAVEDA'


currentPath = os.path.join(dir,bookName)
print(" current path is: " + currentPath)

dir_list = os.listdir(currentPath)
# print(" directory list of current path is; ", dir_list)

#for filename in dir_list:
    #newFilename = filename.replace(' ', '-')
    #print(newFilename)
    #src = os.path.join(currentPath, filename)
    #dst = os.path.join(currentPath, newFilename)
    #os.rename(src,dst)

#print(dir_list[1])
with open(r"test.txt", 'w') as file:
    for filename in dir_list:
        fullPath = os.path.join(currentPath, filename)
        file.write(fullPath + "\n")

