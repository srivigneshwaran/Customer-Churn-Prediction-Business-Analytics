# 📈 Customer Churn Prediction & Business Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://customer-churn-prediction-business-analytics.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![MySQL / SQL](https://img.shields.io/badge/SQL-MySQL%20%7C%20SQLite-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🌐 **Live Web Application**: [https://customer-churn-prediction-business-analytics.streamlit.app/](https://customer-churn-prediction-business-analytics.streamlit.app/)  
> **Portfolio Track**: Enterprise Data Science / Junior Data Scientist Portfolio  
> **Domain**: Telecommunications & Customer Retention Analytics  
> **Dataset**: IBM Telco Customer Churn (7,043 customer accounts, 21 initial attributes)

---

## 📌 Executive Summary & Business Objective

Acquiring a new customer costs **5 to 25 times more** than retaining an existing one. For a telecommunications enterprise with over 7,000 subscribers and \$456,000+ in Monthly Recurring Revenue (MRR), unmitigated churn results in severe revenue erosion.

In this enterprise project, we build an end-to-end customer churn analysis and predictive intelligence platform that:
1. **Identifies Churn Patterns**: Dissects behavioral, contractual, and service features causing customer defection.
2. **Quantifies Statistical Significance**: Uses parametric (Welch's $t$-test), non-parametric (Mann-Whitney $U$), and categorical association tests (Chi-Square $\chi^2$, Cramér's $V$, and Bayes' Theorem) to prove causal factors.
3. **Predicts Individual Churn Propensity**: Deploys an interpretable, production-ready Machine Learning model achieving **~79% Recall and 0.849 ROC-AUC**, prioritized to flag high-risk subscribers before they cancel.
4. **Calculates Financial Impact**: Provides actionable SQL business analytics and strategic recommendations to safeguard at-risk revenue.

---

## 🏗️ Repository Architecture

```text
customer-churn-analysis/
│
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Raw IBM Telco dataset (7,043 rows)
│   └── cleaned_telco_churn.csv               # Cleaned & engineered dataset
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb                # Module 1: Missing values, anomalies & typing
│   ├── 02_eda.ipynb                          # Module 2: Visualizations, distributions & cohorts
│   ├── 03_statistical_analysis.ipynb         # Module 3: Hypothesis tests, p-values & Cramer's V
│   └── 04_model_training.ipynb               # Module 4: Pipeline, modeling, odds ratios & export
│
├── sql/
│   └── customer_analysis.sql                 # Module 5: 10 production SQL analytics queries & DDL
│
├── models/
│   └── churn_model.pkl                       # Serialized Sklearn production pipeline (preprocessor + model)
│
├── reports/
│   └── figures/                              # High-resolution saved visualizations
│       ├── 01_churn_distribution.png
│       ├── 02_tenure_vs_churn.png
│       ├── 03_monthly_charges_vs_churn.png
│       ├── 04_contract_type_churn.png
│       ├── 05_internet_service_techsupport_churn.png
│       ├── 06_payment_method_churn.png
│       ├── 08_correlation_matrix.png
│       ├── 09_cramers_v_association.png
│       ├── 10_confusion_matrices.png
│       ├── 11_roc_pr_curves.png
│       └── 12_feature_importance_odds_ratios.png
│
├── src/
│   ├── data_cleaning.py                      # Standalone data cleaning ETL script
│   ├── predict_churn.py                      # Interactive CLI prediction tool
│   └── run_sql_analysis.py                   # Automated SQL test runner & reporting engine
│
├── app.py                                    # Interactive Streamlit Web UI Dashboard
├── PROJECT_DETAILED_DESCRIPTION.txt          # In-depth plain-text project reference
├── requirements.txt                          # Python dependencies
├── .gitignore                                # Git ignore file
└── README.md                                 # Comprehensive portfolio documentation
```

---

## 🛠️ Technology Stack & Purpose

| Technology | Purpose in Project |
| :--- | :--- |
| **Python 3.12** | Core programming language for data pipelines and modeling |
| **Pandas** | Data wrangling, aggregation, missing value imputation, cohort binning |
| **NumPy** | Vectorized mathematical operations and probability computations |
| **Matplotlib & Seaborn** | Statistical data visualization, KDE plots, odds ratio charts |
| **SciPy (Stats)** | Welch's $t$-test, Mann-Whitney $U$, Chi-Square test of independence, Cramér's $V$ |
| **Scikit-Learn** | Pipeline, ColumnTransformer, Logistic Regression, Random Forest, Gradient Boosting |
| **Joblib** | Model serialization for deployment (`churn_model.pkl`) |
| **SQL (MySQL / SQLite)** | Database schema design, window functions, and business cohort queries |
| **Jupyter Notebook** | Reproducible development, step-by-step documentation and reporting |

---

## 📊 Modules & Key Findings

### Module 1 – Data Collection & Cleaning
- **Raw Data Audit**: 7,043 rows, 21 columns, 0 duplicate records.
- **Anomalous Field Resolution**: `TotalCharges` was loaded as text (`object`) due to 11 empty whitespace strings (`' '`).
- **Domain-Specific Imputation**: All 11 records had `tenure = 0` months (new accounts before their first billing cycle). Imputing `0.0` preserved valuable customer profiles without introducing synthetic bias.
- **Engineered Attributes**: `Churn_Binary` ($1 = \text{Yes}, 0 = \text{No}$) and `TenureGroup` cohorts (`0-12 Mo`, `13-24 Mo`, etc.). Clean dataset saved to `data/cleaned_telco_churn.csv`.

---

### Module 2 – Exploratory Data Analysis (EDA)
- **Baseline Churn Rate**: **26.54%** (1,869 churned vs 5,174 retained customers).
- **The Early Churn Hazard**: Customers in their first 12 months exhibit a **47.4% churn rate**, dropping to **6.6%** after 5 years ($61\text{--}72$ months).
- **Contract Type**: Month-to-month contracts represent **88.6% of all churn volume** with a **42.71% churn rate**, compared to **11.27%** for one-year and **2.83%** for two-year contracts.
- **Fiber Optic Paradox**: Fiber Optic subscribers churn at **41.89%** vs DSL at **18.96%**, driven by steep monthly charges ($\$87+$) without bundled technical assistance.
- **Payment Method Friction**: Electronic check users have a **45.29% churn rate**, whereas credit card and bank transfer auto-pay users churn at only $\sim 15\text{--}16\%$.

---

### Module 3 – Statistical Analysis & Hypothesis Testing

#### 1. Parametric & Non-Parametric Tests (Continuous Variables)
- **Hypothesis 1: Monthly Charges**:
  - Churned Mean: **\$74.44** ($\pm \$24.67$) | Retained Mean: **\$61.27** ($\pm \$31.09$)
  - **Welch's $t$-test**: $t = 18.40$, $p = 8.59 \times 10^{-73}$ $\rightarrow$ **Reject $H_0$**.
  - **Mann-Whitney $U$ test**: $U = 3,747,404.5$, $p = 1.09 \times 10^{-58}$ $\rightarrow$ Confirmed non-parametric robustness.
  - *Conclusion*: Churned customers pay statistically significantly higher monthly charges.
- **Hypothesis 2: Customer Tenure**:
  - Retained Mean: **37.57 months** | Churned Mean: **17.98 months** ($-19.59$ months difference)
  - **Welch's $t$-test**: $t = 34.82$, $p = 7.79 \times 10^{-208}$ $\rightarrow$ **Reject $H_0$**.
  - *Conclusion*: Customer tenure is significantly shorter for churners.

#### 2. Categorical Association Tests ($\chi^2$ & Cramér's $V$)
| Predictor Feature | Chi-Square ($\chi^2$) | $p$-value | Cramér's $V$ | Association Strength |
| :--- | :---: | :---: | :---: | :--- |
| **Contract** | 1,184.60 | $< 10^{-250}$ | **0.410** | **Strong** |
| **OnlineSecurity** | 849.99 | $< 10^{-180}$ | **0.347** | **Strong** |
| **TechSupport** | 828.20 | $< 10^{-180}$ | **0.337** | **Strong** |
| **InternetService** | 732.31 | $< 10^{-150}$ | **0.322** | **Strong** |
| **PaymentMethod** | 648.14 | $< 10^{-130}$ | **0.301** | **Strong** |
| **PaperlessBilling** | 258.28 | $< 10^{-55}$ | **0.192** | Moderate |
| **SeniorCitizen** | 159.43 | $< 10^{-35}$ | **0.150** | Moderate |

#### 3. Bayesian Probability Update
- Prior Probability $P(\text{Churn}) = 26.54\%$.
- Posterior Probability given Month-to-Month Contract: $P(\text{Churn} \mid \text{M2M}) = 42.71\%$.
- Posterior Probability given High-Risk Signature (M2M + Fiber Optic + Electronic Check + Tenure $\le 12$): **$P(\text{Churn}) = 71.16\%$**.

---

### Module 4 – Machine Learning Modeling & Evaluation

An end-to-end scikit-learn `Pipeline` was constructed with `StandardScaler` for numeric variables and `OneHotEncoder(drop='first')` for categorical predictors, evaluated on an 80/20 stratified test set (1,409 customers).

#### Model Benchmark Comparison
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Balanced)** | **73.95%** | **50.60%** | **78.61%** | **0.6157** | **0.8418** | **0.6345** |
| **Random Forest (Balanced)** | 75.51% | 52.57% | 79.41% | 0.6326 | 0.8434 | 0.6513 |
| **Gradient Boosting** | 80.34% | 66.11% | 53.21% | 0.5896 | 0.8434 | 0.6567 |

