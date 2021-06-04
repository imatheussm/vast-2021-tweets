import pandas as pd
from datetime import datetime
import json

data = pd.read_csv('processed/full.csv')

data['time'] = data['date(yyyyMMddHHmmss)'].apply(lambda t : datetime.strptime(str(t),'%Y%m%d%H%M%S').strftime("%Y-%m-%dT%H:%M:%S"))
data = data\
    .drop(['longitude','latitude','Unnamed: 0.1','Unnamed: 0', 'date(yyyyMMddHHmmss)'], axis='columns')\
    .rename(columns={' location' : 'location'})

res = []

for index, row in data.iterrows():

    if row.type == 'ccdata':
        case = []
        for i in range(index - 2, index): case.append(data.iloc[i].to_dict())
        for i in range(index + 1, index + 3): case.append(data.iloc[i].to_dict())
        res.append(case)

fp = open('processed/neighbors.json', 'w')
json.dump(res, fp)
fp.close()