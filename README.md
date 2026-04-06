import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Page Config
st.set_page_config(page_title="Tesfa Berhan VSLA", layout="wide")

# የድርጅቱ ስም እና መግለጫ
st.title("📊 VSLA መከታተያ - Google Sheets ስሪት")
st.subheader("የተስፋ ብርሃን ህፃናትና ቤተሰብ ልማት ድርጅት")
 
sheet_url = ](https://docs.google.com/spreadsheets/d/1vOt20fbuc-XBj-iKifiJmYABe5Cs5-A6u-pnmHQIdJc/edit?gid=0#gid=0)"
conn = st.connection("gsheets", type=GSheetsConnection)

# መረጃ መቀበያ ፎርም
with st.sidebar.form("vsla_form"):
    st.header("አዲስ መረጃ መመዝገቢያ")
    g_no = st.number_input("የቡድን ቁጥር", min_value=1)
    g_name = st.text_input("የቡድኑ ስም")
    active_m = st.number_input("ንቁ አባላት", min_value=0)
    savings = st.number_input("ጠቅላላ ቁጠባ", min_value=0.0)
    loan = st.number_input("ጠቅላላ ብድር", min_value=0.0)
    capital = st.number_input("ጠቅላላ ካፒታል", min_value=0.0)
    
    submitted = st.form_submit_button("መረጃውን ወደ Google Sheet ላክ")

if submitted:
    # አዲስ ዳታ ማዘጋጀት
    new_data = pd.DataFrame([{
        "Date": str(date.today()),
        "Group_No": g_no,
        "Group_Name": g_name,
        "Active_Members": active_m,
        "Total_Savings": savings,
        "Total_Loan": loan,
        "Total_Capital": capital
    }])
    
    # የቆየውን ዳታ ማንበብ
    existing_data = conn.read(spreadsheet=sheet_url)
    
    # አዲሱን ዳታ ከቆየው ጋር መቀላቀል
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    
    # ወደ Google Sheet መመለስ (Update ማድረግ)
    conn.update(spreadsheet=sheet_url, data=updated_df)
    st.success("መረጃው በቋሚነት በ Google Sheet ላይ ተቀምጧል!")

# መረጃውን ከአፑ ላይ ለማየት
st.write("### በአሁኑ ሰዓት በሺቱ ላይ ያለው መረጃ")
data = conn.read(spreadsheet=sheet_url)
st.dataframe(data, use_container_width=True)
