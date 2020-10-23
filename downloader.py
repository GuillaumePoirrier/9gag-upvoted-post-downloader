import requests
import shutil


data_filename = 'data.txt'

# Counting total amount of ids
ids = open(data_filename, 'r')
totalAmount = 0
for line in ids:
    if line != "\n":
        totalAmount += 1
ids.close()

# Donloadind files
ids = open(data_filename, 'r')
count = 0
while True:
    count += 1
    line = ids.readline().strip()
    if not line:
        break
    extensions = ['_460sv.mp4', '_460svvp9.webm',
                  '_460svav1.mp4', '_700bwp.webp']
    found = False
    for i in range(0, len(extensions)):
        if found == False:
            r = requests.get(
                'https://img-9gag-fun.9cache.com/photo/'+line+extensions[i], stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open('data/'+line+extensions[i], 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ', line, extensions[i])
                found = True
    if(count % 10 == 0):
        print(count, '/', totalAmount, '~', round(count/totalAmount), '%')
ids.close()
