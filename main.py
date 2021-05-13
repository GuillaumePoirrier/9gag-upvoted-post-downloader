#################################################
#   Developped with love by GuillaumePoirrier   #
#   Do not hesitate to suggest improvements !   #
#################################################

from appJar import gui
import requests
import shutil
import time
import datetime
import os
import glob
import pandas as pd

import resources.const.constants as cst


##
# GUI is managed by appjar lib: http://appjar.info/
# data processing done with pandas : https://pandas.pydata.org/
# requests are done with requests: https://pypi.org/project/requests/
##

app = gui()
running = True
t0 = 0

def main():
    initApp()

def initApp():
    createWidgets()
    app.go()

def createWidgets():
    app.setTitle(cst.TITLE_LABEL)
    app.setSize(500, 300)
    app.setPadding(8)
    app.setResizable (False)
    app.addLabel(cst.TITLE, cst.MAIN_LABEL)
    app.addFileEntry(cst.INPUT_FILE)
    app.setEntryDefault(cst.INPUT_FILE, cst.INPUT_FILE_PLACEHOLDER)
    app.addDirectoryEntry(cst.OUTPUT_PATH)
    app.setEntryDefault(cst.OUTPUT_PATH, cst.OUTPUT_PATH_PLACEHOLDER)
    app.addButton(cst.SUBMIT_BUTTON, submit)
    app.addMeter(cst.PROGRESS_BAR)
    app.setMeterFill(cst.PROGRESS_BAR, cst.BLUE)
    app.addStatusbar(header='', fields=1, side=None)
    app.addButton(cst.PAUSE_BUTTON, pauseMode)
    app.disableButton(cst.PAUSE_BUTTON)

def submit(button):  
    global t0 
    inputPath , outputPath =  app.getEntry(cst.INPUT_FILE), app.getEntry(cst.OUTPUT_PATH)
    if outputPath and inputPath != '':
        outputPath+='/'
        runningMode()
        t0 = time.time()
        app.thread(readIds, outputPath, getUpvoteListFromFile(inputPath))
    else:
        app.errorBox('Input Data', cst.WRONG_INPUTS, parent=None)

def runningMode():
    app.enableButton(cst.PAUSE_BUTTON)
    app.disableEntry(cst.INPUT_FILE)
    app.disableEntry(cst.OUTPUT_PATH)
    app.disableButton(cst.SUBMIT_BUTTON)

def readIds(outputPath, data):
    global running
    totalCount = len(data)
    for idx, val in enumerate(data):
        print('id', val[1])
        downloadFiles(val, outputPath, idx+1, totalCount)
        if running==False:
            app.setStatusbar(cst.STATUS_PAUSE, field=0)
            app.enableButton(cst.SUBMIT_BUTTON)
            app.setButton(cst.SUBMIT_BUTTON, cst.RESUME_BUTTON)
            app.disableButton(cst.PAUSE_BUTTON)
            app.setButtonCursor(cst.PAUSE_BUTTON, cst.MOUSE_ARROW)
            running = True
            break

def downloadFiles(val, outputPath, count, totalCount):
    found = False
    for i in range(0, len(cst.FILE_EXTENSIONS)):
        if found == False:
            if doesExist(val, outputPath) == False:
                r = requests.get(cst.NINE_GAG_PREFIX + val[1] + cst.FILE_EXTENSIONS[i], stream=True)
                if r.status_code == 200:
                    print('dl')
                    r.raw.decode_content = True
                    with open(outputPath+filename(val)+cst.FILE_EXTENSIONS[i], 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    app.setMeter(cst.PROGRESS_BAR, (count/totalCount)*100)
                    app.setStatusbar(
                        cst.STATUS_LABEL
                        + ' : ['
                        + str(count)
                        + '/'
                        + str(totalCount)
                        + '] '
                        + cst.DOWNLOADED
                        +' '
                        + cst.ESTIMATED
                        + ' '
                        + getEstimatedTime(count, totalCount), field=0)
                    found = True
                if count == totalCount:
                    app.setStatusbar(
                        '['+cst.FINISHED_STATUS+'] '
                        + cst.STATUS_LABEL
                        + ' : ['
                        + str(count)
                        + '/'
                        + str(totalCount)
                        + '] '
                        + cst.DOWNLOADED
                        + cst.ELAPSED_TIME
                        + str(time.time()-t0), field=0)
            else:
                app.setStatusbar(
                    '['+cst.ALREADY_FOUD_STATUS+'] '
                    + cst.STATUS_LABEL
                    + ' : ['
                    + str(count)
                    + '/'
                    + str(totalCount)
                    + '] '
                    + cst.DOWNLOADED
                    + ' '
                    + cst.ESTIMATED
                    +' '
                    + getEstimatedTime(count, totalCount), field=0)


def pauseMode(button):
    global running
    app.setButtonCursor(cst.PAUSE_BUTTON, cst.MOUSE_WATCH)
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
    seconds = round(((time.time() - t0) * totalCount ) / count)
    return(str(datetime.timedelta(seconds=seconds)))
    
def getUpvoteListFromFile(inputPath):
    with open(inputPath, encoding="utf8") as infile, open(cst.TEMP_DATA_FILENAME, 'w', encoding="utf8") as upvoteList:
        copy = False
        for line in infile:
            if line.strip() == cst.UPVOTES_SECTION :
                copy = True
                continue
            elif line.strip() == cst.DOWNVOTES_SECTION :
                copy = False
                continue
            elif copy:
                upvoteList.write(line)
    upvoteList.close()
    
    idDataFrame = pd.read_html(cst.TEMP_DATA_FILENAME)[0].values.tolist()

    for id in idDataFrame:
        id[1] = id[1][-7:]
        id[0] = id[0][:10]

    os.remove(cst.TEMP_DATA_FILENAME)
    return idDataFrame


if __name__ == '__main__':
    main()
