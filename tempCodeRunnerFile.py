import Streamlit as st
import pickle
import pandas as pd

                                        ## To Add External CSS ##
with open('css/style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




                                        ## Application Backend ##

                    # To load medicine-dataframe from pickle in the form of dictionary
medicines_dict = pickle.load(open('./pickle_files/medicine_dict.pkl','rb'))
medicines = pd.DataFrame(medicines_dict)

                    # To load similarity-vector-data from pickle in the form of dictionary
similarity = pickle.load(open('./pickle_files/similarity.pkl','rb'))

with open('./pickle_files/collab_filtering.pkl', 'rb') as file:
    collab_filtering_data = pickle.load(file)

# Extract the components
reader = collab_filtering_data["reader"]
model_collab = collab_filtering_data["model_collab"]
user_item_interactions = collab_filtering_data["user_item_interactions"]

def recommend(medicine):
     medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
     distances = similarity[medicine_index]
     medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

     recommended_medicines = []
     for i in medicines_list:
         recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
     return recommended_medicines



def collaborative_filtering_recommendations(user_id, n=5):
    # Get the list of medicines that the user has not interacted with
    medicines_not_interacted = user_item_interactions[~user_item_interactions['Drug_Name'].isin(user_item_interactions[user_item_interactions['User_ID'] == user_id]['Drug_Name'])]['Drug_Name'].unique()
    
    # Predict ratings for uninteracted medicines
    predictions = []
    for medicine in medicines_not_interacted:
        predicted_score = model_collab.predict(user_id, medicine).est
        predictions.append((medicine, predicted_score))
    
    # Sort predictions by estimated score and get the top N recommendations
    top_n_recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    
    return [medicine for medicine, _ in top_n_recommendations]


def hybrid_recommendations(user_id, medicine_name, n=5):
    # Content-based recommendations
    content_recommendations = recommend(medicine_name)
    # Collaborative filtering recommendations
    collab_recommendations = collaborative_filtering_recommendations(user_id, n)
    
    content_recommendations=list(content_recommendations)
    hybrid_recommendations=content_recommendations
    if collab_recommendations is not None:
        hybrid_recommendations = content_recommendations + collab_recommendations
    
    # Deduplicate and return the top N recommendations
    top_n_recommendations = list(set(hybrid_recommendations))[:n]
    
    return top_n_recommendations




                                    ## Appliaction Frontend ##

                                   # Title of the Application
st.title('Medicine Recommender System')

                                        # Searchbox
selected_medicine_name = st.selectbox(
'Type your medicine name whose alternative is to be recommended',
     medicines['Drug_Name'].values)
selected_user_name = st.selectbox(
'Select the userId 1-100',range(1,101))


                                   # Recommendation Program
if st.button('Recommend Medicine'):
     recommendations = hybrid_recommendations(selected_user_name, selected_medicine_name)
     j=1
     for i in recommendations:
          st.write(j,i)                      # Recommended-drug-name
          # st.write("Click here -> "+" https://www.netmeds.com/catalogsearch/result?q="+i) # Recommnded drug purchase link from netmeds
          st.write("Click here -> "+" https://pharmeasy.in/search/all?name="+i) # Recommnded-drug purchase link from pharmeasy
          j+=1



                                         ## Image load ##
from PIL import Image
image = Image.open('images/medicine-image.jpg')
st.image(image, caption='Recommended Medicines')


