Manufacturing API Project:

Overview

This project provides a RESTful API for predicting machine downtime in a manufacturing setup. It allows users to upload a dataset, train a machine learning model, and make real-time predictions of machine downtime. The API is built using FastAPI and a Logistic Regression model trained with scikit-learn.

Features:

Upload Dataset: Upload manufacturing data in CSV format via the /upload endpoint.
Train the Model: Train a Logistic Regression model to predict machine downtime using the /train endpoint.
Make Predictions: Use the trained model to predict machine downtime via the /predict endpoint.
Performance Metrics: View training metrics like accuracy and F1-score after model training.

Folder Structure:

plaintext
Copy
Edit
manufacturing_api_project/
├── app/
│   ├── __init__.py       # Makes the app folder a package
│   ├── main.py           # FastAPI application
│   ├── data/             # Directory for storing datasets
│   │   └── dataset.csv   # Example manufacturing dataset
│   ├── model/            # Directory for storing the trained model
│       └── model.pkl     # Serialized machine learning model
├── requirements.txt      # Dependencies for the project
├── README.md             # Project documentation
├── .gitignore            # Files and directories to ignore in Git
Dataset Description
The dataset includes information about machine operations and whether downtime occurred. Example columns:

Machine_ID: Unique identifier for each machine.
Temperature: Operational temperature of the machine.
Run_Time: Total runtime of the machine (in hours).
Downtime_Flag: Target column indicating downtime (1 = Yes, 0 = No).
Endpoints
1. POST /upload
Description: Upload a CSV file containing the manufacturing data.
Request Example:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/upload" \
    -F "file=@path_to_your_file.csv"
Response Example:

json
Copy
Edit
{
    "message": "Dataset uploaded successfully",
    "rows": 100,
    "columns": 4
}
2. POST /train
Description: Train a Logistic Regression model using the uploaded dataset.
Request Example:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/train"
Response Example:

json
Copy
Edit
{
    "message": "Model trained successfully",
    "accuracy": 0.85,
    "f1_score": 0.88
}
3. POST /predict
Description: Make predictions for machine downtime using new input data.
Request Example:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"Temperature": 80, "Run_Time": 120}'
Response Example:

json
Copy
Edit
{
    "Downtime": "Yes",
    "Confidence": 0.92
}
How to Set Up the Project
1. Clone the Repository
bash
Copy
Edit
git clone <repository-url>
cd manufacturing_api_project
2. Install Dependencies
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
3. Run the API
Start the FastAPI application:

bash
Copy
Edit
uvicorn app.main:app --reload
The API will be accessible at: http://127.0.0.1:8000

Example Dataset
Here’s an example of the dataset you can use:

csv
Copy
Edit
Machine_ID,Temperature,Run_Time,Downtime_Flag
1,75,100,0
2,80,120,1
3,72,95,0
4,90,150,1
5,65,85,0
Future Improvements
Add support for additional machine learning models (e.g., Decision Trees, Random Forest).
Include more advanced metrics such as Precision, Recall, and ROC-AUC score.
Deploy the API using Docker or a cloud platform like AWS or Heroku.
Acknowledgements
Dataset: Synthetic dataset created for demonstration purposes.
Libraries: FastAPI, scikit-learn, pandas, joblib.
License
This project is licensed under the MIT License. See LICENSE for details.