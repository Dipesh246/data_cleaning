import pandas as pd
from pymongo import MongoClient
pd.set_option("display.max_columns",None)

excel_data = pd.read_excel('D:\Dipesh\practice\data_management\VAT_Purchase_Register_Report.xlsx')

new_excel_data=excel_data.drop(range(0,6))
excel_data=new_excel_data.reset_index(drop=True)

excel_data.iloc[0] = excel_data.iloc[0].str.replace(' ','_')
excel_data.columns = excel_data.iloc[0]
excel_data=excel_data.drop([0,])
excel_data=excel_data.drop(excel_data.index[-1])


excel_data[['TOTAL_AMOUNT',
            'NON_TAXABLE_AMOUNT',
            'PURCHASE_AMOUNT',
            'PURCHASE_TAX_AMOUNT',
            'IMPORT_PURCHASE_AMOUNT',
            'CAPITALIZED_PURCHASE_AMOUNT',
            'CAPITALIZED_TAX_AMOUNT']]= excel_data[['TOTAL_AMOUNT',
                                                    'NON_TAXABLE_AMOUNT',
                                                    'PURCHASE_AMOUNT',
                                                    'PURCHASE_TAX_AMOUNT',
                                                    'IMPORT_PURCHASE_AMOUNT',
                                                    'CAPITALIZED_PURCHASE_AMOUNT',
                                                    'CAPITALIZED_TAX_AMOUNT']].replace({',':''},regex=True).astype(float)
# print(excel_data.dtypes)
# setting column names(rename)
excel_data.columns=['ENTRY_DATE_AD',
                    'ENTRY_DATE_BS',
                     'BILL_DATE',
                     'BILL_NO',
                     'SUPPLIER_NAME',
                     'SUPPLIER_PAN',
                     'TOTAL_AMOUNT',
                     'NON_TAXABLE_AMOUNT',
                     'PURCHASE_AMOUNT',
                     'PURCHASE_TAX_AMOUNT',
                     'IMPORT_PURCHASE_AMOUNT',
                     'CAPITALIZED_PURCHASE_AMOUNT',
                     'CAPITALIZED_TAX_AMOUNT',
                     'VOUCHER_NO']
# print(excel_data.head())
#grouping data and adding data of some columns
agg_function = {'TOTAL_AMOUNT':'sum',
                'NON_TAXABLE_AMOUNT':'sum',
                'PURCHASE_AMOUNT':'sum',
                'PURCHASE_TAX_AMOUNT':'sum',
                'IMPORT_PURCHASE_AMOUNT':'sum',
                'CAPITALIZED_PURCHASE_AMOUNT':'sum',
                'CAPITALIZED_TAX_AMOUNT':'sum',               
                }
grouped_data= excel_data.groupby(['SUPPLIER_PAN']).aggregate(agg_function).reset_index()
# print(grouped_data.head())

# print("total amount: ",grouped_data['TOTAL_AMOUNT'])

client= MongoClient('mongodb://localhost:27017')
db = client['reports']
collection = db['purchase']
collection2= db['invoice_item_detail']

collection.insert_many(grouped_data.to_dict(orient='records'))

# columns_to_drop = ['INVOICE_DATE_AD', 'INVOICE_DATE_BS', 'INVOICE_BUYER_NAME', 'INVOICE_BUYER_PAN',]
# excel_data = excel_data.drop(columns=columns_to_drop, axis=1)

# new_grouped_data = excel_data.groupby(excel_data['INVOICE_NO'])
# collection2.insert_many(excel_data.to_dict(orient='records'))

# client.close()