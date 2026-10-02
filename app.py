import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Friends Finder", layout="wide")

# Make all column names small so Name/name both work
@st.cache_data
def load_data():
    df = pd.read_csv("database.csv")
    # Make columns lowercase and trim spaces
    df.columns = [c.strip().lower() for c in df.columns]
    # Make all data lowercase for searching but keep original display
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Sidebar - Our Gang
st.sidebar.title("👭 Our Gang - 8 Members")
for i, name in enumerate(df['name'], 1):
    st.sidebar.write(f"{i}. {name}")

# Main Title
st.title("👫 Friends Finder - Enter Name → Get Photo & Details")
st.write("BTech 3rd Year Project | By Bhoomika")

# Search Box
col1, col2 = st.columns([3,1])
with col1:
    search = st.text_input("Type Name Here:", placeholder="e.g. Bhoomika")
with col2:
    option = st.selectbox("Or Select from List:", ["Choose an option"] + df['name'].tolist())

query = option if option!= "Choose an option" else search

if query:
    # Case-insensitive search
    result = df[df['name'].str.lower() == query.strip().lower()]

    if not result.empty:
        row = result.iloc[0]
        st.success(f"Found: {row['name']}")

        c1, c2 = st.columns([1,2])
        with c1:
            photo_path = row['photo']
            if os.path.exists(photo_path):
                st.image(photo_path, caption=row['name'], width=250)
            else:
                st.warning(f"Add photo: {photo_path}")
                st.info(f"Add {row['name']} in photos folder")

        with c2:
            st.subheader(f"Details of {row['name']}")
            st.write(f"**Name:** {row['name']}")
            st.write(f"**Roll No:** {row['rollno']}")
            st.write(f"**Branch:** {row['branch']}")
            st.write(f"**Year:** {row['year']}")
            st.write(f"**Hobby:** {row['hobby']}")
            if st.button(f"Say Hi to {row['name']} 👋"):
                st.balloons()
                st.success(f"Hi {row['name']}! From Bhoomika's Project!")
    else:
        st.error(f"Not Found: {query}. Try from list.")