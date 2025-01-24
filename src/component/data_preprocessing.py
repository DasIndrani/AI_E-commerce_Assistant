import os
import sys
import pandas as pd
import numpy as np
from langchain_community.document_loaders import DataFrameLoader
from src.Tools import PreprocessingTools
from src.logger import logging
from src.exception import AIAssistantException

class DataPreprocessing:
    def __init__(self,df):
        try:
            logging.info(f" ***start Data preprocessing*** ")
            self.df = df
        except Exception as e:
            raise AIAssistantException(e,sys)

    def preprocessing(self):
        try:
            logging.info(f"read dataset")
            df = self.df
            df = df.drop(['image','link'], axis=1) 
            print(df.shape)
            logging.info(f"start data cleaning through various steps")
            sub_category=df["sub_category"].unique()

            self.tools = PreprocessingTools()

            logging.info(f"drop unnecessary rows")
            df =self.tools.remove_duplicate(df,"sub_category",sub_category)
            df = self.tools.drop_row(df,'actual_price','₹0')
            df = df.drop(df[(df["name"].apply(lambda x: str(x)[0].isdigit())) & (df["ratings"].isnull()) & (df["discount_price"].isnull())].index).reset_index(drop=True)
            df = df.drop(df[(df["name"].apply(lambda x: str(x)[0].isdigit())) & (df["ratings"].isnull())].index).reset_index(drop=True)
            df = df[((df["sub_category"]!=sub_category[0]) & (df['name'].str.contains(r'\b(Refrigerator|Refrigerators|TV|tv)\b', case=False, na=False))) | ((df["sub_category"]==sub_category[0]) & 
                (df["name"].apply(lambda x:any(substr in str(x) for substr in ["AC","Ac","Air Cooler","Air Conditioner","Fan"]))))].reset_index(drop=True)
            df['no_of_ratings']=df['no_of_ratings'].apply(lambda x:str(x).replace(',', '') if pd.notna(x) else x)
            df['discount_price']=df['discount_price'].apply(lambda x:str(x).replace('₹', '').replace(',','') if pd.notna(x) else x).astype(float)
            df['actual_price']=df['actual_price'].apply(lambda x:str(x).replace('₹', '').replace(',','')if pd.notna(x) else x).astype(float)

            row_to_impute = self.tools.row_mark(df,n=int(df['discount_price'].isnull().sum()),columns='discount_price')
            df.loc[row_to_impute,"discount_price"]=df['discount_price'][row_to_impute].fillna(0.0)
           # print(df.shape,df.isnull().sum())

            list_of_feature = df.columns[0:3].to_list()
            v1_list=df['ratings'].apply(lambda x:x if  str(x).isalnum() or not str(x).isascii() else None).unique()[6:].tolist()
            v2_list = df['no_of_ratings'].apply(lambda x:x if not str(x).isdigit() else None).unique()[2:].tolist()

            logging.info(f"convert non-numerical rating into null value")
            self.tools.conversion(df,'ratings',v1_list)
            self.tools.conversion(df,'no_of_ratings',v2_list)

            #print(df.isnull().sum())

            logging.info(f"convert category value into numerical value and handle missing value")
            self.tools.encoder(df,list_of_feature=list_of_feature)
            df = self.tools.handle_missing_value_by_predicting(df,"sub_category")
            df[list_of_feature] = df[list_of_feature].astype(int)

            self.tools.decoder(df,list_of_feature)

            logging.info(f"Add new feature from existing feature")
            self.tools.add_new_feature_or_value(df,"discount_%",col1='discount_price', col2='actual_price')

            df['ratings']=df['ratings'].round(1)
            df['no_of_ratings']=df['no_of_ratings'].round(0).astype(int)
            df['discount_price']=np.where(df['discount_price']==0.0, None ,df['discount_price'])
            df['discount_price']=df['discount_price'].apply(lambda x:self.tools.add_prefix('₹',x) if x != None else x)
            df['actual_price']=df['actual_price'].apply(lambda x:self.tools.add_prefix('₹',x))
            df=self.tools.remove_duplicate(df,"sub_category",sub_category)
            df.to_csv("cleaned_data.csv",index=True)
        
            logging.info("create a text columns for embedding")
            data = df.copy()
            data['discount_%']=data['discount_%'].astype(int)
            self.tools.complete_sentence(data,'name')
            semi_df1 = data[['ratings', 'no_of_ratings','discount_price','discount_%', 'actual_price']]
            self.tools.add_text(data,data.columns.to_list()[1:])
            data = data[['name','discount_price','discount_%', 'actual_price','ratings', 'no_of_ratings']]
            data['text'] = data.sum(axis=1)
            data= data[["text"]]
            data = pd.concat([data,semi_df1],axis=1)
            print(data.head())
            logging.info("start load documents")
            loader = DataFrameLoader(data, page_content_column="text")
            documents=loader.load()
            logging.info(f"~~~ complete data preprocessing")
        
            return df, documents
        
        except Exception as e:
            raise AIAssistantException(e,sys)



        




       



       

        
