import os
import random
import copy
import shutil
import sys
import argparse

parser = argparse.ArgumentParser()

verbose = """What is this script for?
> It provides to create k different datasets that have k different validation sets from base dataset.
> It is similiar to k-fold cross validation method. But this script creates k different dataset.

How it works?
> Script reads all of the labels that in given in the label path. 
> It accepts the first labeled class in the label file as the class of the label file. And counts number of labels for each class.
> To get validation size of each class, divides number of each class value to k value.
> Script uses "random.randint" to create k different "randomize" validation sets. 
> Saves each generated dataset to "generatedCrossValDataSet" folder as set_x.

How to use?
> Script gets 4 parameters.
>> -img_path=your_image_files_directory
>> -lbl_path=your_label_files_directory
>> -nof_cls=number_of_class_of_your_dataset
>> -k=number_of_dataset_that_will_be_created

Here is an example for generating 5 different dataset from helper_data_v5_2_whole file that have 5 classes: 

python dataset_shuffler_for_yolo.py -img_path=helper_data_v5_2_whole/images -lbl_path=helper_data_v5_2_whole/labels -nof_cls=5 -k=5"""

parser.add_argument("-img_path", help="Directory path of all images.", type=str)
parser.add_argument("-lbl_path", help="Directory path of all labels.", type=str)
parser.add_argument("-nof_cls", help="Number of classes in dataset.", type=int)
parser.add_argument("-k", help="Number of datasets that will be created.", type=int)
parser.add_argument("-verbose", help="Usage and detailed info.", action="store_true")
args = parser.parse_args()

if args.verbose:
    print(verbose)
    sys.exit()
if args.nof_cls < 1:
    print("Non-valid nof_cls value input")
    sys.exit()
if args.k < 1:
    print("Non-valid k value input.")
    sys.exit()
if not os.path.isdir(args.lbl_path):
    print("Label directory doesn't exist: " + args.lbl_path)
    sys.exit()
if not os.path.isdir(args.img_path):
    print("Image directory doesn't exist: " + args.img_path)
    sys.exit()


imgPath = args.img_path
lblPath = args.lbl_path
nofClass = args.nof_cls
kVal = args.k

if imgPath[-1] != '/' or imgPath[-1] != '\\':
    imgPath += '/'
if lblPath[-1] != '/' or lblPath[-1] != '\\':
    lblPath += '/'

# script runs for .jpg, .jpeg, and .png files.
# if you have different image file extension like
# .bmp add it in "ADD ME" sections :)

images = os.listdir(imgPath)
labels = os.listdir(lblPath)

lLabels = [[] for _ in range(nofClass)]
allLabels = []

print("Reading label files...")
for i in labels: # creating list that contains labels for each class.
    if '.txt' not in i:
        continue
    f = open(lblPath + i, 'r')
    lblVal = f.read()
    if(len(lblVal) == 0):
        print(i)
    lblVal = lblVal[0]
    lLabels[int(lblVal)].append(i)
    allLabels.append(i)
    
print("Reading files completed.")

nofLabels4EachClass = []

for i in range(nofClass):
    nofLabels4EachClass.append(int(len(lLabels[i]) / kVal))

trainLabels = [[[]] for _ in range(nofClass)]
valLabels = [[[]] for _ in range(nofClass)]

print("Generating shuffled labels...")
# creating validation sets
for i in range(nofClass):
    tmpClassLabels = lLabels[i]
    tmpValLabelList = [[] for _ in range(kVal)]
    for j in range(kVal):
        classVal = nofLabels4EachClass[i]
        tmpValLabel = []
        while classVal > 0:
            n = random.randint(0, len(tmpClassLabels) - 1)
            classVal = classVal - 1
            tmpValLabel.append(tmpClassLabels[n])
            del tmpClassLabels[n]
        tmpValLabelList[j].append(tmpValLabel)
    valLabels[i].append(tmpValLabelList)

for i in range(nofClass):
    for j in range(len(lLabels[i])):
        valLabels[i][1][j][0].append(lLabels[i][j])
        
