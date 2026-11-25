"""
Interactive Customer Churn Prediction CLI
Customer Churn Prediction & Business Analytics
Author: Data Science Apprentice
"""

import sys
import os
import joblib
import pandas as pd

def load_pipeline(model_path="models/churn_model.pkl"):
    """Load the trained model pipeline."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    return joblib.load(model_path)

def predict_single_customer(model, customer_dict):
    """
    Given a customer feature dictionary, return the binary churn prediction
    and continuous churn probability.
    """
    df = pd.DataFrame([customer_dict])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0, 1]
    
    if prob >= 0.70:
        tier = "CRITICAL RISK"
        color_flag = "🚨"
    elif prob >= 0.40:
        tier = "ELEVATED RISK"
        color_flag = "⚠️"
    else:
        tier = "LOW RISK"
        color_flag = "✅"
        
    return {
        'prediction': 'WILL CHURN' if pred == 1 else 'RETAINED',
        'churn_probability_pct': round(prob * 100, 2),
        'risk_tier': tier,
        'flag': color_flag
    }

def run_demo():
    print("=" * 70)
    print("🎯 Customer Churn Prediction Engine - Interactive Demo")
    print("=" * 70)
    
    model = load_pipeline()
    print("Production model successfully loaded from models/churn_model.pkl\n")
    
    # Pre-set test profiles representing key personas
    profiles = [
        {
            'name': 'Persona 1: High-Risk New Subscriber (Fiber + Electronic Check + Month-to-Month)',
            'data': {
                'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
                'tenure': 2, 'PhoneService': 'Yes', 'MultipleLines': 'No',
                'InternetService': 'Fiber optic', 'OnlineSecurity': 'No', 'OnlineBackup': 'No',
                'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'Yes', 'StreamingMovies': 'Yes',
                'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes', 'PaymentMethod': 'Electronic check',
                'MonthlyCharges': 95.50, 'TotalCharges': 191.00
            }
        },
        {
            'name': 'Persona 2: Loyal Long-Tenure Subscriber (DSL + Tech Support + Two-Year Contract)',
            'data': {
                'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
                'tenure': 60, 'PhoneService': 'Yes', 'MultipleLines': 'Yes',
                'InternetService': 'DSL', 'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes',
                'DeviceProtection': 'Yes', 'TechSupport': 'Yes', 'StreamingTV': 'No', 'StreamingMovies': 'No',
                'Contract': 'Two year', 'PaperlessBilling': 'No', 'PaymentMethod': 'Credit card (automatic)',
                'MonthlyCharges': 65.20, 'TotalCharges': 3912.00
            }
        },
        {
            'name': 'Persona 3: Moderate-Risk Mid-Tenure Fiber Customer with Online Security',
            'data': {
                'gender': 'Male', 'SeniorCitizen': 1, 'Partner': 'No', 'Dependents': 'No',
                'tenure': 18, 'PhoneService': 'Yes', 'MultipleLines': 'Yes',
                'InternetService': 'Fiber optic', 'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes',
                'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'Yes', 'StreamingMovies': 'No',
                'Contract': 'One year', 'PaperlessBilling': 'Yes', 'PaymentMethod': 'Bank transfer (automatic)',
                'MonthlyCharges': 84.50, 'TotalCharges': 1521.00
            }
        }
    ]
    
    for item in profiles:
        print(f"📋 {item['name']}")
        res = predict_single_customer(model, item['data'])
        print(f"   Contract: {item['data']['Contract']} | Internet: {item['data']['InternetService']} | Tenure: {item['data']['tenure']} mo")
        print(f"   Monthly Bill: ${item['data']['MonthlyCharges']} | Payment: {item['data']['PaymentMethod']}")
        print(f"   {res['flag']} Result: {res['prediction']} ({res['churn_probability_pct']}% Churn Probability) -> [{res['risk_tier']}]")
        print("-" * 70)

if __name__ == "__main__":
    run_demo()