> **Business Rationale for Primary Model**:  
> In customer churn prevention, **Recall is the top-priority metric**: a False Negative (failing to catch a churner) costs hundreds of dollars in lost lifetime value, whereas a False Positive costs only a nominal retention email or discount offer. Logistic Regression with balanced weighting captures **nearly 8 out of 10 churning customers** while providing complete transparency through **Odds Ratios**.

#### Feature Impact & Odds Ratios ($OR = e^{\beta}$)
- **Top Churn Catalysts (Risk Factors)**:
  - `InternetService_Fiber optic`: $\beta = +0.967 \rightarrow \mathbf{OR = 2.63}$ ($+163\%$ higher odds of churn)
  - `TotalCharges`: $\beta = +0.458 \rightarrow \mathbf{OR = 1.58}$ ($+58\%$ higher odds of churn)
  - `PaymentMethod_Electronic check`: $\beta = +0.400 \rightarrow \mathbf{OR = 1.49}$ ($+49\%$ higher odds of churn)
  - `PaperlessBilling_Yes`: $\beta = +0.337 \rightarrow \mathbf{OR = 1.40}$ ($+40\%$ higher odds of churn)
- **Top Protective Factors (Retention Anchors)**:
  - `Contract_Two year`: $\beta = -1.381 \rightarrow \mathbf{OR = 0.25}$ (**75% reduction** in churn odds)
  - `tenure`: $\beta = -1.134 \rightarrow \mathbf{OR = 0.32}$ (**68% reduction** in churn odds per std dev)
  - `Contract_One year`: $\beta = -0.708 \rightarrow \mathbf{OR = 0.49}$ (**51% reduction** in churn odds)
  - `OnlineSecurity_Yes` & `TechSupport_Yes`: $\mathbf{OR \approx 0.68\text{--}0.73}$ (**$27\text{--}32\%$ reduction** in churn odds)

