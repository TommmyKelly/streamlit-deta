from turtle import width
import streamlit as st
from deta import Deta
import streamlit_authenticator as stauth
import pandas as pd
import bcrypt
import base64
import io



# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
users = deta.Base("users")

user_details = users.fetch().items

names = [user["name"] for user in user_details]
usernames = [user["email"] for user in user_details]
password = [user['password'] for user in user_details]




authenticator = stauth.Authenticate(names, usernames, password,'cookie_name','signature_key',cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login','main')


 # your application
if authentication_status == False:
    st.error('Username/password is incorrect')
    print(password)
if authentication_status == None:
    st.warning('Please enter your username and password')
if authentication_status:
    st.write('Welcome *%s*' % (name))
    authenticator.logout('logout')
    admin_status = users.fetch({'email': username}).items[0]['admin']
    print(admin_status)
    # print(f"{name} {authentication_status} {username}")
    if admin_status == True:
        st.header('Admin Dashboard')
        st.write('This is an admin dashboard')



    menu = ['Select','Add', 'View', 'Edit', 'Delete']

    choice = st.sidebar.selectbox('Select an option', menu)

    if choice == 'Add':
        st.subheader('Add a new user')
        name = st.text_input('Name')
        username = st.text_input('Username')
        password = st.text_input('Password')
        salt = bcrypt.gensalt()
        hashed_passwords = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_passwords = hashed_passwords.decode('utf-8')
        admin = st.selectbox('Admin', ['Select',True, False])
        
        submitted_user = st.button("Add User")
        if submitted_user:
            print(hashed_passwords)
            if name and username and password:
                new_user = users.put({'name': name, 'email': username, 'password': hashed_passwords,'admin': admin})
                print(new_user)
                if new_user:
                    st.success('User added successfully')
                else:
                    st.error('User could not be added')
            else:
                st.error('Please fill in all fields')

    elif choice == 'View':
        st.subheader('View all users')
        users_df = pd.DataFrame(user_details)
        st.table(users_df)
        download = st.button('Download')
        if download:
             df_download= pd.DataFrame(users_df)            
             csv = df_download.to_csv(index=False)
             b64 = base64.b64encode(csv.encode()).decode()  # some strings
             linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
             st.markdown(linko, unsafe_allow_html=True)

            
             df= pd.DataFrame(users_df)
             towrite = io.BytesIO()
             downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
             towrite.seek(0)  # reset pointer
             b64 = base64.b64encode(towrite.read()).decode()  # some strings
             linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
             st.markdown(linko, unsafe_allow_html=True)

    elif choice == 'Edit':
        st.subheader('Edit a user')
        name = st.text_input('Name')
        username = st.text_input('Username')
        password = st.text_input('Password')
        hashed_passwords = stauth.Hasher(password).generate()
        users.update(name, username, password)
        st.success('User edited successfully')
    elif choice == 'Delete':
        # st.subheader('Delete a user')
        # name = st.text_input('Name')
        # users.delete(name)
        st.success('User deleted successfully')
# Data to be written to Deta Base
    # with st.form("form"):
    #     name = st.text_input("Your name")
    #     age = st.number_input("Your age")
    #     submitted = st.form_submit_button("Store in database")




    # # # Create a new database "example-db"
    # # # If you need a new database, just use another name.
    # db = deta.Base("example-db")

    # # # If the user clicked the submit button,
    # # # write the data from the form to the database.
    # # # You can store any data you want here. Just modify that dictionary below (the entries between the {}).
    # if submitted:
    #     # db.put({"name": name, "age": age})
    #     age_test = db.fetch({"age": 8})
    #     print(age_test.items)

       
    # "---"
    # # "Here's everything stored in the database:"
    # # # This reads all items from the database and displays them to your app.
    # # # db_content is a list of dictionaries. You can do everything you want with it.
    # db_content = db.fetch().items

    # df = pd.DataFrame(db_content)
    # print(df)
    # df.to_excel("example.xlsx")
    # menu_data = df['name'].unique()
    # option = st.selectbox('Select a name', menu_data)
    # st.table(df[df['name'] == option])
    # # st.dataframe(df)
    # st.table(df)
    
    # selected_index = st.multiselect("Select a column", df.columns)

    # if selected_index:
    #     st.write(df[selected_index])