import pandas as pd
import datetime
import json
import csv
import requests
import time

'''Gets data from PushShift'''
def getPushshiftData(query, after, before, sub):

    url = 'https://api.pushshift.io/reddit/search/comment/?q='+str(query)+'&subreddit='+str(sub)+'&after='+str(after)+'&before='+str(before)+'&size='+str(size)
    print('------------------------------------------------')
    try:
        data = requests.get(url).json()
    except json.decoder.JSONDecodeError:
        return None
    return data['data']

''' Collects comment data'''
def collectSubData(subm):
    subData = list() #list to store data points
    body = subm['body']
    author = subm['author']
    id = subm['id']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    score = subm['score']

    subData.append((body, author, id, created, score))
    subStats[id] = subData

'''Writes csv file'''
def updateSubs_file():
    upload_count = 0
    location = "/Users/anand/Documents/policygenius/reddit/data/"
    # print("input filename of submission file, please add .csv")
    # filename = input()
    filename = 'Insurance_comments.csv'
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["body", "Author", "ID", "Created", "score"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
        print(str(upload_count) + " submissions have been uploaded")

'''Variables'''
sub='insurance'       # Subreddit to query
before = "1577836800" # 01/01/2020
after = "1420070400"  # 01/01/2015
query = "a"
size = 100
subCount = 0          # Tracks the number of total submission collected
subStats = {}         # Dictionary where data is stored
errorCount  = 0       # Tracks total errors

data = getPushshiftData(query, after, before, sub)

'''Will run until all comments have been gathered'''
while len(data) > 1:
    if data != [0,0] and data != None:
        for submission in data:
            collectSubData(submission)
            subCount+=1
        print(len(data))
        print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
    else:
        continue
    data = getPushshiftData(query, after, before, sub)
    if data is None:
        errorCount += 1
        print('********ERROR!!!******** # {}'.format(errorCount))
        data = [0,0]
        continue

print(len(data))
print('Total erros: {}'.format(errorCount))
print(str(len(subStats)) + " submissions have added to list")
print("1st entry by:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][3]))
print("Last entry by:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][3]))
updateSubs_file()