---

### Module 5 – SQL Business Analytics Queries

The project includes `sql/customer_analysis.sql` with 10 production queries tested against the database:

1. **Executive KPI Query**: Total customer base (7,043), churn rate (26.54%), Active MRR (\$316,985.75), Total MRR (\$456,116.60).
2. **Contract Segmentation**: Shows Month-to-month contracts driving 1,655 of the 1,869 churned accounts.
3. **Price Sensitivity Analysis**: Demonstrates that churners across all contract tiers pay higher monthly charges than retained peers.
4. **Payment Method Analysis**: Flags Electronic Check as the highest-churn channel (45.29% churn, \$180,345 MRR).
5. **Revenue Breakdown**: Quantifies that churned customers represent **\$139,130.85 in lost MRR** (30.5% of potential recurring cash flow).
6. **Support Service Cross-Tab**: Highlights that Fiber Optic churn drops from **49.37% (without Tech Support) to 22.63% (with Tech Support)**.
7. **Tenure Cohort Velocity**: Tracks retention recovery from 47.4% churn in Year 1 down to 6.6% in Years 5–6.
8. **High-Risk Segment Revenue**: Isolates 631 critical-risk customers with a **71.16% churn rate, risking \$51,934.95 monthly and \$623,219.40 annualized**.
9. **Senior Citizen Analysis**: Analyzes the 41.68% churn rate in senior citizens (\$79.82 average monthly charge).
10. **Window Function Active Risk Queue**: Uses `DENSE_RANK() OVER (ORDER BY MonthlyCharges DESC, tenure ASC)` to output the top high-paying active customers needing immediate intervention.

---

## 💡 Strategic Business Recommendations

| Problem Identified | Root Cause | Recommended Strategic Action | Expected Impact |
| :--- | :--- | :--- | :--- |
| **88.6% of churn from Month-to-Month** | High flexibility to exit with no contractual commitment | Introduce a **"Transition & Save" campaign**: offer 15% discount or 3 months of free streaming for signing a 1-year agreement | Shift 20% of M2M base $\rightarrow$ **Reduce churn volume by ~330 customers (\$260k annual MRR)** |
| **49.4% churn on Fiber Optic without Tech Support** | Premium price (\$85+) leads to acute frustration during outages | **Bundle 6 months of free Tech Support & Online Security** into all new Fiber Optic installations | Cut Fiber Optic churn rate from 49.4% down towards 22.6% |
| **45.3% churn on Electronic Check** | Manual monthly billing friction, bill shock, payment failure | Provide a **\$3.00/month recurring statement credit** for customers enrolling in automated credit card or bank transfer auto-pay | Shift users to autopay channels exhibiting only 15% churn |
| **47.4% churn during Months 0–12** | Poor onboarding experience and early feature adoption deficit | Establish an automated **Onboarding Lifecycle Trigger**: proactive reach-out at Day 14, 45, and 90 with satisfaction checks | Boost 1st-year retention by 15–20% |

