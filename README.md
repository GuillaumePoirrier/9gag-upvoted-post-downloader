# 9gag upvoted posts downloader

This projects helps nostalgic 9gaggers retrieving and downloading old upvoted memes.



## Preparation

### Download project

Be careful to put your project in a place where you have enough storage to store your posts.

### Download your upvoted posts

1. Open a Python cli
2. run `pip install requests`
3. run `python3 downloader.py`

The posts that will be downloaded in /data directoryare the ones listed in data.txt. To download yours, go to next step


### Get Posts ids list

According to GDPR, all websites detaining personal informaton about you can be asked to give the user's all the data they detain about them. Thus, we have first to ask 9gag the list of all the data they have about your profile. 

 - Connect to your 9gag acount on your desktop.
 - Click on your profile picture > Settings >Privacy & Safety > Request my data.

Within minutes, you will receive a mail from 9gag. Download the file "You 9gag data"

Open the file with an editor ( Notepad ++ for instance)
Delete all the lines **until** :
```
<h3>Upvotes</h3>

    <table>
    <tr>
        <th>Creation Time</th>
        <th>Link</th>
        <th>Title</th>
    </tr>
```
And after :

```
<h3>Downvotes</h3>
```


The result shall be :


```
<h3>Upvotes</h3>

    <table>
    <tr>
        <th>Creation Time</th>
        <th>Link</th>
        <th>Title</th>
    </tr>
    <tr>
        <td>2020-10-23xxxxxxx</td>
        <td><a href="https://9gag.com/gag/xxxxx" target="_blank">https://9gag.com/gag/xxxxx</a><td>
        <td>xxxxxxxxxxxxxxxxxxx</td>
    </tr>
    
    ...
    
    <tr>
        <td>2020-10-23 xxxxxx</td>
        <td><a href="https://9gag.com/gag/xxxxx" target="_blank">https://9gag.com/gag/xxxxx</a>td>
        <td>xxxxxxxxxxxxxxxxxxx</td>
    </tr>
    
```

Then, we need to isolate a list of post id's :

To do so, open git bash next to the downloaded file and execute with the correct filename (small tip: rename the file without spacesshould be better):

```
sed '/href/!d' FILENAME.html | cut -c 47-53 > data.txt
```

The result will seem like :

```
abGVKAv
aO7DADE
...
```

Finally, replace the project data.txt with the new one you just created.

1. Open a Python cli
2. run `pip install requests` //if not done yet
3. run python3 downloader.py

That's all folks ! Your memes will be downloaded in /data directory
