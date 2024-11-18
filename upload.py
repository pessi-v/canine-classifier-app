import streamlit as st
MAX_FILE_SIZE = 5 * 1024 * 1024  # 6MB

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)
with open("styles/main.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

for key in st.session_state.keys():
    del st.session_state[key]



column_1, column_2 = st.columns(2, gap="medium", vertical_alignment="bottom")

# column 1
with column_1:

    st.title("Canine Classifier")
    st.subheader("Identify a dog's breed!")
    upload = st.file_uploader("Upload an image of a dog", label_visibility='hidden', type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    enable = st.checkbox("Enable webcam input")
    camera = st.camera_input("Take a picture of a dog with your webcam", label_visibility="visible", disabled=not enable)

# column 2
with column_2:
    st.image("images/orange_doggo.png", use_container_width=True)

if upload is not None:
    if upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        st.session_state.upload = upload.read()

        st.switch_page("pages/crop.py")

if camera is not None:
    if camera.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        st.session_state.upload = camera.read()
        st.switch_page("pages/crop.py")
