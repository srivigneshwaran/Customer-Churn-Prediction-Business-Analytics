"""
Automated SQL Test Runner & Reporting Script
Executes all business analytics queries in sql/customer_analysis.sql against SQLite/MySQL.
Author: Data Science Apprentice
"""

import sqlite3
import pandas as pd
import os

def run_sql_analytics():
    csv_path = 'data/cleaned_telco_churn.csv'
    if not os.path.exists(csv_path):
        csv_path = '../data/cleaned_telco_churn.csv'
        
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path} for SQL Database Ingestion.")
    
    # Create SQLite database connection
    conn = sqlite3.connect(':memory:')
    df.to_sql('customer_churn', conn, if_exists='replace', index=False)
    print("Database table `customer_churn` initialized successfully in SQL engine.\n")
    
    queries = [
        ("Query 1: Executive KPI Summary (Total Customers, Churned, Churn Rate)", """
        SELECT 
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS total_churned,
            SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS total_retained,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS overall_churn_rate_pct,
            ROUND(SUM(MonthlyCharges), 2) AS total_mrr_all_customers,
            ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS active_mrr
        FROM customer_churn;
        """),
        
        ("Query 2: Customers Grouped by Contract Type", """
        SELECT 
            Contract,
            COUNT(*) AS customer_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_churn), 2) AS pct_of_customer_base,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
        FROM customer_churn
        GROUP BY Contract
        ORDER BY churn_rate_pct DESC;
        """),
        
        ("Query 3: Average Monthly Charges by Churn Status & Contract Type", """
        SELECT 
            Contract,
            Churn,
            COUNT(*) AS customer_count,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(MIN(MonthlyCharges), 2) AS min_monthly_charges,
            ROUND(MAX(MonthlyCharges), 2) AS max_monthly_charges,
            ROUND(AVG(TotalCharges), 2) AS avg_lifetime_charges,
            ROUND(AVG(tenure), 1) AS avg_tenure_months
        FROM customer_churn
        GROUP BY Contract, Churn
        ORDER BY Contract, Churn DESC;
        """),
        
        ("Query 4: Customer Churn Percentage by Payment Method", """
        SELECT 
            PaymentMethod,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue
        FROM customer_churn
        GROUP BY PaymentMethod
        ORDER BY churn_rate_pct DESC;
        """),
        
        ("Query 5: Total Revenue Comparison: Active vs Churned Customers", """
        SELECT 
            Churn AS customer_status,
            COUNT(*) AS customer_count,
            ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_contribution,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge_per_customer,
            ROUND(SUM(TotalCharges), 2) AS total_lifetime_revenue,
            ROUND(AVG(TotalCharges), 2) AS avg_lifetime_revenue_per_customer,
            ROUND(SUM(MonthlyCharges) * 100.0 / (SELECT SUM(MonthlyCharges) FROM customer_churn), 2) AS pct_of_monthly_revenue
        FROM customer_churn
        GROUP BY Churn;
        """),
        
        ("Query 6: Churn Breakdown by Internet Service and Tech Support", """
        SELECT 
            InternetService,
            TechSupport,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge
        FROM customer_churn
        GROUP BY InternetService, TechSupport
        ORDER BY InternetService, churn_rate_pct DESC;
        """),
        
        ("Query 7: Tenure Cohort Retention Analysis", """
        SELECT 
            CASE 
                WHEN tenure <= 12 THEN '01. 0 - 12 Months'
                WHEN tenure <= 24 THEN '02. 13 - 24 Months'
                WHEN tenure <= 36 THEN '03. 25 - 36 Months'
                WHEN tenure <= 48 THEN '04. 37 - 48 Months'
                WHEN tenure <= 60 THEN '05. 49 - 60 Months'
                ELSE '06. 61 - 72 Months'
            END AS tenure_cohort,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(SUM(MonthlyCharges), 2) AS cohort_monthly_revenue
        FROM customer_churn
        GROUP BY tenure_cohort
        ORDER BY tenure_cohort;
        """),
        
        ("Query 8: High-Risk Customer Cohort Identification", """
        SELECT 
            COUNT(*) AS high_risk_customer_count,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS cohort_churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue_at_risk,
            ROUND(SUM(MonthlyCharges) * 12, 2) AS annualized_revenue_at_risk
        FROM customer_churn
        WHERE Contract = 'Month-to-month'
          AND InternetService = 'Fiber optic'
          AND PaymentMethod = 'Electronic check'
          AND tenure <= 12;
        """),
        
        ("Query 9: Senior Citizen Vulnerability Analysis", """
        SELECT 
            CASE WHEN SeniorCitizen = 1 THEN 'Senior Citizen' ELSE 'Non-Senior Citizen' END AS demographic_group,
            COUNT(*) AS total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(AVG(tenure), 1) AS avg_tenure_months
        FROM customer_churn
        GROUP BY SeniorCitizen;
        """),
        
        ("Query 10: Top 10 High-Value Active Customers at Immediate Risk of Churn (Window Function)", """
        WITH HighRiskActive AS (
            SELECT 
                customerID,
                tenure,
                Contract,
                InternetService,
                PaymentMethod,
                TechSupport,
                OnlineSecurity,
                MonthlyCharges,
                TotalCharges,
                DENSE_RANK() OVER (ORDER BY MonthlyCharges DESC, tenure ASC) AS risk_rank
            FROM customer_churn
            WHERE Churn = 'No'
              AND Contract = 'Month-to-month'
              AND InternetService = 'Fiber optic'
              AND TechSupport = 'No'
        )
        SELECT 
            risk_rank,
            customerID,
            tenure AS tenure_months,
            Contract,
            InternetService,
            PaymentMethod,
            TechSupport,
            OnlineSecurity,
            MonthlyCharges,
            TotalCharges
        FROM HighRiskActive
        WHERE risk_rank <= 10
        ORDER BY risk_rank;
        """)
    ]
    
    for title, q in queries:
        print("=" * 80)
        print(f"📊 {title}")
        print("=" * 80)
        res_df = pd.read_sql_query(q, conn)
        print(res_df.to_string(index=False))
        print("\n")
        
    conn.close()

if __name__ == "__main__":
    run_sql_analytics()
