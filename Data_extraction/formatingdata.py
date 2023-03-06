import pandas as pd
import numpy as np

emp_df = pd.read_csv('emergencyplus.csv')
hjelp_df = pd.read_csv('hjelp113.csv')
sos_df = pd.read_csv('sosalarm.csv')
suomi_df = pd.read_csv('suomi112.csv')

combined_df = pd.concat([emp_df,hjelp_df,sos_df,suomi_df])

nan_index_list = list(combined_df.loc[pd.isna(combined_df["Review"]), :].index)

non_nan_combined_df = combined_df.drop(nan_index_list,axis=0)

non_nan_combined_df.to_csv('user_review_data.csv',index=False)

print("File created!!")