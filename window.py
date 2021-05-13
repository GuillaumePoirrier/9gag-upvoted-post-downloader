from appJar import gui
from pandas.core.frame import DataFrame
import requests
import shutil
import time
import datetime
import os
import glob
import pandas as pd

app = gui()
gag_prefix = 'https://img-9gag-fun.9cache.com/photo/'
running=True
t0=0


def main():
    initApp()

def initApp():
    createWidgets()
    app.go()

def createWidgets():
    app.setTitle('9gag upvotes downloader')
    app.setSize(500, 300)
    app.setPadding(8)
    app.setResizable (False)
    app.addLabel('title', 'Welcome to 9gag upvotes downloader !')
    app.addFileEntry('inputPath')
    app.setEntryDefault('inputPath', 'Input data html file')
    app.addDirectoryEntry('outputPath')
    app.setEntryDefault('outputPath', 'Output directory')
    app.addButton('Submit', submit)
    app.addMeter('progress')
    app.setMeterFill('progress', 'blue')
    app.addStatusbar(header='', fields=1, side=None)
    app.addButton('Pause', pauseMode)
    app.disableButton('Pause')

def submit(button):  
    inputPath , outputPath =  app.getEntry('inputPath'), app.getEntry('outputPath')
    if outputPath and inputPath != '':
        outputPath+='/'
        runningMode()
        t0 = time.process_time()
        app.thread(readIds, outputPath, convertFileToIdsList(inputPath))
    else:
        app.errorBox('Input Data', 'Please input your html file and select the output directory', parent=None)

def runningMode():
    app.enableButton('Pause')
    app.disableEntry('inputPath')
    app.disableEntry('outputPath')
    app.disableButton('Submit')

def readIds(outputPath, data):
    global running
    totalCount = len(data)
    for idx, val in enumerate(data):
        downloadFiles(val, outputPath, idx+1, totalCount)
        if running==False:
            app.setStatusbar('Paused', field=0)
            app.enableButton('Submit')
            app.setButton('Submit', 'Resume')
            app.disableButton('Pause')
            app.setButtonCursor('Pause','arrow')
            running = True
            break

def downloadFiles(val, outputPath, count, totalCount):
    extensions = ['_460sv.mp4',
                  '_700bwp.webp',
                  '_460svvp9.webm',
                  '_460svav1.mp4']
    found=False
    print(val[1])
    for i in range(0, len(extensions)):
        if found == False:
            if doesExist(val, outputPath) == False:
                r = requests.get(gag_prefix + val[1] + extensions[i], stream=True)
                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open(outputPath+filename(val)+extensions[i], 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    app.setMeter('progress', (count/totalCount)*100)
                    app.setStatusbar('Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. Estimated '+ getEstimatedTime(count, totalCount), field=0)
                    found=True
                if count == totalCount:
                    app.setStatusbar('[finished] Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. elapsed time: '+ (str(datetime.timedelta(seconds=round(time.process_time()-t0)))), field=0)
                    os.remove('data.txt')
            else:
                app.setStatusbar('[Already found] Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. Estimated '+ getEstimatedTime(count, totalCount), field=0)


def pauseMode(button):
    global running
    app.setButtonCursor('Pause','watch')
    running = False

def filename(val):
    return val[0]+val[1]

def doesExist(val, outputPath):
    exist = False
    files = glob.glob(outputPath+'/*')
    for file in files:
        if filename(val) in file:
            exist =True
    return exist

def getEstimatedTime(count, totalCount):
    seconds = round(((time.process_time()-t0+totalCount)/count))*60
    return(str(datetime.timedelta(seconds=seconds)))


def convertFileToIdsList(inputPath):
    with open(inputPath, encoding="utf8") as infile, open('upvoteList.txt', 'w', encoding="utf8") as upvoteList:
        copy = False
        for line in infile:
            if line.strip() == '<h3>Upvotes</h3>':
                copy = True
                continue
            elif line.strip() == '<h3>Downvotes</h3>':
                copy = False
                continue
            elif copy:
                upvoteList.write(line)
    upvoteList.close()
    
    idDataFrame = pd.read_html('upvoteList.txt')[0].values.tolist()

    for id in idDataFrame:
        id[1] = id[1][-7:]
        id[0] = id[0][:10]
        print(id[0])

    os.remove('upvoteList.txt')
    return idDataFrame


if __name__ == '__main__':
    main()
