import streamlit as st
MAX_FILE_SIZE = 5 * 1024 * 1024  # 6MB

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

for key in st.session_state.keys():
    del st.session_state[key]



column_1, column_2 = st.columns(2, gap="medium", vertical_alignment="bottom")

# column 1
with column_1:

    st.title("Canine Classifier")
    st.subheader("Identify a dog's breed!")
    uploaded_file = st.file_uploader("Upload an image of a dog", label_visibility='hidden', type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    enable = st.checkbox("Enable webcam input")
    camera_input = st.camera_input("Take a picture of a dog with your webcam", label_visibility="visible", disabled=not enable)

# column 2
with column_2:
    st.image("images/orange_doggo.png", use_container_width=True)

# explainer box
explainer = st.container(border=True)
with explainer:
    st.write("""This app uses an EfficientNet V2s, a type of Vision Transformer Machine Learning model,
    to output probabilities of a type of dog breed in any given image. You can upload a photo of your dog,
    or take a webcam shot of yourself to see if the algorithm thinks it 'sees' a poodle, a schnautzer, or a labby.
    You can find the code for the project at https://github.com/pessi-v/canine-classifier-app""")



if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        st.session_state.uploaded_file = uploaded_file.read()
        st.switch_page("pages/crop.py")

if camera_input is not None:
    if camera_input.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        st.session_state.uploaded_file = camera_input.read()
        st.switch_page("pages/crop.py")