print("Shuffled labels generated.")        
trainSet = []
valSet = []

print("Creating datasets...")   
for i in range(kVal):
    #tmpTrainDataSet = allLabels.copy()
    tmpTrainDataSet = copy.deepcopy(allLabels)
    tmpValDataSet = []
    for j in range(nofClass):
        tmpValDataSetClass = []
        for k in range(len(valLabels[j][1][i][0])):
            tmpValDataSetClass.append(valLabels[j][1][i][0][k])
            tmpIndex = tmpTrainDataSet.index(tmpValDataSetClass[k])
            del tmpTrainDataSet[tmpIndex]
        tmpValDataSet.append(tmpValDataSetClass)
    trainSet.append(tmpTrainDataSet) # train
    valSet.append(tmpValDataSet)

print("Datasets created.")

valSetVectorized = []       
for i in range(kVal):
    tmpValSetVectorized = []
    for j in range(nofClass):
        for k in range(len(valSet[i][j])):
            tmpValSetVectorized.append(valSet[i][j][k])
    valSetVectorized.append(tmpValSetVectorized) # validation

folderName = "generatedCrossValDataSet"
kThDataSetFolderName = "set_"

if os.path.isdir(folderName):
    os.rmdir(folderName) # removing existing dataset.
    os.mkdir(folderName)
else:
    os.mkdir(folderName)
    
print("Copying files...")
for i in range(kVal):
    tmpFolderName = kThDataSetFolderName + str(i + 1)
    tmpDir = folderName + "/" + tmpFolderName
    tmpLabelFolder = tmpDir + "/" + "labels"
    tmpImageFolder = tmpDir + "/" + "images"
    os.mkdir(tmpDir)
    os.mkdir(tmpLabelFolder)
    os.mkdir(tmpImageFolder)
    tmpTrainLabelFolder = tmpLabelFolder + "/train"
    os.mkdir(tmpTrainLabelFolder)
    tmpValLabelFolder = tmpLabelFolder + "/val"
    os.mkdir(tmpValLabelFolder)
    tmpTrainImageFolder = tmpImageFolder + "/train"
    os.mkdir(tmpTrainImageFolder)
    tmpValImageFolder = tmpImageFolder + "/val"
    os.mkdir(tmpValImageFolder)
    
    for j in range(len(trainSet[i])):
        fileName = trainSet[i][j]
        shutil.copy(lblPath + trainSet[i][j], tmpTrainLabelFolder) # copying training labels.
        fileName = fileName[:-4] # removing ".txt" file extension.
        #ADD ME
        if os.path.isfile(imgPath + fileName + ".jpg"):
           tmpImgFileName = fileName + ".jpg"
        elif os.path.isfile(imgPath + fileName + ".png"):
             tmpImgFileName = fileName + ".png"
        elif os.path.isfile(imgPath + fileName + ".jpeg"):
             tmpImgFileName = fileName + ".jpeg"
        else:
            print("File extension non-exist in this script.")
            print(fileName)
            continue
        shutil.copy(imgPath + tmpImgFileName, tmpTrainImageFolder + "//")
        
    for j in range(len(valSetVectorized[i])):
        fileName = valSetVectorized[i][j]
        shutil.copy(lblPath + valSetVectorized[i][j], tmpValLabelFolder + "//") # copying training labels.
        fileName = fileName[:-4] # removing ".txt" file extension.
        #ADD ME
        if os.path.isfile(imgPath + fileName + ".jpg"):
            tmpImgFileName = fileName + ".jpg"
        elif os.path.isfile(imgPath + fileName + ".png"):
            tmpImgFileName = fileName + ".png"
        elif os.path.isfile(imgPath + fileName + ".jpeg"):
            tmpImgFileName = fileName + ".jpeg"
        else:
            print("File extension non-exist in this script.")
            print(fileName)
            continue
        shutil.copy(imgPath + tmpImgFileName, tmpValImageFolder + "//")
print("Datasets generated! Number of created generated: " + str(i + 1))
