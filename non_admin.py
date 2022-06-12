import streamlit as st
import pandas as pd
from deta import Deta
deta = Deta(st.secrets["deta_key"])
db = deta.Base("example-db")
data = db.fetch().items

def test_function():
    st.subheader('Test')
    st.write('Hello World')
    

def non_admin_view():
    # users only
    user_menu = ['Select','None', 'View', 'Edit', 'Delete']
    user_choice = st.sidebar.selectbox('Select an option', user_menu)
    if user_choice == 'View':
        st.subheader('View your details')
        data_df = pd.DataFrame(data)
        st.table(data_df)
    
    

        db_content = db.fetch().items

        df = pd.DataFrame(db_content)
        # df.to_excel("example.xlsx")
        menu_data = df['name'].unique()
        option = st.selectbox('Select a name', menu_data)
        st.table(df[df['name'] == option])
        st.table(df)
    
        selected_index = st.multiselect("Select a column", df.columns)

        if selected_index:
            st.write(df[selected_index])
            print(df[selected_index])