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

# Class for extracting CSV data and storing into MongoDB
class NetworkDataExtract():

    # Constructor runs automatically when object is created
    def __init__(self):
        try:
            # pass means currently no setup code written here
            pass
        except Exception as e:
            # If any error happens, raise custom exception
            raise NetworkSecurityException(e,sys)
        
    # Function to read CSV file and convert data into JSON records
    def cv_to_json_converetor(self,file_path):
        try:
            # Read CSV file into pandas dataframe
            data=pd.read_csv(file_path)

            # Reset index (0,1,2,3...)
            data.reset_index(drop=True,inplace=True)

            # Convert dataframe rows into JSON record format
            # Output becomes list of dictionaries
            records=list(json.loads(data.T.to_json()).values())

            # Return converted records
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    # Function to insert records into MongoDB
    def insert_data_mongodb(self,records,database,collection):
        try:
            # Save values into object variables
            self.database=database
            self.collection=collection
            self.records=records

            # Connect to MongoDB server
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            # Select database
            self.database = self.mongo_client[self.database]

            # Select collection inside database
            self.collection=self.database[self.collection]

            # Insert multiple records
            self.collection.insert_many(self.records)

            # Return total inserted records count
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH = os.path.join("Network_Data", "phisingData.csv")
    DATABASE="RITESH"
    Collection="Network Data"

    # Create object of class
    networkobj=NetworkDataExtract()

    # Convert CSV data into JSON records
    records=networkobj.cv_to_json_converetor(file_path=FILE_PATH)

    # Insert records into MongoDB
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    