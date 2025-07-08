import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
from langchain_community.vectorstores import FAISS
from src.exception import AIAssistantException
from sklearn.preprocessing import RobustScaler

class PreprocessingTools:
    def __init__(self):
        pass

    def remove_duplicate(self, dataset, feature, list_subcategory):
        try:
            data = pd.DataFrame()
            for sub_category in list_subcategory:
                filter_data = dataset[dataset[feature]==sub_category].drop_duplicates(subset=["name","ratings","no_of_ratings"], keep=False).reset_index(drop=True)
                data = pd.concat([data,filter_data],ignore_index=True)
            return data
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def drop_row(self,data,feature,var:str):
        try:
            return data.drop(data[(data[feature].isna()) | (data[feature]==var)].index).reset_index(drop=True)
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def row_mark(self,dataframe,n:int, columns):
        try:
            null_rows = dataframe[dataframe[columns].isnull()]
            return null_rows.sample(n=n,random_state=1).index
        except Exception as e:
            raise AIAssistantException(e,sys)

    
        
    label_encoders = {}
    def encoder(self,data,list_of_feature:list): 
        try: 
            for i in list_of_feature:
                self.label_encoders[i] = LabelEncoder()
                data[i] = self.label_encoders[i].fit_transform(data[i])
        except Exception as e:
            raise AIAssistantException(e,sys)

    def conversion(self,data,col,var_list):
        try:
            data[col] = data[col].apply(lambda x: None if str(x) in var_list else x)
        except Exception as e:
            raise AIAssistantException(e,sys)
        
    def handle_missing_value_by_predicting(self,dataset,feature):
        try:
            data = pd.DataFrame()
            imputer = IterativeImputer(estimator=RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=42),
                                        initial_strategy='median', max_iter=5, random_state=42)
            for sub_category in dataset["sub_category"].unique().tolist():
                transformed_data = pd.DataFrame(imputer.fit_transform(dataset[dataset[feature]==sub_category]), columns=dataset.columns)
                data = pd.concat([data,transformed_data],ignore_index= True)
            return data
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def decoder(self,data,list_of_feature:list):
        try:
            for i in list_of_feature:
                data[i] = self.label_encoders[i].inverse_transform(data[i])
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def add_new_feature_or_value(self,data,new_featrue:str|None,col1,col2):
        try:
            value1 = (((data[col2]-data[col1])/data[col2])*100).round(0)
            value2 = 0
            if new_featrue:
                data[new_featrue]=np.where((data[col1] < data[col2]) & (data[col1]>0.0),value1,value2).astype(float)
                return data[new_featrue]
            else:
                return value1,value2
        except Exception as e:
            raise AIAssistantException(e,sys)

    def add_prefix(self,prefix,value):
        try:
            return f'{prefix}{value}'
        except Exception as e:
            raise AIAssistantException(e,sys)
 
    

    def complete_sentence(self,df,feature):
        try:
            df[feature]=df[feature].apply(lambda x:' '.join(str(x).split()[:-1]) if str(x).endswith('...') and not str(x).endswith(',...') 
                            else (str(x).replace(',...',' ') if str(x).endswith(',...') else str(x)))
            df[feature]=df[feature].apply(lambda x:str(x) if str(x).endswith(")") else str(x)+")")
        except Exception as e:
            raise AIAssistantException(e,sys)  
        
    def pre_text(self,text):
        try:
            return f'{text}'
        except Exception as e:
            raise AIAssistantException(e,sys)

    def add_text(self,df,feature_name):
        try:
            for feature in feature_name:
                if feature == 'ratings':
                    df[feature] = df[feature].apply(lambda x:self.pre_text(f" It has a {x} stars rating "))
                elif feature == 'no_of_ratings':
                    df[feature] = df[feature].apply(lambda x:self.pre_text(f"from {x} ratings."))
                elif feature == 'actual_price':
                    df[feature] = df.apply(lambda x:self.pre_text(f"on the original price of {x[feature]}.") if x['discount_%']> 0 else
                                self.pre_text(f"and the original price is {x[feature]}."),axis=1)
                elif feature == 'discount_price':
                    df[feature] = df[feature].apply(lambda x:self.pre_text(f", is available for {x} after a ") if pd.notna(x) else self.pre_text(f" has no discount available,"))
                elif feature == 'discount_%':
                    df[feature] = df[feature].apply(lambda x:self.pre_text(f"{x}% discount ") if x>0 else self.pre_text(f" so the discount is {x}%, "))
        except Exception as e:
            raise AIAssistantException(e,sys)
        
    def recommend(self,retrieved_docs):
        try:
            rating_weight=0.3
            no_of_ratings_weight = 0.7
            ratings = [float(doc.metadata["ratings"]) for doc in retrieved_docs]
            no_of_ratings = [float(doc.metadata["no_of_ratings"]) for doc in retrieved_docs]

            # Combine into a 2D array for scaling
            metadata_array = np.array([ratings, no_of_ratings]).T

            # Step 3: Fit and transform with RobustScaler
            scaler = RobustScaler()
            scaled_metadata = scaler.fit_transform(metadata_array)

            # Step 4: Apply formula using scaled values
            for idx, doc in enumerate(retrieved_docs):
                new_ratings, new_no_of_ratings= scaled_metadata[idx]
                ratings, no_of_ratings = scaled_metadata[idx]
                if doc.metadata["ratings"]<4.4:
                    score1 = (rating_weight * new_ratings) + (no_of_ratings_weight * new_no_of_ratings)
                    doc.metadata['score1'] = score1
                else:
                    score1 = 0.0
                    doc.metadata['score1'] = score1

                if doc.metadata["ratings"]>=4.4:
                    score2 = np.sqrt(np.square(ratings)+np.square(no_of_ratings))
                    doc.metadata['score2'] = score2
                else:
                    score2 = 0.0
                    doc.metadata['score2'] = score2

            sorted_docs1 = sorted(retrieved_docs, key=lambda doc: doc.metadata['score1'],reverse=True)[:7]
            sorted_docs2 = sorted(retrieved_docs, key=lambda doc: doc.metadata['score2'],reverse=True)[:7]

            filter_doc = []
            for doc in sorted_docs1:
                if (doc.metadata["ratings"]<4.4) & (doc.metadata["ratings"]>=3.9):
                    filter_doc.append(doc)
            for doc in sorted_docs2:
                if (doc.metadata["ratings"]>=4.4) & (doc.metadata["no_of_ratings"]>=10):
                    filter_doc.append(doc)
            return filter_doc

        except Exception as e:
                raise AIAssistantException(e,sys)



        
    

