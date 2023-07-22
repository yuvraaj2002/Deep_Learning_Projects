import sys
import os
from src.Logger import logging
from src.Exception import CustomException
from src.Utils import save_object
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
import category_encoders as ce
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf



class Data_Processing:
    def __int__(self):
        self.pipe_path = Data_Processing_Config()

    def Engineer_features(self, df):
        """
        This method will take dataframe as input,add/remove/create features
        will return the new dataframe
        """
        df["month"] = df["DATE"].dt.month
        df["year"] = df["DATE"].dt.year
        df["week"] = df["DATE"].dt.isocalendar().week
        df.drop(["DATE"], axis=1, inplace=True)
        df['RAIN'] = df['RAIN'].astype('object') # Changing the datatype from Booelan to object

        return df

    def Encode_target(self,series):
        """
        This method will take series as input and will encode the boolean values in it
        """
        for i in range(len(series)):
            item = series[i]
            if item == 'True':
                series[i] = 1
            else:
                series[i] = 0
        return series.astype(np.int64)



    def create_dataloaders(self, features_numpy, target_numpy):
        """
        This method will take training features and corresponding features numpy arrays
        and will return tensorflow dataloaders
        """
        # Converting numpy array to TensorFlow tensors
        features_numpy = tf.convert_to_tensor(features_numpy)
        target_numpy = tf.convert_to_tensor(target_numpy)

        # Creation of tensorflow dataset and Set the batch size and shuffle the data
        tf_Dataset = tf.data.Dataset.from_tensor_slices((features_numpy, target_numpy))
        tf_Dataset = tf_Dataset.batch(32).shuffle(True).repeat()

        # iter will help us to iterate over tensorflow dataset in form of batches
        data_loader = iter(tf_Dataset)
        return data_loader


    def Initialize_data_processing(self, train_dp, val_dp):
        try:
            logging.info("Initializing data processing")

            # Let's let's load the data from the files
            train_df = self.Engineer_features(
                pd.read_csv(train_dp,parse_dates=['DATE'])
            )
            val_df = self.Engineer_features(pd.read_csv(val_dp,parse_dates=['DATE']))
            logging.info("Files loaded successfully with feature engineered")

            # Let's build the pipeline
            yeo_john_transformation = ColumnTransformer(
                transformers=[("Yeo_johnson_transformation", PowerTransformer(), [0])],
                remainder="passthrough",
            )

            missing_value_imputer = ColumnTransformer(
                transformers=[("Mean_imputation", SimpleImputer(strategy="mean"), [0])],
                remainder="passthrough",
            )

            nominal_encoding = ColumnTransformer(
                transformers=[
                    (
                        "Target_encode_year",
                        ce.TargetEncoder(smoothing=0.2, handle_missing="return_nan"),
                        [4],
                    )
                ],
                remainder="passthrough",
            )

            feature_scaling = ColumnTransformer(
                transformers=[("Feature_scaling", MinMaxScaler(), [0, 1, 2, 3, 4, 5])],
                remainder="passthrough",
            )

            # Let's build a pipeline
            pipe = Pipeline(
                steps=[
                    ("Yeo-Johnson-Transformation", yeo_john_transformation),
                    ("Nan_Imputation", missing_value_imputer),
                    ("Encoding", nominal_encoding),
                    ("Scaling", feature_scaling),
                ]
            )
            logging.info("Built the pipeline successfully")

            # Let's now process the train and validation data
            X_train = train_df.drop(["RAIN"], axis=1)
            y_train = train_df["RAIN"]
            X_val = val_df.drop(["RAIN"], axis=1)
            y_val = val_df["RAIN"]

            # Imputing the missing values
            rain_imp = SimpleImputer(strategy="most_frequent")
            y_train = rain_imp.fit_transform(y_train.values.reshape(-1, 1)).reshape(-1)
            y_val = rain_imp.fit_transform(y_val.values.reshape(-1, 1)).reshape(-1)
            logging.info("Imputed missing values in the target variable")

            # Encoding the target variable
            y_train = self.Encode_target(y_train)
            y_val = self.Encode_target(y_val)
            logging.info("Target encoding completed")

            #Let's process the training and validation data
            X_train = pipe.fit_transform(X_train, y_train)
            X_val = pipe.transform(X_val)
            logging.info("Training and validation data processed")

            # Let's now save the pipeline
            pipeline_path = os.path.join("Artifacts", "processing_pipe.pkl")
            save_object(file_path=pipeline_path, obj=pipe)
            logging.info("Saved pipeline object")

            # Now we are calling create_dataloader to create data loaders out of Simple numpy arrays
            y_train = y_train.reshape(-1, 1)
            y_val = y_val.reshape(-1, 1)
            train_dataloader = self.create_dataloaders(X_train, y_train)
            val_dataloader = self.create_dataloaders(X_val, y_val)
            logging.info("Train and validation data loaders created")

            return (train_dataloader, val_dataloader)

        except Exception as e:
            raise CustomException(e, sys)
