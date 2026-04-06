import streamlit as st
import pandas as pd
from datetime import date
import os

# የአፑ ርዕስ እና ገጽታ 설정
st.set_page_config(page_title="የተስፋ ብርሃን VSLA መከታተያ", layout="wide")

# --- Sidebar (የጎን ክፍል) ---
# የድርጅቱ ሎጎ (ፋይሉ ካለ ስሙን እዚህ ይተኩ፣ ለምሳሌ "logo.png")
logo_path = "logo.png" 
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=200)
else:
    st.sidebar.warning("⚠️ ሎጎው አልተገኘም (logo.png)")

st.sidebar.header("📋 አዲስ የቡድን መረጃ መመዝገቢያ")

# --- Main Page (ዋናው ገጽ) ---
st.title("📊 ሙሉ የቁጠባና ብድር ቡድን (VSLA) መከታተያ አፕ")
st.subheader("የተስፋ ብርሃን ህፃናትና ቤተሰብ ልማት ድርጅት")
st.info("ይህ አፕ በፎቶው ላይ ያለውን ፎርም መሰረት በማድረግ የተዘጋጀ የቡድን መረጃ መከታተያ ነው።")
st.markdown("---")

# መረጃ መቀበያ ክፍል (Sidebar Form)
with st.sidebar.form("vsla_form", clear_on_submit=True):
    st.subheader("1. መሰረታዊ መረጃ")
    group_no = st.number_input("የቡድን ቁጥር (Group No)", min_value=1)
    group_name = st.text_input("የቡድኑ ስም (Name of Group)")
    est_date = st.date_input("የተመሰረተበት ቀን (Date of Establishment)")
    
    st.subheader("2. የአባላት ሁኔታ")
    total_members_start = st.number_input("የመጀመሪያ የአባላት ብዛት", min_value=0)
    active_members = st.number_input("ንቁ አባላት", min_value=0)
    dropout_members = st.number_input("የለቀቁ አባላት", min_value=0)
    new_members = st.number_input("አዲስ አባላት", min_value=0)

    st.subheader("3. ቁጠባ (Savings)")
    savings_this_qtr = st.number_input("የዚህ ሩብ ዓመት ቁጠባ", min_value=0.0)
    savings_upto_qtr = st.number_input("እስከዚህ ሩብ ዓመት ጠቅላላ ቁጠባ", min_value=0.0)

    st.subheader("4. ብድር (Loan)")
    loan_this_qtr = st.number_input("የዚህ ሩብ ዓመት ብድር", min_value=0.0)
    loan_upto_qtr = st.number_input("እስከዚህ ሩብ ዓመት ጠቅላላ ብድር", min_value=0.0)

    st.subheader("5. የመለስ ብድር ብዛት/መጠን")
    repaid_no_this_qtr = st.number_input("የዚህ ሩብ ዓመት መለስ ብዛት", min_value=0)
    repaid_amt_this_qtr = st.number_input("የዚህ ሩብ ዓመት መለስ መጠን", min_value=0.0)

    st.subheader("6. ክፍያዎችና ካፒታል")
    service_fee = st.number_input("ጠቅላላ የአገልግሎት ክፍያ", min_value=0.0)
    penalty = st.number_input("ጠቅላላ ቅጣት", min_value=0.0)
    social_fund = st.number_input("ጠቅላላ ማህበራዊ ፈንድ", min_value=0.0)
    total_capital = st.number_input("ጠቅላላ ካፒታል (Total Capital)", min_value=0.0)

    submitted = st.form_submit_button("መረጃውን መዝግብ")

# መረጃውን ለማስቀመጥ (Session State)
if "vsla_data" not in st.session_state:
    st.session_state.vsla_data = []

if submitted:
    new_entry = {
        "ቀን": date.today(),
        "ቡድን ቁጥር": group_no,
        "የቡድኑ ስም": group_name,
        "ንቁ አባላት": active_members,
        "ጠቅላላ ቁጠባ": savings_upto_qtr,
        "ጠቅላላ ብድር": loan_upto_qtr,
        "ጠቅላላ ካፒታል": total_capital
    }
    st.session_state.vsla_data.append(new_entry)
    st.success(f"የቡድን '{group_name}' መረጃ በትክክል ተመዝግቧል!")

# የተመዘገቡ መረጃዎችን ሰንጠረዥ ማሳያ
st.header("📋 የተመዘገቡ የቡድን መረጃዎች")
if st.session_state.vsla_data:
    df = pd.DataFrame(st.session_state.vsla_data)
    st.dataframe(df, use_container_width=True)
    
    # ዳታውን ወደ Excel/CSV ለማውረድ
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("ዳታውን በ CSV አውርድ", csv, "vsla_data.csv", "text/csv")
else:
    st.write("እስካሁን ምንም የተመዘገበ መረጃ የለም።")

st.markdown("---")
st.caption("© 2026 የተስፋ ብርሃን ህፃናትና ቤተሰብ ልማት ድርጅት - VSLA Tracking System")