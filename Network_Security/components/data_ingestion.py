from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

## Configuration of the Data Ingestion Config
from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            # Get database and collection names from config
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            # Create a MongoDB client using the connection URL
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Access the specific collection from the database
            collection = self.mongo_client[database_name][collection_name]

            # Fetch all documents from the collection and convert them into a pandas DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Check if '_id' column exists in the DataFrame
            if "_id" in df.columns.to_list():
                # Drop the '_id' column (MongoDB automatically adds this field)
                df = df.drop(columns=["_id"])

            # Replace string value "na" with actual NaN values for proper data handling
            df.replace({"na": np.nan}, inplace=True)

            # Return the cleaned DataFrame
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def export_data_info_feature_store(self,dataframe: pd.DataFrame):
        try:
            # Get the file path where the feature store CSV will be saved
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # Extract the directory path from the full file path
            dir_path = os.path.dirname(feature_store_file_path)

            # Create the directory if it doesn't already exist
            # exist_ok=True prevents an error if the folder is already present
            os.makedirs(dir_path, exist_ok=True)

            # Save the DataFrame to a CSV file
            # index=True → includes row indices in the file
            # header=True → includes column names as the first row
            dataframe.to_csv(feature_store_file_path, index=True, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_info_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)