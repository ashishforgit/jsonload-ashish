#!/usr/bin/env python

<<<<<<< HEAD
=======

>>>>>>> 94d13e3... Add files via upload
'''
Assumption:
As mentined in the PDF, criteria to mark a user active is
1. event_type is user_engagement.
2. engagement time is at least 3 seconds AND any valuable events occured at least once

Now for the AND condition to be True for any user at a particular day, there should be at least two events
against a user at a particular day, one event of type user_engagement & another any valuable type.

Now given that in the provided json data, At the most only one event exists against each user id,
our result output will be 0 rows.
So, to avoid that, I have made the critera of active user be a user with at least
one event at a particular day of type user_engagement 
'''


'''
Import required libraries
''' 
import json
from datetime import datetime

import pandas as pd

JSON_FILE_LOCATION = r'/path/bq-results-sample-data.json'
OUTPUT_FILE_PATH = r'/path/output.csv'

'''
This function converts the certain type of json we have in our `user_properties' and 'event_params' to dictionary
so that we can get the required data frome it.
''' 
def json_to_dict(js):
    final_dict = {}
    for value in js:
        key = ""
        val = ""
        for k,v in value.items():
            if k == 'key':
                key = v
            else:
                val = list(v.values())[0]
        final_dict[key]=val
    return final_dict

# Read json file in dataframe
df = pd.read_json(path_or_buf=JSON_FILE_LOCATION, lines=True)
# Convert date string to date type
df['event_date'] = [datetime.strptime(str(dt),'%Y%m%d') for dt in df['event_date']]
# Convert event_params json to dictionary.
df['event_params'] = [json_to_dict(dt) for dt in df['event_params']]
# Convert user_properties json to dictionary.
df['user_properties'] = [json_to_dict(dt) for dt in df['user_properties']]
# Filter events where event_name is user_engagement 
df = df[df['event_name'] == 'user_engagement']
# Create a seperate column engagement_time from even_params
df['engagement_time'] = [int(dt['engagement_time_msec']) for dt in df['event_params']]
# Filter user_engagement type events where engagement_time is at least 3 seconds
df = df[df['engagement_time'] >= 3000]
# Now our dataframe has only those events which meet our assumed criteria of identifying a user as active.
# Group events by event_date
df = df.groupby(['event_date'])['user_pseudo_id'].count().to_frame()
# Rename column to active_user_count
df.columns = ['active_user_count']
# Rename index to date
df.index.names = ['date']
# Save output as csv
df.to_csv(OUTPUT_FILE_PATH)

'''
In case you want to write dataframe to sql database.
'''
#from sqlalchemy import create_engine
#engine = create_engine('mysql://user:password@localhost:3306/active_user_table', echo=False)
#df.to_sql('active_user_table', con, flavor='sqlite', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)

