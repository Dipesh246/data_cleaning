import pandas as pd
# from pymongo import MongoClient
pd.set_option("display.max_columns",None)

def extract_data(data_file):
    # excel_data = pd.read_excel('D:\Dipesh\practice\data_management\VAT_Purchase_Register_Report.xlsx')
    # file_format = data_file.name.split('.')[-1].lower()
    file_format = data_file.split('.')[-1].lower()

    if file_format=='xlsx':
        excel_data = pd.read_excel(data_file)
    elif file_format == 'csv':
        excel_data = pd.read_csv(data_file)
    else:
        return 'file not supported' 



    new_excel_data=excel_data.drop(columns=["GEN Price"])
    string_columns = ['Batch No.', 'Exp Date', 'Qty']
    new_excel_data[string_columns] = new_excel_data[string_columns].astype(str)
    df1 = new_excel_data.assign(**{col: new_excel_data[col].str.split(',') for col in string_columns}).explode(['Batch No.', 'Exp Date', 'Qty'])
    df1.columns = df1.columns.str.replace(" ", "_")
    # integer_columns = ['Qty','Purchase_Cost']
    df1['Qty'] = pd.to_numeric(df1['Qty'], errors= 'coerce')
    
    df1 = df1[df1['Qty'] != 0].dropna().reset_index()
    total_qty = df1['Qty'].sum()
    total_purchase_cost = df1['Purchase_Cost'].sum()
    # print("total_qty, total_purchase_cost")
    # new_excel_file = df1.to_csv("new_file.csv")
    cleaned_excel_data = df1.to_dict("records")  
    grand_total = 0     
    for indiv_data in cleaned_excel_data:
        sub_total = indiv_data['Qty']*indiv_data['Purchase_Cost']
        grand_total += sub_total 
    print(grand_total)
        # if not new_excel_data["Batch No."].dropna().empty: 
        #     print(new_excel_data["Batch No."])
        # excel_data=new_excel_data.reset_index(drop=True)

    # excel_data.iloc[0] = excel_data.iloc[0].str.replace(' ','_')
    # excel_data.columns = excel_data.iloc[0]
    # excel_data=excel_data.drop([0,])
    # excel_data=excel_data.drop(excel_data.index[-1])


    # excel_data[['TOTAL_AMOUNT',
    #             'NON_TAXABLE_AMOUNT',
    #             'PURCHASE_AMOUNT',
    #             'PURCHASE_TAX_AMOUNT',
    #             'IMPORT_PURCHASE_AMOUNT',
    #             'CAPITALIZED_PURCHASE_AMOUNT',
    #             'CAPITALIZED_TAX_AMOUNT']]= excel_data[['TOTAL_AMOUNT',
    #                                                     'NON_TAXABLE_AMOUNT',
    #                                                     'PURCHASE_AMOUNT',
    #                                                     'PURCHASE_TAX_AMOUNT',
    #                                                     'IMPORT_PURCHASE_AMOUNT',
    #                                                     'CAPITALIZED_PURCHASE_AMOUNT',
    #                                                     'CAPITALIZED_TAX_AMOUNT']].replace({',':''},regex=True).astype(float)
    # print(excel_data.dtypes)
    # setting column names(rename)
    # excel_data.columns=['ENTRY_DATE_AD',
    #                     'ENTRY_DATE_BS',
    #                     'BILL_DATE_BS',
    #                     'BILL_NO',
    #                     'SUPPLIER_NAME',
    #                     'SUPPLIER_PAN',
    #                     'TOTAL_AMOUNT',
    #                     'NON_TAXABLE_AMOUNT',
    #                     'PURCHASE_AMOUNT',
    #                     'PURCHASE_TAX_AMOUNT',
    #                     'IMPORT_PURCHASE_AMOUNT',
    #                     'CAPITALIZED_PURCHASE_AMOUNT',
    #                     'CAPITALIZED_TAX_AMOUNT',
    #                     'VOUCHER_NO']
    # # print(excel_data.head())
    # #grouping data and adding data of some columns
    # agg_function = {'TOTAL_AMOUNT':'sum',
    #                 'NON_TAXABLE_AMOUNT':'sum',
    #                 'PURCHASE_AMOUNT':'sum',
    #                 'PURCHASE_TAX_AMOUNT':'sum',
    #                 'IMPORT_PURCHASE_AMOUNT':'sum',
    #                 'CAPITALIZED_PURCHASE_AMOUNT':'sum',
    #                 'CAPITALIZED_TAX_AMOUNT':'sum',               
    #                 }
    # grouped_data= excel_data.groupby(['SUPPLIER_PAN']).aggregate(agg_function).reset_index()
    # # print(grouped_data.head())
    # columns_to_drop = ['SUPPLIER_NAME','SUPPLIER_PAN',]
    # detail_excel_data = excel_data.drop(columns=columns_to_drop, axis=1)
    # data = {"grouped_data":grouped_data.to_dict(orient='records'),
    #         "detail_data":detail_excel_data.to_dict(orient='records'),}
    
    # return data


# print("total amount: ",grouped_data['TOTAL_AMOUNT'])

# client= MongoClient('mongodb://localhost:27017')
# db = client['reports']
# collection = db['purchase']
# collection2= db['invoice_item_detail']

# collection.insert_many(grouped_data.to_dict(orient='records'))



# new_grouped_data = excel_data.groupby(excel_data['INVOICE_NO'])
# collection2.insert_many(excel_data.to_dict(orient='records'))

# client.close()
data = 'D:\Dipesh\practice\data_management\data_cleaning\StoreInv_final_rate.csv'
extract_data(data)