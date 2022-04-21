import pandas as pd
from datetime import datetime
import math

filename = 'results.csv'

def load_data():
  '''
  Returns a dataframe of the data.

  load_data: None -> DataFrame
  '''
  return pd.read_csv(filename)

# TODO not just use max(x), need first addedItemsCount to be 3 (a constant)
def get_individual_tct(grouped_df):
  '''
  Returns a DataFrame with rows of primary keys
  (userId, taskId, interfaceId, sessionId) and values of
  task completion time (timeDeltas) from grouped_df.

  get_individual_tct: pandas.core.groupby -> DataFrame 
  '''
  return grouped_df['ts'].agg([lambda x: (parse_date(max(x)) - parse_date(min(x)))])

def get_individual_ctr(grouped_df):
  '''
  Returns a DataFrame with rows of primary keys
  (userId, taskId, interfaceId, sessionId, productId) and values of
  click through rate (CTR) from grouped_df.

  get_individual_tct: pandas.core.groupby -> DataFrame 
  '''

  return grouped_df
def get_tct(df):

  pass

def get_ctr(df):
  pass


def fix_iso_date(date):
  '''
  Returns a string replacing Z to 000 to fix 
  YYYY-mm-DDTHH:MM:SS.mmmZ format to
  YYYY-mm-DDTHH:MM:SS.uuuuuu format

  fix_iso_date: Str -> Str
  '''
  return date.replace('Z','000')

def parse_date(date):
  '''
  Parses an ISO8601 formatted date string
  and returns the DateTime

  parse_date: Str -> DateTime
  '''
  return datetime.fromisoformat(fix_iso_date(date))

# 

def ctr_agg(df):
  '''
  Aggregator for click-through-rate. 
  Uses passed DataFrame df.

  Requires: 
  - x is the pandas data from the .agg() function.

  ctr_agg: DataFrame -> Float
  '''
  print("Df:",df)
  clicked_df = df[df['action'] == 'click']

  viewed_df = df[df['action'] == 'view']


  return clicked_df['productId'].nunique() / (viewed_df['productId'].nunique() if viewed_df['productId'].nunique() else 1)

df = load_data()
# userId, ts, taskId, interfaceId, sessionId, productId, action, addedItemsCount

# Group by userId, taskId, interfaceId, sessionId
# grouped_df = df.groupby(['userId','sessionId','taskId','interfaceId'])
# grouped_df['ts'].agg([lambda x: (parse_date(max(x)) - parse_date(min(x)))])

ctrs = df.groupby(['userId','sessionId','taskId','interfaceId']).groupby(['productId'])

# Calculate view times per productId
#

# Calculate dwell times per productId

# For each user, calculate CTR of 