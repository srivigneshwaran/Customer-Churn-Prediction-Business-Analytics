"""
Customer Churn Prediction & Business Analytics Dashboard
Interactive Streamlit Web Application
Track: Enterprise Data Science Portfolio
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction & Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive cards and badges
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #2b5c8f;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 26px;
        font-weight: bold;
        color: #1a202c;
    }
    .metric-label {
        font-size: 13px;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .risk-badge-critical {
        background-color: #ffebee;
        color: #c62828;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #ef9a9a;
    }
    .risk-badge-elevated {
        background-color: #fff8e1;
        color: #f57f17;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #ffe082;
    }
    .risk-badge-low {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #a5d6a7;
    }
    /* Hide Streamlit header anchor link icons */
    [data-testid="stHeaderActionElements"], a.anchor-link {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Load Model & Dataset
# -----------------------------------------------------------------------------
@st.cache_resource
def load_model():
    model_path = "models/churn_model.pkl"
    if not os.path.exists(model_path):
        st.error(f"Model file not found at {model_path}. Please train the model first.")
        return None
    return joblib.load(model_path)

@st.cache_data
def load_data():
    data_path = "data/cleaned_telco_churn.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

model = load_model()
df_clean = load_data()

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("📈 Telecom Customer Churn Prediction & Analytics")
st.markdown("**Predictive Intelligence & Retention Analytics** | **Primary Model**: Balanced Logistic Regression (Recall: 78.6%, ROC-AUC: 0.842)")

# -----------------------------------------------------------------------------
# Navigation Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Real-Time Churn Predictor",
    "📊 Business Analytics & Executive KPIs",
    "🧠 Model Explainability & Odds Ratios"
])

# =============================================================================
# TAB 1: Real-Time Churn Predictor
# =============================================================================
with tab1:
    st.subheader("Customer Profile & Risk Scoring")
    st.write("Adjust subscriber attributes below or choose a pre-configured customer persona to predict churn probability.")

    # Quick persona buttons
    col_preset1, col_preset2, col_preset3, _ = st.columns([1, 1, 1, 2])
    
    preset_choice = None
    if col_preset1.button("🚨 Load High-Risk Persona"):
        preset_choice = "high_risk"
    if col_preset2.button("✅ Load Loyal Persona"):
        preset_choice = "loyal"
    if col_preset3.button("🔄 Reset Defaults"):
        preset_choice = "default"

    # Default values based on preset
    if preset_choice == "high_risk":
        def_gender, def_senior, def_partner, def_dep = "Female", 0, "No", "No"
        def_tenure, def_contract = 2, "Month-to-month"
        def_internet, def_techsup, def_sec = "Fiber optic", "No", "No"
        def_phone, def_mult = "Yes", "No"
        def_backup, def_device, def_tv, def_movies = "No", "No", "Yes", "Yes"
        def_paperless, def_pay = "Yes", "Electronic check"
        def_monthly = 95.50
    elif preset_choice == "loyal":
        def_gender, def_senior, def_partner, def_dep = "Male", 0, "Yes", "Yes"
        def_tenure, def_contract = 60, "Two year"
        def_internet, def_techsup, def_sec = "DSL", "Yes", "Yes"
        def_phone, def_mult = "Yes", "Yes"
        def_backup, def_device, def_tv, def_movies = "Yes", "Yes", "No", "No"
        def_paperless, def_pay = "No", "Credit card (automatic)"
        def_monthly = 65.00
    else:
        def_gender, def_senior, def_partner, def_dep = "Female", 0, "No", "No"
        def_tenure, def_contract = 12, "Month-to-month"
        def_internet, def_techsup, def_sec = "Fiber optic", "No", "No"
        def_phone, def_mult = "Yes", "No"
        def_backup, def_device, def_tv, def_movies = "No", "No", "No", "No"
        def_paperless, def_pay = "Yes", "Electronic check"
        def_monthly = 75.00

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<p style='font-size: 17px; font-weight: bold; margin-bottom: 8px;'>👤 Demographics & Tenure</p>", unsafe_allow_html=True)
            gender = st.selectbox("Gender", ["Female", "Male"], index=0 if def_gender=="Female" else 1)
            senior = st.selectbox("Senior Citizen", [0, 1], index=def_senior, format_func=lambda x: "Yes (Senior)" if x == 1 else "No (Non-Senior)")
            partner = st.selectbox("Has Partner", ["No", "Yes"], index=0 if def_partner=="No" else 1)
            dependents = st.selectbox("Has Dependents", ["No", "Yes"], index=0 if def_dep=="No" else 1)
            tenure = st.slider("Tenure with Company (Months)", min_value=0, max_value=72, value=def_tenure, help="Number of months customer has stayed with telecom")

        with col2:
            st.markdown("<p style='font-size: 17px; font-weight: bold; margin-bottom: 8px;'>🌐 Connectivity & Services</p>", unsafe_allow_html=True)
            phone_service = st.selectbox("Phone Service", ["Yes", "No"], index=0 if def_phone=="Yes" else 1)
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"], index=["No", "Yes", "No phone service"].index(def_mult))
            internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"], index=["Fiber optic", "DSL", "No"].index(def_internet))
            online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_sec))
            online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_backup))
            device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_device))
            tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_techsup))
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_tv))
            streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(def_movies))

        with col3:
            st.markdown("<p style='font-size: 17px; font-weight: bold; margin-bottom: 8px;'>💳 Contract & Billing</p>", unsafe_allow_html=True)
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], index=["Month-to-month", "One year", "Two year"].index(def_contract))
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"], index=0 if def_paperless=="Yes" else 1)
            payment_method = st.selectbox(
                "Payment Method",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
                index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(def_pay)
            )
            monthly_charges = st.slider("Monthly Charges ($)", min_value=18.0, max_value=120.0, value=float(def_monthly), step=0.5)
            # Approximate total charges
            est_total = max(round(tenure * monthly_charges, 2), 0.0)
            total_charges = st.number_input("Total Lifetime Charges ($)", min_value=0.0, max_value=10000.0, value=float(est_total), step=10.0)

        submit_btn = st.form_submit_button("⚡ Predict Customer Churn Risk", use_container_width=True)

    if submit_btn and model is not None:
        input_data = pd.DataFrame([{
            'gender': gender,
            'SeniorCitizen': senior,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }])

        pred = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0, 1]
        prob_pct = prob * 100

        st.markdown("---")
        st.subheader("Prediction Result & Risk Diagnosis")

        res_col1, res_col2 = st.columns([1, 1.5])

        with res_col1:
            if prob >= 0.70:
                st.markdown(f"<div class='risk-badge-critical'>🚨 CRITICAL CHURN RISK ({prob_pct:.1f}%)</div>", unsafe_allow_html=True)
                st.progress(prob, text=f"Churn Propensity: {prob_pct:.1f}%")
                st.error("⚠️ **High Probability of Churn**: This customer has a very high propensity to cancel within the next billing cycle.")
            elif prob >= 0.40:
                st.markdown(f"<div class='risk-badge-elevated'>⚠️ ELEVATED RISK ({prob_pct:.1f}%)</div>", unsafe_allow_html=True)
                st.progress(prob, text=f"Churn Propensity: {prob_pct:.1f}%")
                st.warning("⚡ **Moderate / Elevated Risk**: Customer exhibits signs of vulnerability. Monitor for retention campaign.")
            else:
                st.markdown(f"<div class='risk-badge-low'>✅ LOW CHURN RISK ({prob_pct:.1f}%)</div>", unsafe_allow_html=True)
                st.progress(prob, text=f"Churn Propensity: {prob_pct:.1f}%")
                st.success("🎉 **Customer Retained**: Subscriber shows high loyalty metrics and low cancellation likelihood.")

        with res_col2:
            st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 8px;'>💡 Tactical Business Actions for this Profile:</p>", unsafe_allow_html=True)
            recommendations = []
            if contract == "Month-to-month":
                recommendations.append("📌 **Contract Transition**: Offer a 15% discount for switching to an annual commitment.")
            if payment_method == "Electronic check":
                recommendations.append("💳 **Autopay Credit**: Grant a $3/mo bill credit for enrolling in automated bank or credit card autopay.")
            if internet_service == "Fiber optic" and tech_support == "No":
                recommendations.append("🛠️ **Bundle Support**: Offer 3 months of free Technical Support to mitigate fiber outage frustration.")
            if tenure <= 12:
                recommendations.append("📞 **Early Touchpoint**: Schedule a Customer Success check-in to ensure satisfaction during month 1–12 window.")
            if not recommendations:
                recommendations.append("🌟 **Loyalty Milestone**: Customer is in a healthy loyalty bracket. Maintain relationship and explore cross-sell opportunities.")

            for r in recommendations:
                st.markdown(r)

# =============================================================================
# TAB 2: Business Analytics & Executive KPIs
# =============================================================================
with tab2:
    st.subheader("Telecom Portfolio Health (IBM Telco Dataset: 7,043 Customers)")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown("<div class='metric-card'><div class='metric-label'>Total Customer Base</div><div class='metric-value'>7,043</div></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown("<div class='metric-card'><div class='metric-label'>Overall Churn Rate</div><div class='metric-value'>26.54%</div></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown("<div class='metric-card'><div class='metric-label'>Total Monthly Revenue</div><div class='metric-value'>$456,116</div></div>", unsafe_allow_html=True)
    with kpi4:
        st.markdown("<div class='metric-card'><div class='metric-label'>Monthly Revenue Lost to Churn</div><div class='metric-value' style='color:#c62828;'>$139,130 (30.5%)</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Key Empirical Visualizations")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        if os.path.exists("reports/figures/04_contract_type_churn.png"):
            st.image("reports/figures/04_contract_type_churn.png", caption="Churn Rate by Contract Duration", use_container_width=True)
        if os.path.exists("reports/figures/02_tenure_vs_churn.png"):
            st.image("reports/figures/02_tenure_vs_churn.png", caption="Tenure vs Churn (47.4% churn in Month 0-12)", use_container_width=True)

    with chart_col2:
        if os.path.exists("reports/figures/05_internet_service_techsupport_churn.png"):
            st.image("reports/figures/05_internet_service_techsupport_churn.png", caption="Internet Service & Tech Support Impact", use_container_width=True)
        if os.path.exists("reports/figures/06_payment_method_churn.png"):
            st.image("reports/figures/06_payment_method_churn.png", caption="Payment Method Friction (45.3% churn on Electronic Check)", use_container_width=True)

# =============================================================================
# TAB 3: Model Explainability & Odds Ratios
# =============================================================================
with tab3:
    st.subheader("Model Rationale & Explainability: Why Logistic Regression?")
    st.markdown("""
    In enterprise customer retention, **interpretability is as important as accuracy**. 
    While black-box ensembles give obscure importance scores, Logistic Regression produces mathematically rigorous **Odds Ratios ($e^\beta$)**.
    """)

    st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 8px;'>Top Risk Multipliers vs Retention Anchors:</p>", unsafe_allow_html=True)
    
    odds_data = {
        'Feature Name': [
            'InternetService = Fiber optic',
            'TotalCharges (Higher bill volume)',
            'PaymentMethod = Electronic check',
            'PaperlessBilling = Yes',
            'Contract = Two year',
            'Customer Tenure (per std deviation)',
            'Contract = One year',
            'TechSupport = Yes',
            'OnlineSecurity = Yes'
        ],
        'Odds Ratio (OR)': [
            '2.63x (Risk Factor)',
            '1.58x (Risk Factor)',
            '1.49x (Risk Factor)',
            '1.40x (Risk Factor)',
            '0.25x (75% Reduction)',
            '0.32x (68% Reduction)',
            '0.49x (51% Reduction)',
            '0.73x (27% Reduction)',
            '0.68x (32% Reduction)'
        ],
        'Business Meaning': [
            'Fiber customers have 2.63x higher odds of leaving without bundled support',
            'Accumulated cost pressures increase churn sensitivity',
            'Manual payment friction increases likelihood of cancellation',
            'Digital statements make it easier to switch providers',
            'Signing a 2-year agreement drops churn likelihood by 75%',
            'Each year of tenure dramatically solidifies customer loyalty',
            'Annual agreements halve the odds of departure',
            'Proactive technical support protects accounts from leaving',
            'Cybersecurity add-ons create switching friction and lock-in'
        ]
    }
    st.table(pd.DataFrame(odds_data))

    if os.path.exists("reports/figures/12_feature_importance_odds_ratios.png"):
        st.image("reports/figures/12_feature_importance_odds_ratios.png", caption="Feature Coefficients & Odds Ratio Impact", use_container_width=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built with Python, Scikit-Learn, Pandas & Streamlit</p>", unsafe_allow_html=True)
