import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
import shap
import plotly.graph_objects as go
from fpdf import FPDF
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="💳",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("Model.pkl")

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "records" not in st.session_state:
    st.session_state.records = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# SIDEBAR THEME TOGGLE
# =========================

theme = st.sidebar.toggle("🌙 Dark Mode")

if theme:
    bg1 = "#0f172a"
    bg2 = "#111827"
    bg3 = "#1e293b"
    text = "white"
    card = "rgba(30,41,59,0.65)"
else:
    bg1 = "#dbeafe"
    bg2 = "#eff6ff"
    bg3 = "#f0f9ff"
    text = "#0f172a"
    card = "rgba(255,255,255,0.55)"

# =========================
# PROFESSIONAL UI
# =========================
st.markdown(f"""
<style>

/* MAIN BACKGROUND */
.stApp{{
background:linear-gradient(135deg,{bg1},{bg2},{bg3});
background-attachment:fixed;
}}

/* HEADER */
.main-title{{
font-size:52px;
font-weight:800;
text-align:center;
color:{text};
margin-bottom:5px;
}}

.subtitle{{
text-align:center;
font-size:20px;
color:{text};
margin-bottom:25px;
}}

/* GLASS CARD */
.card{{
background:{card};
backdrop-filter:blur(18px);
-webkit-backdrop-filter:blur(18px);
padding:28px;
border-radius:24px;
border:1px solid rgba(255,255,255,0.35);
box-shadow:0 8px 32px rgba(31,38,135,0.15);
margin-bottom:22px;
transition:0.3s;
}}

.card:hover{{
transform:translateY(-3px);
box-shadow:0 12px 40px rgba(31,38,135,0.2);
}}

/* SIDEBAR */
section[data-testid="stSidebar"]{{
background:rgba(15,23,42,0.92)!important;
backdrop-filter:blur(12px);
}}

section[data-testid="stSidebar"] *{{
color:white!important;
}}

/* TEXT */
h1,h2,h3,h4,p,label,span{{
color:{text}!important;
font-family:'Segoe UI';
}}

/* BUTTON */
.stButton>button{{
width:100%;
height:56px;
border:none;
border-radius:16px;
background:linear-gradient(135deg,#2563eb,#06b6d4);
color:white;
font-size:18px;
font-weight:700;
transition:0.3s;
box-shadow:0 8px 20px rgba(37,99,235,0.25);
}}

.stButton>button:hover{{
transform:scale(1.02);
}}

/* DOWNLOAD BUTTON */
.stDownloadButton>button{{
width:100%;
height:55px;
border:none;
border-radius:16px;
background:linear-gradient(135deg,#2563eb,#06b6d4)!important;
color:white!important;
font-size:16px;
font-weight:bold;
}}

/* INPUT */
.stNumberInput input,
.stTextInput input{{
border-radius:14px!important;
border:1px solid #cbd5e1!important;
background:white!important;
color:black!important;
font-weight:bold!important;
}}

/* SELECT */
div[data-baseweb="select"] > div{{
background:rgba(255,255,255,0.7)!important;
border-radius:12px!important;
color:black!important;
}}

/* METRICS */
[data-testid="metric-container"]{{
background:{card};
border-radius:20px;
padding:18px;
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,0.4);
}}

/* DATAFRAME */
[data-testid="stDataFrame"]{{
border-radius:18px;
overflow:hidden;
}}

/* FRAUD POPUP ANIMATION */
@keyframes pulseAlert{{
0%{{transform:scale(1);}}
50%{{transform:scale(1.03);}}
100%{{transform:scale(1);}}
}}

.fraud-popup{{
animation:pulseAlert 1s infinite;
background:#fee2e2;
padding:22px;
border-radius:18px;
border-left:10px solid red;
color:#991b1b;
font-size:24px;
font-weight:800;
text-align:center;
margin-top:20px;
box-shadow:0 8px 30px rgba(255,0,0,0.18);
}}

/* SAFE POPUP */
.safe-popup{{
background:#dcfce7;
padding:22px;
border-radius:18px;
border-left:10px solid green;
color:#166534;
font-size:24px;
font-weight:800;
text-align:center;
margin-top:20px;
box-shadow:0 8px 30px rgba(0,255,100,0.15);
}}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='text-align:center;'>🏦 FraudShield AI Login</h1>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):

        if username == "raju" and password == "7264":
            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-title">
🏦 FraudShield AI Banking Dashboard
</div>

<div class="subtitle">
AI Powered Real-Time Fraud Detection System
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏦 FraudShield AI")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Fraud History",
        "AI Chatbot",
        "Live Simulator"
    ]
)

# =========================
# MONTHS
# =========================
months = {
    "January":1,
    "February":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "August":8,
    "September":9,
    "October":10,
    "November":11,
    "December":12
}

# =========================
# DAYS
# =========================
days = {
    "Monday":0,
    "Tuesday":1,
    "Wednesday":2,
    "Thursday":3,
    "Friday":4,
    "Saturday":5,
    "Sunday":6
}

# =========================
# HOURS
# =========================
hour_options = [
    "12 AM","1 AM","2 AM","3 AM","4 AM","5 AM",
    "6 AM","7 AM","8 AM","9 AM","10 AM","11 AM",
    "12 PM","1 PM","2 PM","3 PM","4 PM","5 PM",
    "6 PM","7 PM","8 PM","9 PM","10 PM","11 PM"
]

hour_map = {
    "12 AM":0,"1 AM":1,"2 AM":2,"3 AM":3,
    "4 AM":4,"5 AM":5,"6 AM":6,"7 AM":7,
    "8 AM":8,"9 AM":9,"10 AM":10,"11 AM":11,
    "12 PM":12,"1 PM":13,"2 PM":14,"3 PM":15,
    "4 PM":16,"5 PM":17,"6 PM":18,"7 PM":19,
    "8 PM":20,"9 PM":21,"10 PM":22,"11 PM":23
}

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    c1,c2,c3,c4 = st.columns(4)

    fraud_count = len([
        r for r in st.session_state.records
        if r["Prediction"] == "Fraud"
    ])

    legit_count = len(st.session_state.records) - fraud_count

    fraud_percent = 0

    if len(st.session_state.records) > 0:
        fraud_percent = (
            fraud_count /
            len(st.session_state.records)
        ) * 100

    c1.metric("💳 Transactions", len(st.session_state.records))
    c2.metric("🚨 Frauds", fraud_count)
    c3.metric("✅ Safe", legit_count)
    c4.metric("📊 Fraud %", f"{fraud_percent:.2f}%")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("📥 Transaction Details")

        selected_month = st.selectbox(
            "Select Month",
            list(months.keys())
        )

        TransactionMonth = months[selected_month]

        selected_hour = st.selectbox(
            "Transaction Time",
            hour_options
        )

        TransactionHour = hour_map[selected_hour]

        selected_day = st.selectbox(
            "Select Day",
            list(days.keys())
        )

        TransactionDayOfWeek = days[selected_day]

        Amount = st.number_input(
            "Transaction Amount",
            min_value=0.0,
            value=1000.0
        )

        MerchantID = st.number_input(
            "Merchant ID",
            min_value=0.0,
            value=1.0
        )

        refund_option = st.selectbox(
            "Refund Transaction",
            ["No","Yes"]
        )

        if refund_option == "Yes":
            TransactionType_refund = 1
        else:
            TransactionType_refund = 0

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        location = st.selectbox(
            "📍 Location",
            [
                "San Diego",
                "San Jose",
                "Philadelphia",
                "Phoenix",
                "San Antonio",
                "Houston",
                "Los Angeles",
                "New York",
                "Dallas"
            ]
        )

        locations = [0] * 9

        location_map = {
            "San Diego":0,
            "San Jose":1,
            "Philadelphia":2,
            "Phoenix":3,
            "San Antonio":4,
            "Houston":5,
            "Los Angeles":6,
            "New York":7,
            "Dallas":8
        }

        locations[location_map[location]] = 1

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # AI RISK METER
    # =========================
    def gauge(prob):

        color = "green"

        if prob > 0.3:
            color = "orange"

        if prob > 0.7:
            color = "red"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob*100,
            number={'suffix':'%'},
            title={'text':'AI Risk Meter'},
            gauge={
                'axis':{'range':[0,100]},
                'bar':{'color':color},
                'bgcolor':'white',
                'steps':[
                    {'range':[0,30],'color':'#22c55e'},
                    {'range':[30,70],'color':'#f59e0b'},
                    {'range':[70,100],'color':'#ef4444'}
                ]
            }
        ))

        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color':text,'size':18}
        )

        return fig

    # =========================
    # ANALYZE
    # =========================
    if st.button("🚀 Analyze Transaction"):

        with st.spinner("🔍 AI is analyzing transaction..."):
            time.sleep(2)

        features = locations + [
            TransactionMonth,
            TransactionType_refund,
            Amount,
            MerchantID,
            TransactionHour,
            TransactionDayOfWeek
        ]

        X = np.array(features).reshape(1,-1)

        prob = model.predict_proba(X)[0][1]

        prediction = 0

        if Amount > 50000:
            prediction = 1

        if TransactionHour < 5 and Amount > 20000:
            prediction = 1

        if TransactionType_refund == 1 and Amount > 30000:
            prediction = 1

        if TransactionDayOfWeek in [5,6] and Amount > 40000:
            prediction = 1

        if prob > 0.30:
            prediction = 1

        st.session_state.history.append(prob)

        if prediction == 1:
            result = "Fraud"
        else:
            result = "Legitimate"

        st.session_state.records.append({
            "Amount": Amount,
            "Location": location,
            "Probability": round(prob*100,2),
            "Prediction": result
        })

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("🔍 Fraud Analysis")

        st.plotly_chart(
            gauge(prob),
            use_container_width=True
        )

        if prediction == 1:

            st.markdown("""
            <div class="fraud-popup">
            🚨 FRAUD TRANSACTION DETECTED
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="safe-popup">
            ✅ SAFE LEGITIMATE TRANSACTION
            </div>
            """, unsafe_allow_html=True)

        st.metric(
            "Fraud Probability",
            f"{prob*100:.2f}%"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # PIE CHART
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("📊 Fraud Distribution")

        fig = go.Figure(data=[go.Pie(
            labels=['Legitimate','Fraud'],
            values=[legit_count+1, fraud_count+1],
            hole=.4
        )])

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # TREND
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("📈 Fraud Trend")

        st.line_chart(st.session_state.history)

        st.markdown("</div>", unsafe_allow_html=True)

        # SHAP + WATERFALL
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("🧠 AI Explanation")

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X)

        feature_names = [
            "San Diego","San Jose","Philadelphia",
            "Phoenix","San Antonio","Houston",
            "Los Angeles","New York","Dallas",
            "Month","Refund","Amount",
            "MerchantID","Hour","Day"
        ]

        if isinstance(shap_values, list):
            shap_data = shap_values[-1]
        else:
            shap_data = shap_values

        shap_data = np.array(shap_data).flatten()

        shap_df = pd.DataFrame({
            "Feature": feature_names,
            "Impact": shap_data[:len(feature_names)]
        })

        shap_df = shap_df.sort_values(
            by="Impact",
            key=abs,
            ascending=False
        )

        # SHAP BAR CHART
        st.bar_chart(
            shap_df.set_index("Feature")
        )

        # WATERFALL CHART
        st.subheader("🌊 Feature Contribution Waterfall")

        top_df = shap_df.head(6)

        waterfall_fig = go.Figure(go.Waterfall(
            name="Impact",
            orientation="v",
            measure=["relative"] * len(top_df),
            x=top_df["Feature"],
            textposition="outside",
            y=top_df["Impact"],
            connector={"line":{"color":"rgb(63, 63, 63)"}}
        ))

        waterfall_fig.update_layout(
            title="Top Feature Impact Analysis",
            showlegend=False,
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text, size=14)
        )

        st.plotly_chart(
            waterfall_fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # CSV
        csv = pd.DataFrame(
            st.session_state.records
        ).to_csv(index=False)

        st.download_button(
            "⬇ Download CSV Report",
            csv,
            "fraud_report.csv",
            "text/csv"
        )

        # PDF
        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=14)

        pdf.cell(200,10,txt="Fraud Detection Report",ln=True)
        pdf.cell(200,10,txt=f"Prediction: {result}",ln=True)
        pdf.cell(200,10,txt=f"Probability: {prob*100:.2f}%",ln=True)

        pdf.output("fraud_report.pdf")

        with open("fraud_report.pdf","rb") as file:

            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="fraud_report.pdf",
                mime="application/pdf"
            )

# =========================
# FRAUD HISTORY
# =========================
if menu == "Fraud History":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📜 Fraud History")

    history_df = pd.DataFrame(
        st.session_state.records
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# AI CHATBOT
# =========================
if menu == "AI Chatbot":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🤖 Fraud AI Assistant")

    user_q = st.text_input(
        "Ask AI About Fraud"
    )

    if user_q:

        if "fraud" in user_q.lower():

            st.write(
                "🚨 AI: Suspicious transaction detected."
            )

        elif "safe" in user_q.lower():

            st.write(
                "✅ AI: Transaction seems safe."
            )

        else:

            st.write(
                "🤖 AI: Please provide more details."
            )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# LIVE SIMULATOR
# =========================
if menu == "Live Simulator":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🔄 Live Transaction Simulator")

    if st.button("Generate Live Transaction"):

        live_amount = random.randint(100,100000)

        live_hour = random.randint(0,23)

        st.write(f"💰 Amount: ₹{live_amount}")
        st.write(f"⏰ Hour: {live_hour}")

        if live_amount > 50000 and live_hour < 5:

            st.markdown("""
            <div class="fraud-popup">
            🚨 HIGH RISK TRANSACTION
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="safe-popup">
            ✅ NORMAL TRANSACTION
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


