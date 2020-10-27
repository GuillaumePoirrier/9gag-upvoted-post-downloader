from appJar import gui
import requests
import shutil
import time
import datetime
import os
import glob

app = gui()
gag_prefix = 'https://img-9gag-fun.9cache.com/photo/'
generated_data_filename='data.txt'
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
    app.addButton('Pause', pause)
    app.disableButton('Pause')

def submit(button):  
    inputPath , outputPath =  app.getEntry('inputPath'), app.getEntry('outputPath')
    if outputPath and inputPath != '':
        runningMode()
        t0 = time.process_time()
        print(t0)
        convertFileToIdsList(inputPath)
        app.thread(readIds, outputPath)
    else:
        app.errorBox('Input Data', 'Please input your html file and select the output directory', parent=None)

def runningMode():
    app.enableButton('Pause')
    app.disableEntry('inputPath')
    app.disableEntry('outputPath')
    app.disableButton('Submit')

def readIds(outputPath):
    global running
    totalCount = countLines(generated_data_filename)
    ids = open(generated_data_filename, 'r')
    lines = ids.readlines()
    count = 0
    for line in lines:
        line=line.strip()
        count += 1
        if not line:
            break
        downloadFiles(line, outputPath, count, totalCount)
        if running==False:
            ids.close()
            app.setStatusbar('Paused', field=0)
            app.enableButton('Submit')
            app.setButton('Submit', 'Resume')
            app.disableButton('Pause')
            app.setButtonCursor('Pause','arrow')
            running = True
            break
    ids.close()

def downloadFiles(line, outputPath, count, totalCount):
    extensions = ['_460sv.mp4','_700bwp.webp',  '_460svvp9.webm',
                    '_460svav1.mp4']
    found=False
    for i in range(0, len(extensions)):
        if found == False:
            if doesExist(line, outputPath) == False:
                r = requests.get(
                    gag_prefix + line + extensions[i], stream=True)
                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open(outputPath+'/'+line+extensions[i], 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    app.setMeter('progress', (count/totalCount)*100)
                    app.setStatusbar('Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. Estimated '+ getEstimatedTime(count, totalCount), field=0)
                    found=True
                if count == totalCount:
                    app.setStatusbar('[finished] Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. elapsed time: '+ (str(datetime.timedelta(seconds=round(time.process_time()-t0)))), field=0)

            else:
                app.setStatusbar('[Already found] Status : ['+str(count)+'/'+str(totalCount)+'] downloaded. Estimated '+ getEstimatedTime(count, totalCount), field=0)


def pause(button):
    global running
    app.setButtonCursor('Pause','watch')
    running = False

def doesExist(filename, outputPath):
    exist = False
    files = glob.glob(outputPath+'/*')
    for file in files:
        if filename in file:
            exist =True
    return exist

def getEstimatedTime(count, totalCount):
    seconds = round(((time.process_time()-t0+totalCount)/count))*60
    return(str(datetime.timedelta(seconds=seconds)))

def countLines(inputPath):
    # Counting total amount of ids
    ids = open(inputPath, 'r')
    print(ids)
    totalCount = 0
    for line in ids:
        if line != '\n':
            totalCount += 1
    ids.close()
    return totalCount

def convertFileToIdsList(inputPath):
    with open(inputPath) as infile, open('upvotes.txt', 'w') as upvotes:
        copy = False
        for line in infile:
            if line.strip() == '<h3>Upvotes</h3>':
                copy = True
                continue
            elif line.strip() == '<h3>Downvotes</h3>':
                copy = False
                continue
            elif copy:
                upvotes.write(line)
    upvotes.close()
    infile.close()
    
    with open('upvotes.txt') as upvotes, open('urls.txt', 'w') as urls:
        for line in upvotes:
            if 'href' in line:
                urls.write(line)
    upvotes.close()
    urls.close()

    with open('urls.txt') as urls, open(generated_data_filename, 'w') as data:
        for line in urls:
            data.write(line[46:53]+'\n')
    data.close()
    urls.close()

    os.remove('upvotes.txt')
    os.remove('urls.txt')


if __name__ == '__main__':
    main()