---

## 🚀 Quickstart & Reproduction Guide

### 1. Prerequisites & Environment Setup
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/Customer-Churn-Prediction-Business-Analytics.git
cd Customer-Churn-Prediction-Business-Analytics
pip install -r requirements.txt
```

### 2. Run Data Cleaning & ETL
```bash
python src/data_cleaning.py
```
*Generates `data/cleaned_telco_churn.csv`.*

### 3. Run Automated SQL Analytics
```bash
python src/run_sql_analysis.py
```
*Executes all 10 business queries from `sql/customer_analysis.sql` and prints formatted tabular reports.*

### 4. Interactive Jupyter Notebooks
Open the notebooks in your preferred environment:
```bash
jupyter notebook notebooks/
```
- `notebooks/01_data_cleaning.ipynb`
- `notebooks/02_eda.ipynb`
- `notebooks/03_statistical_analysis.ipynb`
- `notebooks/04_model_training.ipynb`

### 5. Launch Interactive Streamlit Web UI Dashboard
- 🌐 **Live Cloud App**: [https://customer-churn-prediction-business-analytics.streamlit.app/](https://customer-churn-prediction-business-analytics.streamlit.app/)
- Or run locally on your machine:
```bash
streamlit run app.py
```
*Opens an interactive browser app featuring real-time churn prediction sliders, executive KPI cards, empirical charts, and odds ratio explainability tables.*

### 6. Production Model Scoring Demo (CLI)
To score a new customer using the serialized model pipeline:
```python
import joblib
import pandas as pd

# Load saved pipeline
model = joblib.load('models/churn_model.pkl')

# New customer profile
new_customer = pd.DataFrame([{
    'gender': 'Female',
    'SeniorCitizen': 0,
    'Partner': 'No',
    'Dependents': 'No',
    'tenure': 2,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No',
    'OnlineBackup': 'No',
    'DeviceProtection': 'No',
    'TechSupport': 'No',
    'StreamingTV': 'Yes',
    'StreamingMovies': 'Yes',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 95.50,
    'TotalCharges': 191.00
}])

prob = model.predict_proba(new_customer)[0, 1]
print(f"Customer Churn Probability: {prob*100:.2f}%")
# Output: Customer Churn Probability: 90.14% [CRITICAL RISK]
```

---

## 🎯 Enterprise Data Science Interview Talking Points

1. **Why Logistic Regression over Complex Black-Box Ensembles?**
   - *Answer*: In enterprise telecom analytics, interpretability is as critical as predictive accuracy. Logistic Regression provides explicit **Odds Ratios ($e^\beta$)** allowing business stakeholders to see the exact odds multiplier of each feature (e.g., Month-to-month contract multiplies odds of leaving by $2.15\times$, whereas Two-year contracts reduce odds by $75\%$). Furthermore, with class-balanced weighting, it achieves **~79% Recall and 0.842 ROC-AUC**, closely matching Random Forest while enabling regulatory and compliance auditing.
2. **How did you handle missing values in TotalCharges without data leakage?**
   - *Answer*: Rather than applying a naive global mean or median imputation, I performed an anomaly audit and observed that all 11 missing `TotalCharges` entries occurred exclusively when `tenure = 0`. These represent newly onboarded customers who have not completed their first billing cycle. Setting `TotalCharges = 0.0` reflects business ground-truth, avoids deleting customer signups, and prevents target leakage.
3. **Why Welch's $t$-test instead of Student's $t$-test?**
   - *Answer*: Student's $t$-test assumes equal population variances (homoscedasticity). In customer churn data, retained customers and churned customers have markedly unequal sample sizes ($5,174$ vs $1,869$) and unequal variances ($\sigma_{\text{Retain}} = \$31.09$ vs $\sigma_{\text{Churn}} = \$24.67$). Welch's $t$-test adjusts the degrees of freedom using the Welch-Satterthwaite equation, providing an unbiased $t$-statistic and p-value.
4. **How do SQL and Python collaborate in this architecture?**
   - *Answer*: SQL handles structured extraction, database schema design, and cohort aggregation in the data warehouse layer (e.g. calculating MRR impact and identifying active accounts with window functions). Python and Scikit-Learn handle statistical hypothesis testing, data transformations, and machine learning inference.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
