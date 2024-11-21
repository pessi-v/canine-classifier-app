import streamlit as st
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

# layout
left_column, right_column = st.columns(2, vertical_alignment="top")


def image_cropper(uploaded_file):
    with left_column:
        st.write("Draw borders around your dog")
        img = Image.open(io.BytesIO(uploaded_file))
        cropped_img = st_cropper(
            img,
            realtime_update=True,
            aspect_ratio=None)

    with right_column:
        st.write("Preview")
        _ = cropped_img.thumbnail((150,150))
        st.image(cropped_img)
        if st.button("Identify dog", use_container_width=False):
            buf = io.BytesIO()
            cropped_img.save(buf, format='JPEG')
            st.session_state.cropped_pic = buf.getvalue()
            st.switch_page("pages/results.py")

try:
    image_cropper(st.session_state.uploaded_file)
except Exception as e:
    print(e)
    st.switch_page("app.py")
