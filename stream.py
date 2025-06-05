import streamlit as st
import pandas as pd
import os
from main import Data_Mining

CSV_PATH = r"C:\Users\Elyar\Desktop\linkdin-job-information\job_data.csv"

st.set_page_config(page_title="LinkedIn Job Scraper", layout="wide")
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

    # ===========================
    # 🎛️ فیلترهای تعاملی
    # ===========================
    with st.expander("🔧 فیلتر نتایج"):
        location_filter = st.multiselect("🌍 انتخاب موقعیت مکانی", df["Location"].dropna().unique())
        company_filter = st.multiselect("🏢 انتخاب شرکت", df["Company"].dropna().unique())
        title_search = st.text_input("🔎 جستجو در عنوان شغلی")

    filtered_df = df.copy()
    if location_filter:
        filtered_df = filtered_df[filtered_df["Location"].isin(location_filter)]
    if company_filter:
        filtered_df = filtered_df[filtered_df["Company"].isin(company_filter)]
    if title_search:
        filtered_df = filtered_df[filtered_df["Title"].str.contains(title_search, case=False, na=False)]

    st.metric("📊 تعداد مشاغل بعد از فیلتر", len(filtered_df))

    # ===========================
    # 📈 نمودار آماری ساده
    # ===========================
    with st.expander("📊 نمودارهای آماری"):
        location_count = filtered_df['Location'].value_counts().head(10)
        st.bar_chart(location_count)

    # ===========================
    # 📋 جدول نتایج با لینک
    # ===========================
    def make_clickable(link):
        return f'<a href="{link}" target="_blank">مشاهده در لینکدین</a>'

    filtered_df['لینک'] = filtered_df['Link'].apply(make_clickable)
    st.write("### 📄 نتایج شغلی")
    st.write(filtered_df[['Title', 'Company', 'Location', 'Salary', 'لینک']].to_html(escape=False, index=False), unsafe_allow_html=True)

    # ===========================
    # 📤 دکمه دانلود
    # ===========================
    st.download_button(
        label="⬇️ دانلود نتایج فیلتر شده",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_jobs.csv",
        mime="text/csv"
    )
