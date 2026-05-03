import os
from model import Model
from controller import Controller
from view import View

import streamlit as st

st.set_page_config(
    page_title="Evolution des décès COVID-19", layout="wide",)

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader('Parameters')
    my_file = st.file_uploader('Choose a CSV file',
                               type=['csv'],
                               help = "Choose a csv file containing the data."
                               )
    department = st.number_input('Department', min_value=1, max_value=90, value=75)
    start_date = st.date_input("start date", value=None)
    end_date = st.date_input("end date", value=None)
    print_graph = st.button("Run")
    if st.button("Exit"):
        os.kill(os.getpid(), 9)

with col1:
    st.subheader('Visualisation')
    if print_graph:
        if my_file:
            model = Model(my_file)
            data = Controller.select_data(model.data, start=start_date, end=end_date)
            fig = View.get_figure(data)
            st.pyplot(fig)
        else:
            st.error('Please select a file')
    else:
        st.info('Click on Run to visualize the graph')
