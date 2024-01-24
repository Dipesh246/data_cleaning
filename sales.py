import pandas as pd
from pymongo import MongoClient
import datetime

excel_data = pd.read_excel('D:\Dipesh\practice\data_management\VAT_Sales_Register_Report.xlsx')

new_excel_data=excel_data.drop(range(0,6))
excel_data=new_excel_data.reset_index(drop=True)
excel_data.iloc[0] = excel_data.iloc[0].str.replace(' ','_')
new_columns = excel_data.iloc[0] + '_' + excel_data.iloc[1]
excel_data.columns = new_columns
excel_data=excel_data.drop([0,1])
excel_data=excel_data.drop(excel_data.index[-1])
excel_data.columns=['INVOICE_DATE_AD', 'INVOICE_DATE_BS', 'INVOICE_NO', 'INVOICE_BUYER_NAME', 'INVOICE_BUYER_PAN', 'INVOICE_ITEM_NAME',
       'INVOICE_QTY', 'INVOICE_UNIT', 'TOTAL_SALES/EXPORT_VALUE',  'NON_TAXABLE_SALES_VALUE', 'TAXABLE_SALES_VALUE', 'TAXABLE_SALES_VAT',
       'EXPORT_SALES_VALUE', 'EXPORT_SALES_COUNTRY',
       'EXPORT_SALES_EXPORT_PP_NO', 'EXPORT_SALES_EXPORT_PP_DATE']


try:
    excel_data[['INVOICE_QTY',
                'TOTAL_SALES/EXPORT_VALUE',
                'NON_TAXABLE_SALES_VALUE',
                'TAXABLE_SALES_VALUE',
                'TAXABLE_SALES_VAT',
                'EXPORT_SALES_VALUE']] = excel_data[['INVOICE_QTY',
                                                    'TOTAL_SALES/EXPORT_VALUE',
                                                    'NON_TAXABLE_SALES_VALUE',
                                                    'TAXABLE_SALES_VALUE',
                                                    'TAXABLE_SALES_VAT',
                                                    'EXPORT_SALES_VALUE']].replace({',':''},regex=True).astype(float)
    print(excel_data.dtypes)
except Exception as e:
    print(e)

agg_function = {'INVOICE_DATE_AD':'first',
                'INVOICE_DATE_BS':'first',
                'INVOICE_BUYER_NAME':'first',
                'INVOICE_BUYER_PAN':'first',
                'INVOICE_QTY':'sum',
                'INVOICE_UNIT':'first',
                'TOTAL_SALES/EXPORT_VALUE':'sum',
                'NON_TAXABLE_SALES_VALUE':'sum',
                'TAXABLE_SALES_VALUE':'sum',
                'TAXABLE_SALES_VAT':'sum',
                'EXPORT_SALES_VALUE':'sum',
                'EXPORT_SALES_COUNTRY':'first',
                'EXPORT_SALES_EXPORT_PP_NO':'first',
                'EXPORT_SALES_EXPORT_PP_DATE':'first',
                }
grouped_data= excel_data.groupby('INVOICE_NO').aggregate(agg_function).reset_index()
grouped_data['INVOICE_DATE_BS'] = pd.to_datetime(grouped_data['INVOICE_DATE_BS'], format="%Y.%m.%d").dt.strftime("%Y/%m/%d")

client= MongoClient('mongodb://localhost:27017')
db = client['reports']
collection = db['sales']
collection2= db['invoice_item_detail']

collection.insert_many(grouped_data.to_dict(orient='records'))

columns_to_drop = ['INVOICE_DATE_AD', 'INVOICE_DATE_BS', 'INVOICE_BUYER_NAME', 'INVOICE_BUYER_PAN',]
excel_data = excel_data.drop(columns=columns_to_drop, axis=1)

new_grouped_data = excel_data.groupby(excel_data['INVOICE_NO'])
collection2.insert_many(excel_data.to_dict(orient='records'))

client.close()


