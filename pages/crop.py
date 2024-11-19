import streamlit as st
from streamlit_cropperjs import st_cropperjs
from streamlit_cropper import st_cropper
from PIL import Image
import io

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "uploaded_file" not in st.session_state:
    st.switch_page("app.py")

st.title("Canine Classifier")


def select_borders(uploaded_file):
    st.write("Draw borders around your dog")
    cropped_pic = st_cropperjs(
        pic=uploaded_file, btn_text="Identify dog", key="cropper"
    )
    if cropped_pic:
        st.session_state.cropped_pic = cropped_pic
        st.switch_page("pages/results.py")

def select_borders_2(uploaded_file):
    # breakpoint()
    # img = Image.open(uploaded_file)
    img = Image.open(io.BytesIO(uploaded_file))
    cropped_img = st_cropper(
        img,
        realtime_update=True,
        aspect_ratio=None)

    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)
    st.session_state.cropped_pic = cropped_img
    if st.button("Identify", use_container_width=True):
        st.switch_page("pages/results.py")
    # st.page_link("pages/results.py", label="Identify")

try:
    # select_borders(st.session_state.uploaded_file)
    select_borders_2(st.session_state.uploaded_file)
except Exception as e:
    print(e)
    st.switch_page("app.py")
