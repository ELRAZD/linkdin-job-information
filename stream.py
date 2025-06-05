import streamlit as st
import pandas as pd
import os
from main import Data_Mining

CSV_PATH = r"C:\Users\Elyar\Desktop\linkdin-job-information\job_data.csv"

st.set_page_config(page_title="LinkedIn Job Scraper", layout="centered")
st.title("🔍 جستجوی زنده آگهی‌های شغلی LinkedIn")

with st.form("job_form"):
    job_title = st.text_input("🔤 عنوان شغل", value="java")
    location = st.text_input("📍 مکان", value="germany")
    count = st.number_input("📦 تعداد آگهی‌ها برای استخراج", min_value=1, value=50)
    submitted = st.form_submit_button("🚀 شروع جستجو و استخراج")

if submitted:
    scraper = Data_Mining()
    try:
        with st.spinner("🧭 در حال راه‌اندازی مرورگر..."):
            scraper.setup_driver()


        with st.expander("🔐 مرحله ورود به LinkedIn", expanded=True):
            st.markdown("✅ لطفاً در مرورگر بازشده وارد حساب LinkedIn خود شوید و کپچا را حل کنید.")
            st.code("⏳ منتظر بمانید تا بعد از ورود به صفحه اصلی LinkedIn بروید...")


        scraper.login()

        with st.spinner("🔎 در حال جستجوی شغل..."):
            scraper.jobs(job_title, location)

        with st.spinner("📥 در حال استخراج اطلاعات..."):
            scraper.job_scraper(count)

        st.success("✅ استخراج با موفقیت انجام شد!")

    except Exception as e:
        st.error(f"❌ خطا در فرآیند استخراج: {e}")

    finally:
        try:
            scraper.driver.quit()
        except:
            pass


if os.path.exists(CSV_PATH):
    st.subheader("📋 نتایج استخراج شده:")
    df = pd.read_csv(CSV_PATH)
    st.dataframe(df, use_container_width=True)