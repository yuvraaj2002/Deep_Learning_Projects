import streamlit as st
from Pages.Classify_Text import Predict_text
from Pages.Insights import Insights_func

st.set_page_config(
    page_title = "Talks",
    page_icon = "🏠",
    layout="wide",
    initial_sidebar_state= "collapsed"
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

def Home_Page():

    col1,col2 = st.columns(spec=(1,1), gap="large")
    with col1:
        st.title("Unveiling the Unlawful")
        st.write("")
        Intro_text1 = ("<p style='font-size: 22px;'>IThe old woman sat on the park bench, feeding the pigeons. She had been coming to this park every day for as long as she could remember. She loved watching the pigeons, with their plump bodies and cooing sounds. They reminded her of a simpler time, when life was slower and more peaceful. The old woman closed her eyfe.</p>")
        st.markdown(Intro_text1, unsafe_allow_html=True)

        st.write("")
        Intro_text2 = (
            "<p style='font-size: 22px;'>IThe old woman sat on the park bench, feeding the pigeons. She had been coming to this park every day for as long as she could remember. She loved watching the pigeons, witheep breath. She could smell the fresh air and the flowers blooming in the park. She could hear the birds singing and the children playing in the distance. She felt a sense of contentment and peace.She opened her eyes and smiled at the pigeons. She was grateful for this moment, and for all the good things in her life.</p>")
        st.markdown(Intro_text2, unsafe_allow_html=True)
        st.markdown("***")


        # Creating toggle for the dataset link and the github link
        dataset_toggle = st.toggle('Dataset Used')
        if dataset_toggle:
            st.write('Feature activated!')

        github_toggle = st.toggle('Project Github Link')
        if github_toggle:
            st.write('Feature activated!')


    with col2:
        st.image('/home/yuvraj/Github/Deep_Learning_Projects/Illegal_Discussion/Home_Img.png')



page_names_to_funcs = {
    "Project Overview 📑": Home_Page,
    "Classify Text 🤔": Predict_text,
    "Insights📊" : Insights_func,
}
selected_page = st.sidebar.selectbox("Select Module", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
# Home_Page()