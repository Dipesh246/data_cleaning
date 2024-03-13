import pandas as pd

df_right = pd.read_csv('item.csv')
df_wrong = pd.read_csv('item(2)FINAL.csv')
print(df_right.columns)
print(df_wrong.columns)
df_wrong.rename(columns = {'name':'Name'}, inplace = True)
merged_df = pd.merge(df_wrong, df_right[['Code','Name']], on='Name', how='left', suffixes=('_wrong','_right'))
merged_df['Code'] = merged_df['Code_right'].fillna(merged_df['Code_wrong'])
merged_df = merged_df.drop(columns=['Code_right'])
merged_df['Code_wrong'] = merged_df['Code']
merged_df = merged_df.drop(columns=['Code'])
merged_df.rename(columns = {'Code_wrong':'Code'}, inplace = True)
merged_df.to_csv('updated_file.csv', index=False)