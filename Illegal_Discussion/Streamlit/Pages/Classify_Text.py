import streamlit as st
from streamlit.components.v1 import html


def Predict_text():

    prediction_col1,prediction_col2 = st.columns(spec=(1,1),gap="large")

    with prediction_col1:
        st.title("General Guideline🗒️")

        Prediction_page_intro = ("<p style='font-size: 22px;'>This model can help you to classify whether or not the content posted by individuals on social media groups is illegal. To do this, you need to paste the text you want to check into the section below. If you do not have access to any such content, then below are the 5 most common social media sites that have short or long form text content that you can use as query input data.You can also use this model to classify text from other sources, such as news articles, blog posts, or even emails. However, it is important to note that this model is still under development, and it may not be able to accurately classify all types of content.</p>")
        st.markdown(Prediction_page_intro, unsafe_allow_html=True)
        st.markdown("***")

        site_col1, site_col2,site_col3,site_col4,site_col5 = st.columns(spec=(1,1,1,1,1), gap="medium")
        with site_col1:
            st.link_button(label="Quora", url="https://www.quora.com/")
        with site_col2:
            st.link_button(label="Reddit", url = "https://www.reddit.com/?rdt=35863")
        with site_col3:
            st.link_button(label="Linkedin", url = "https://www.linkedin.com/signup/cold-join?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&trk=login_reg_redirect")
        with site_col4:
            st.link_button(label="Twitter", url = "https://twitter.com/")
        with site_col5:
            st.link_button(label="Facebook", url = "https://www.facebook.com/")

        # Taking text input from the user
        st.markdown("***")
        User_Input = st.text_input(label="Insert the text which you want to classify", key='user_input_text')


    with prediction_col2:
        st.image("/home/yuvraj/Github/Deep_Learning_Projects/Illegal_Discussion/Prediction_Img.png")

