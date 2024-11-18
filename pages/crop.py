import streamlit as st
from streamlit_cropperjs import st_cropperjs

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if 'uploaded_file' not in st.session_state:
    st.switch_page("app.py")

# row1 = st.columns(2)
# with row1[0]:
st.title("Canine Classifier")

# st.session_state.cropped_pic = st.session_state.uploaded_file
# st.switch_page("pages/results.py")

# st.write("")

def select_borders(uploaded_file):
    st.write("Draw borders around your dog")
    cropped_pic = st_cropperjs(pic=uploaded_file, btn_text="Identify dog", key='cropper' )
    if cropped_pic:
        st.session_state.cropped_pic = cropped_pic
        st.switch_page("pages/results.py")


try:
    select_borders(st.session_state.uploaded_file)
except Exception as e:
    print(e)
    st.switch_page("pages/upload.py")
