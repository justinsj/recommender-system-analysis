from cmath import nan
import pandas as pd
from datetime import datetime
import math

filename = 'results.csv'


def load_data(only_keep_user_ids=[]):
  '''
  Returns a dataframe of the data.

  load_data: None -> DataFrame
  '''
  df = pd.read_csv(filename)
  return df[df['userId'].isin(only_keep_user_ids)]

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

def df_agg(df, groupby, aggregator, aggregator_key='agg'):
  '''
  Returns a DataFrame that performs .groupby() on df using
  the list of column names groupby, then aggregates 
  the grouped dataframes using agg in column named by aggregator_key.

  df_agg: DataFrame (list Str) (func DataFrame) [Str] -> DataFrame 
  '''
  
  grouped_df = df.groupby(groupby)

  # Initialize results with groupby keys
  results = {}
  for key in groupby:
    results[key] = []

  # Add aggregator_key as the aggregator result key
  results[aggregator_key] = []
  
  for name, group in grouped_df:
    print('name:',name)
    # Add name keys to results
    for i in range(len(groupby)):
      key = groupby[i]
      results[key].append(name[i])
    # Add aggregated value
    results[aggregator_key].append(aggregator(group))

  results_df = pd.DataFrame(results)

  return results_df

def df_deltas(
    df, 
    groupby,  
    delta_func,
    control_key = 'interfaceId',
    delta_key = 'delta', 
  ):
  '''
  Returns a DataFrame that performs .groupby() on df using
  the list of column names groupby, then calculates the delta value 
  placed in the delta_key column using delta_func and the control_key 
  as the source of the control value.

  df_agg: DataFrame (listof Str) (func DataFrame -> DataFrame) [Str Str Str Str] -> DataFrame 
  '''
  grouped_df = df.groupby(groupby)

  # Initialize results with groupby keys
  results = {}
  for key in groupby:
    results[key] = []
  # Add control_key 
  results[control_key] = []
  # Add delta_key as the delta result key
  results[delta_key] = []
  
  for name, group in grouped_df:
    delta_df = delta_func(group)
    for index, row in delta_df.iterrows():
      # Add name keys to results
      for i in range(len(groupby)):
        key = groupby[i]
        results[key].append(name[i])
      # Add control key
      results[control_key].append(row[control_key])
      
      # Add delta value
      results[delta_key].append(row[delta_key])

  results_df = pd.DataFrame(results)

  return results_df
def tct_agg(df, required_count = 3):
  '''
  Returns the task completion time (TCT) in seconds of the dataframe.
  The TCT is determined by the timestamp from the earliest entry
  to the first entry with addedItemsCount equal to the required_count.

  tct_agg: DataFrame [Nat] -> (anyof Float NaN)

  Requires:
  - length of df > 0
  - required_count > 0
  '''

  if (df.shape[0] == 0): raise Exception('tct_agg requires df.shape[0] > 0');

  starting_ts = min(df['ts'])

  df_with_required_count = df[df['addedItemsCount'] == required_count]

  if (df_with_required_count.shape[0] == 0):
    return math.nan

  # The first of the entries with valid required count is the end of the task
  ending_ts = min(df_with_required_count['ts']) 

  return (parse_date(ending_ts) - parse_date(starting_ts)).total_seconds()
def get_individual_tcts(df):
  '''
  Returns a DataFrame with rows of primary keys
  (userId, taskId, interfaceId, sessionId) and values of
  task completion time in seconds from df.
  The 'agg' column is NaN if the task was not completed.

  get_individual_tct: pandas.core.groupby -> DataFrame 
  '''

  results_df = df_agg(
    df, 
    ['userId','sessionId','taskId','interfaceId'],
    tct_agg
  )

  return results_df

def ctr_agg(df):
  '''
  Aggregator for click-through-rate. 
  Uses passed DataFrame df.

  Requires: 
  - x is the pandas data from the .agg() function.

  ctr_agg: DataFrame -> Float
  '''
  clicked_df = df[df['action'] == 'clicked']

  viewed_df = df[df['action'] == 'viewed']

  print('clicked:',clicked_df)
  print('viewed:',viewed_df)

  return clicked_df['productId'].nunique() / (viewed_df['productId'].nunique() if viewed_df['productId'].nunique() else 1)

