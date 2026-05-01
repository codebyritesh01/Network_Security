import sys
import os 
import traceback

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.pipline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.responses import RedirectResponse
import pandas as pd

from Network_Security.utils.main_utils.utils import load_object
from Network_Security.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from Network_Security.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from Network_Security.utils.ml_utils.model.estimator import NetworkModel


from Network_Security.utils.ml_utils.feature_extraction import get_features_from_url
from fastapi import Form

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict_single")
async def predict_single(request: Request, url: str = Form(...)):
    try:
        # Extract features from URL
        df = get_features_from_url(url)
        
        # Load model & preprocessor
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        
        # Predict Class and Probability
        y_pred = network_model.predict(df)
        y_proba = network_model.predict_proba(df)
        
        # Calculate Safety Percentage
        prob_safe = y_proba[0][0] 
        percentage = round(prob_safe * 100, 2)
        result = "Safe" if y_pred[0] == -1 or y_pred[0] == 0 else "Phishing"
        
        return {
            "url": url,
            "result": result,
            "percentage": percentage,
            "status": "success"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        df['predicted_column'] = df['predicted_column'].replace(-1, 0)
        # return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        print(table_html)
        return templates.TemplateResponse(request=request, name="table.html", context={"table": table_html, "url": None, "result": None})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

@app.get("/download")
async def download_predict_file():
    try:
        from fastapi.responses import FileResponse
        file_path = "prediction_output/output.csv"
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="text/csv", filename="network_prediction.csv")
        else:
            return Response("Prediction file not found. Please run prediction first.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
if __name__=="__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

