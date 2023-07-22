import os
import sys
from src.Logger import logging
from src.Exception import CustomException
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class Data_Ingestion_Config:
    train_data_path = os.path.join('Artifacts','train.csv')
    test_data_path = os.path.join('Artifacts','test.csv')
    val_data_path = os.path.join('Artifacts','val.csv')


class Data_Ingestion:

    def __init__(self):
        self.storage_paths = Data_Ingestion_Config()

    def Initialize_data_ingestion(self,raw_data_path):
        """
        This method will take raw data path as input and
        will return the paths of the (train,test and validation csv files
        """
        try:
            logging.info("Initializing data ingestion process")

            # First we will load the raw data from csv file
            raw_df = pd.read_csv(raw_data_path)
            logging.info("Raw data csv file loaded")

            # Now we will do the train,test and validation split
            train_data,test_val_data = train_test_split(raw_df,test_size=0.2, random_state=42)
            test_data,val_data = train_test_split(test_val_data, test_size=0.5, random_state=42)
            logging.info("Train, test and validation split completed")

            # Let's now create Artifacts directory to store the data
            os.makedirs(os.path.dirname(self.storage_paths.train_data_path),exist_ok=True)

            # Let's now store the files
            train_data.to_csv(self.storage_paths.train_data_path, index=False, header=True)
            test_data.to_csv(self.storage_paths.test_data_path, index=False, header=True)
            val_data.to_csv(self.storage_paths.val_data_path, index=False, header=True)
            logging.info("Files saved")

            logging.info("Data Ingestion completed")
            return (
                self.storage_paths.train_data_path,
                self.storage_paths.test_data_path,
                self.storage_paths.val_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":

    data_ingestion_obj = Data_Ingestion()
    data_ingestion_obj.Initialize_data_ingestion('Notebook/data.csv')
