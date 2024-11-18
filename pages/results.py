import streamlit as st
import requests

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "cropped_pic" not in st.session_state:
    st.switch_page("app.py")
st.session_state.complete = False


# layout container for header
column_1, column_2 = st.columns(2, vertical_alignment="center")

with column_1:
    st.title("Canine Classifier")

with column_2:
    if st.button("Identify another dog 🐕", use_container_width=True):
        st.switch_page("app.py")


# layout container for loading gif
left_column, center_column, last_column = st.columns(3)
with center_column:
    holder_img = st.image("images/searching.gif")


# layout container for results
results_column_1, results_column_2 = st.columns(
    2, gap="medium", vertical_alignment="top"
)

try:

    def show_results(data):
        if "url" in data:
            st.image(data["url"], use_container_width=True)
        if "bred_for" in data["breeds"][0]:
            st.caption(f"Bred for: {data['breeds'][0]['bred_for']}")
        if "temperament" in data["breeds"][0]:
            st.caption(f"Temperament: {data['breeds'][0]['temperament']}")
        if "life_span" in data["breeds"][0]:
            st.caption(f"Life span: {data['breeds'][0]['life_span']}")
        if "breed_group" in data["breeds"][0]:
            st.caption(f"Breed group: {data['breeds'][0]['breed_group']}")
        if "weight" in data["breeds"][0]:
            st.caption(f"Weight: {data['breeds'][0]['weight']['metric']}kg")
        if "height" in data["breeds"][0]:
            st.caption(f"Height: {data['breeds'][0]['height']['metric']}cm")

    def show_results_2(data):
        st.image(data[0]["image_link"], use_container_width=True)

    # use model inference to get results
    url = f"{st.secrets['CANINE_API_URL']}/upload_image"
    files = {"img": st.session_state.cropped_pic}
    response = requests.post(url, files=files, timeout=10000)
    data = response.json()
    holder_img.empty()  # remove loader gif
    st.session_state.complete = True

    with results_column_1:
        container = st.container(border=True)
        container.subheader("This dog's most likely breeds are:")

    with results_column_2:
        container = st.container(border=True)
        container.image(
            st.session_state.cropped_pic,
            use_container_width=True,
            caption="Your uploaded image",
        )
        container.image(
            f"{st.secrets['CANINE_API_URL']}{data[0]['gradcam']}",
            use_container_width=True,
            caption="Most relevant sections of the image marked using Gradient-weighted Class Activation Mapping (Grad-CAM):",
        )

    for index, breed in enumerate(data):
        if breed["breedNames"] == "Others":
            if index < 1:
                with results_column_1.expander(
                    f"{breed['prob']}% {breed['breedNames']}", expanded=True
                ):
                    st.image("images/question.gif")
            else:
                with results_column_1.expander(
                    f"{breed['prob']}% {breed['breedNames']}"
                ):
                    st.image("images/question.gif")

        if breed["referenceImageId"]:
            response = requests.get(
                f"https://api.thedogapi.com/v1/images/{breed['referenceImageId']}",
                headers={"Authorization": f"Bearer {st.secrets['THE_DOG_API_KEY']}"},
                timeout=10000,
            )
            response.raise_for_status()
            data = response.json()

            if index < 1:
                with results_column_1.expander(
                    f"{breed['prob']}% {breed['breedNames']}", expanded=True
                ):
                    show_results(data)
            else:
                with results_column_1.expander(
                    f"{breed['prob']}% {breed['breedNames']}"
                ):
                    show_results(data)

        if breed["referenceImageId"] == None:
            if breed["breedNames"] == "It doesn't look like a dog!":
                with results_column_1.expander(f"{breed['breedNames']}", expanded=True):
                    st.image("images/snoop_dogg.gif")
            else:
                response = requests.get(
                    f"https://api.api-ninjas.com/v1/dogs?name={breed['breedNames']}",
                    headers={"X-Api-Key": f"{st.secrets['NINJA_DOGS_API_KEY']}"},
                    timeout=10000,
                )
                response.raise_for_status()
                data = response.json()

                if data:
                    if index < 1:
                        with results_column_1.expander(
                            f"{breed['prob']}% {breed['breedNames']}", expanded=True
                        ):
                            show_results_2(data)
                    else:
                        with results_column_1.expander(
                            f"{breed['prob']}% {breed['breedNames']}"
                        ):
                            show_results_2(data)

except requests.exceptions.RequestException as e:
    print(e)
