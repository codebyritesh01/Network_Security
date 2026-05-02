from Network_Security.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

import sys

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def predict_proba(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_proba = self.model.predict_proba(x_transform)
            return y_proba
        except Exception as e:
            raise NetworkSecurityException(e, sys)