def get_individual_ctrs(df):
  '''
  Returns a DataFrame with rows of primary keys
  (userId, taskId, interfaceId, sessionId, productId) and values of
  click through rate (CTR) from grouped_df.

  get_individual_tct: pandas.core.groupby -> DataFrame 
  '''

  results_df = df_agg(
    df, 
    ['userId','sessionId','taskId','interfaceId'],
    ctr_agg  
  )
  return results_df

def get_tct(df):

  pass

def get_ctr(df):
  pass


def get_per_user_deltas(
    df, 
    target_control_key='interfaceId', 
    target_control_value='control', 
    aggregator_key = 'agg', 
    aggregator_result_key = 'delta'
  ):
  '''
  Returns a new DataFrame copy of df 
  with control value from target_control_key column being target_control_value
  and deltas calculated from the aggregator_key column to the control value
  and placed in the aggregator_result_key column.

  get_per_user_deltas: DataFrame [Str Str Str Str] -> DataFrame
  '''

  results_df = df.copy()
  results_df[aggregator_result_key] = math.nan

  control_df = df[df[target_control_key] == target_control_value]
  if (control_df.shape[0] != 1): return results_df

  control_value = control_df[aggregator_key].iloc[0]

  results_df[aggregator_result_key] = control_value
  results_df[aggregator_result_key] = results_df[aggregator_key] - results_df[aggregator_result_key]

  return results_df

def df_average(df, groupby = ['interfaceId'], delta_key = 'delta', final_key = 'delta'):
  '''
  Returns the average of the delta_key 
  column in the DataFrame df when grouped by groupby.

  df_average: DataFrame (listof Str) -> DataFrame
  '''
  results_df = df.dropna().groupby(groupby)[delta_key].mean().reset_index(name = final_key)
  return results_df

def df_filter(df, key='interfaceId', value='control'):
  return df[df[key] == value]


only_keep_user_ids = ['assk7FcTldFosGOT','ZmwCehMEVYkTvABc','aqIOl5vBVyiHztIx','zyRP3dxISmkr5zwg','dCZE5sHjyiP6zbsD','SMio6cRqi7sBGQyM','YwpjnVGQgvFPY69O','nsDMkeorNmwrIdDo','ZiCWEvAAgAiX8RZA','GXHqjkEnuiMvPoRN']

df = load_data(only_keep_user_ids)
# userId, ts, taskId, interfaceId, sessionId, productId, action, addedItemsCount

individual_ctrs = get_individual_ctrs(df)
individual_tcts = get_individual_tcts(df)

for name, group in individual_ctrs.groupby(['userId','sessionId','taskId']):
  print("name:", name, "\n", group, "\n\n")

per_user_deltas_ctrs = df_deltas(
  individual_ctrs,
  ['userId','sessionId','taskId'],
  get_per_user_deltas,
)

per_user_deltas_tcts = df_deltas(
  individual_tcts,
  ['userId','sessionId','taskId'],
  get_per_user_deltas,
)
print('per_user_deltas_ctrs:\n', per_user_deltas_ctrs)
print('per_user_deltas_tcts:\n', per_user_deltas_tcts)

# interfaceId, delta
average_ctrs_df = df_average(per_user_deltas_ctrs, final_key = 'ctr')
average_tcts_df = df_average(per_user_deltas_tcts, final_key = 'tct')
print("average_ctrs_df:\n", average_ctrs_df)
print("average_tcts_df:\n", average_tcts_df)

average_ctrs_df.to_csv('average_ctrs.csv', index=False)
average_tcts_df.to_csv('average_tcts.csv', index=False)

control_ctrs = df_filter(individual_ctrs)
control_tcts = df_filter(individual_tcts)

print('average ctr: ', control_ctrs['agg'].mean())
print('average tct: ', control_tcts['agg'].mean())
# average_ctrs_df = df_average(individual_ctrs, final_key = 'ctr')
# average_tcts_df = df_average(individual_tcts, final_key = 'tct')
# print("average_ctrs_df:\n", average_ctrs_df)
# print("average_tcts_df:\n", average_tcts_df)