import streamlit as st
import requests

st.set_page_config(
    page_title="Canine Classifier",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

### FUNCTIONS ###

def get_model_data():
  try:
    url = f"{st.secrets['CANINE_API_URL']}/upload_image"
    files = {'img': st.session_state.cropped_pic}
    response = requests.post(url, files=files, timeout=10000)
    data = response.json()
    return data 
  except requests.exceptions.RequestException as e:
    print(e)

def get_the_dog_api_data(breed):
  # use hardcoded referenceImageId specific to thedogapi.com, supplied by the model API
  response = requests.get(
    f"https://api.thedogapi.com/v1/images/{breed['referenceImageId']}",
    headers={"Authorization": f"Bearer {st.secrets['THE_DOG_API_KEY']}"},
    timeout=10000)
  response.raise_for_status()
  data = response.json()
  return data

def get_api_ninjas_data(breed):
  response = requests.get(
    f"https://api.api-ninjas.com/v1/dogs?name={breed['breedNames']}",
    headers={"X-Api-Key": f"{st.secrets['NINJA_DOGS_API_KEY']}"},
    timeout=10000)
  response.raise_for_status()
  api_ninjas_data = response.json()
  return api_ninjas_data[0]

def show_enriched_results(the_dog_api_data):
  if 'url' in the_dog_api_data:
    st.image(the_dog_api_data['url'], use_container_width=True)
  if 'bred_for' in the_dog_api_data['breeds'][0]:
    st.caption(f"Bred for: {the_dog_api_data['breeds'][0]['bred_for']}")
  if 'temperament' in the_dog_api_data['breeds'][0]:
    st.caption(f"Temperament: {the_dog_api_data['breeds'][0]['temperament']}")
  if 'life_span' in the_dog_api_data['breeds'][0]:
    st.caption(f"Life span: {the_dog_api_data['breeds'][0]['life_span']}")
  if 'breed_group' in the_dog_api_data['breeds'][0]:
    st.caption(f"Breed group: {the_dog_api_data['breeds'][0]['breed_group']}")
  if 'weight' in the_dog_api_data['breeds'][0]:
    st.caption(f"Weight: {the_dog_api_data['breeds'][0]['weight']['metric']}kg")
  if 'height' in the_dog_api_data['breeds'][0]:
    st.caption(f"Height: {the_dog_api_data['breeds'][0]['height']['metric']}cm")
  st.caption("added data from thedogapi.com")

def show_api_ninjas_results(api_ninjas_data):
  st.image(api_ninjas_data['image_link'], use_container_width=True)
  for info, value in api_ninjas_data.items():
    if isinstance(value, int):
      st.caption(f"{info.replace("_", " ").capitalize()}: {value}/5")
    elif isinstance(value, float):
      st.caption(f"{info.replace("_", " ").capitalize()}: {value}")
  st.caption("added data from api-ninjas.com")

### ###


# image upload failed
if 'cropped_pic' not in st.session_state:
  st.switch_page("app.py")


### LAYOUTS ###
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
  loading_gif = st.image(
    "images/searching.gif",
    caption="Inference might take a while, if the API server is not yet running. Hold on",
  )

# layout container for results
results_column_1, results_column_2 = st.columns(
    2, gap="medium", vertical_alignment="top"
)


### GET AND SHOW DATA ###
model_data = get_model_data()
loading_gif.empty()

# show cropped image and gradcam image
with results_column_2:
  container = st.container(border=True)
  container.image(
    st.session_state.cropped_pic,
    use_container_width=True,
    caption="Your uploaded image",
  )
  container.image(
    f"{st.secrets['CANINE_API_URL']}{model_data[0]['gradcam']}",
    use_container_width=True,
    caption="Most relevant sections of the image marked using Gradient-weighted Class Activation Mapping (Grad-CAM):",
  )


# Show results!
results_column_1.subheader("Your dogs most likely breeds are:")
for index, breed in enumerate(model_data):

  # "Other" breeds
  if breed['breedNames'] == "Others":
    is_only_result = index == 0
    with results_column_1.expander(f"{breed['prob']}% {breed['breedNames']}", expanded = is_only_result):
      st.image("images/question.gif")

  # Model doesn't identify a dog
  if breed['referenceImageId'] == None and breed['breedNames'] == "It doesn't look like a dog!":
    with results_column_1.expander(f"{breed['breedNames']}", expanded=True):
      st.image('images/snoopy.jpg')

  # Identified breeds
  if breed['referenceImageId']:
    the_dog_api_data = get_the_dog_api_data(breed)
    is_first_result = index == 0
    with results_column_1.expander(f"{breed['prob']}% {breed['breedNames']}", expanded = is_first_result):
      show_enriched_results(the_dog_api_data)

  # there is no known reference image id for The Dog Api, so we ask api-ninjas for details with breed name
  if breed['referenceImageId'] == None and breed['breedNames'] != 'Others':
    api_ninjas_data = get_api_ninjas_data(breed)
    if api_ninjas_data:
      is_only_result = index == 0 
      with results_column_1.expander(f"{breed['prob']}% {breed['breedNames']}", expanded = is_only_result):
        show_api_ninjas_results(api_ninjas_data)
