import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi #The certify is a Python package that provides a set of root certificates.It is commonly used by Python libraries.That needs to probably make a secure HTTP connection.
ca=certifi.where() #CA = Certificate Authorities


import pandas as pd
import numpy as np
import pymongo

from Network_Security.exception.exception import NetworkSecurityException 
from Network_Security.logging.logger import logging

class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def cv_to_json_converetor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH = os.path.join("Network_Data", "phisingData.csv")
    DATABASE="RITESH"
    Collection="Network Data"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_converetor(file_path=FILE_PATH)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
    