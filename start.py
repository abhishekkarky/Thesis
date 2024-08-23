from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

scaler = joblib.load('Isolation Standard Scaler.pkl')
model = joblib.load('Isolation Forest Model.pkl')
label_encoder = joblib.load('Label Encoder.pkl')

def preprocess_data(df):
    df = df.drop(columns=['account_id', 'card_id', 'client_id', 'trans_id'])

    df.replace('none', np.nan, inplace=True)
    df['card_type'] = label_encoder.transform(df['card_type'].astype(str))

    df['full_date_card'] = pd.to_datetime(df['full_date_card'], errors='coerce')
    df['year'] = df['full_date_card'].dt.year
    df['month'] = df['full_date_card'].dt.month
    df['day'] = df['full_date_card'].dt.day
    df = df.drop(columns=['full_date_card'])
    df = df.dropna()

    df = pd.get_dummies(df, columns=['sex', 'owner_type', 'transaction_type', 'operation', 'k_symbol'])

    df = df.reindex(columns=model_columns, fill_value=0)

    df_scaled = scaler.transform(df)
    
    return df_scaled

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    df = pd.read_csv(file)

    df_preprocessed = preprocess_data(df)

    predictions = model.predict(df_preprocessed)
    predictions = np.where(predictions == -1, 'Fraud', 'Normal')

    df['Prediction'] = predictions

    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    model_columns = joblib.load('Model Columns.pkl')  
    app.run(debug=True)
