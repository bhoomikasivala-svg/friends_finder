import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Friends Finder", page_icon="👭", layout="wide")
st.title("👭 Friends Finder - Enter Name -> Get Photo & Details")
st.write("**BTech 3rd Year Project | By Bhoomika**")

def load_database():
    try:
        df = pd.read_csv("database.csv")
        return df
    except:
        st.error("database.csv file not found!")
        return pd.DataFrame()

df = load_database()

if not df.empty:
    st.sidebar.title("👭 Our Gang - 8 Members")
    for i, name in enumerate(df["name"].tolist(), 1):
        st.sidebar.write(f"{i}. {name}")

    st.subheader("🔍 Search Your Friend")
    col1, col2 = st.columns([2,1])
    with col1:
        search_name = st.text_input("Type Name Here:", placeholder="e.g., Bhoomika")
    with col2:
        option = st.selectbox("Or Select from List:", [""] + df["name"].tolist())

    final_search = search_name.strip() if search_name.strip() != "" else option

    if final_search:
        matched = df[df["name"].str.lower() == final_search.lower()]
        if matched.empty:
            matched = df[df["name"].str.lower().str.contains(final_search.lower())]

        if matched.empty:
            st.error(f"'{final_search}' not found!")
        else:
            for idx, person in matched.iterrows():
                st.write("---")
                st.success(f"Found: {person['name']}")
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    photo_path = f"photos/{person['photo']}"
                    if os.path.exists(photo_path):
                        image = Image.open(photo_path)
                        st.image(image, caption=f"{person['name']}", width=300)
                    else:
                        st.warning(f"Add photo: {photo_path}")
                        st.info(f"Add {person['photo']} in photos folder")
                with c2:
                    st.subheader(f"Details of {person['name']}")
                    st.write(f"Name: {person['name']}")
                    st.write(f"Roll No: {person['roll_no']}")
                    st.write(f"Branch: {person['branch']}")
                    st.write(f"Year: {person['year']}")
                    st.write(f"Phone: {person['phone']}")
                    st.write(f"Email: {person['email']}")
                    st.write(f"Hobby: {person['hobby']}")
                    if st.button(f"Say Hi to {person['name']}", key=person['name']):
                        st.balloons()

    st.write("---")
    st.subheader("All 8 Friends")
    cols = st.columns(4)
    for i, (idx, person) in enumerate(df.iterrows()):
        with cols[i % 4]:
            photo_path = f"photos/{person['photo']}"
            if os.path.exists(photo_path):
                st.image(Image.open(photo_path), width=120, caption=person['name'])
            else:
                st.write(f"{person['name']}")
                st.write("Add photo")