from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import joblib
import os

# Initialize the FastAPI app
app = FastAPI()

# Paths for data and model
DATA_PATH = "app/data/desired_manufacturing_dataset.csv"
MODEL_PATH = "app/model/logistic_model.pkl"

# Endpoint: Upload the dataset
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "wb") as f:
            f.write(file.file.read())
        
        # Verify dataset structure
        data = pd.read_csv(DATA_PATH)
        expected_columns = {"Machine_ID", "Temperature", "Run_Time", "Downtime_Flag"}
        if not expected_columns.issubset(data.columns):
            return {"error": f"Dataset must contain columns: {expected_columns}"}
        
        return {"message": "File uploaded successfully.", "columns": list(data.columns), "rows": len(data)}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Train the model
@app.post("/train")
def train_model():
    try:
        # Load the dataset
        if not os.path.exists(DATA_PATH):
            return {"error": "Dataset not found. Please upload a dataset first."}
        
        data = pd.read_csv(DATA_PATH)
        X = data[["Temperature", "Run_Time"]]
        y = data["Downtime_Flag"]

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Logistic Regression model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Save the trained model
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        return {
            "message": "Model trained successfully.",
            "accuracy": accuracy,
            "f1_score": f1
        }
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Predict using the model
class PredictRequest(BaseModel):
    Temperature: float
    Run_Time: float

@app.post("/predict")
def predict_downtime(request: PredictRequest):
    try:
        # Load the model
        if not os.path.exists(MODEL_PATH):
            return {"error": "Model not trained yet. Please train the model first."}

        model = joblib.load(MODEL_PATH)

        # Prepare input data
        input_data = [[request.Temperature, request.Run_Time]]

        # Make prediction
        prediction = model.predict(input_data)
        confidence = model.predict_proba(input_data).max()

        downtime = "Yes" if prediction[0] == 1 else "No"
        return {
            "Downtime": downtime,
            "Confidence": round(confidence, 2)
        }
    except Exception as e:
        return {"error": str(e)}
