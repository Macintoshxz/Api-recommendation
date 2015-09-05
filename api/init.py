from pymongo import MongoClient
import pandas as pd
import codecs

input_file = 'data/2015_02_clickstream.tsv'

with open(input_file, "r") as f:
    tsv = f.readlines()
    
dic_res = {}

for line in tsv:
    l = line.split("\t")
    if l[0]!='':
        if l[3] in dic_res:
            dic_res[l[3]].append({"title":l[4],"score":int(l[2])})
        else:
            dic_res[l[3]] = [{"title":l[4],"score":int(l[2])}]

tsv=[]


client = MongoClient('localhost', 27017)
dbwekey = client.get_database('wekeypedia')

dbwekey.drop_collection('recommendation')
dbwekey.create_collection('recommendation')
clickstream_col = dbwekey.get_collection('recommendation')
print(clickstream_col.count())

for title in dic_res:
    page = { "title":title,
             "links":dic_res[title]}
    clickstream_col.insert_one(page)

print(clickstream_col.count())
