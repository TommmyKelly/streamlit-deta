import streamlit as st
from deta import Deta
import streamlit_authenticator as stauth
import pandas as pd
import bcrypt
import base64
import io
from streamlit.components.v1 import html
import non_admin


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
db = deta.Base("example-db")
users = deta.Base("users")
data = db.fetch().items
user_details = users.fetch().items
selection = [user_details['email'] for user_details in user_details]
selection.insert(0, 'Select')

names = [user["name"] for user in user_details]
usernames = [user["email"] for user in user_details]
password = [user['password'] for user in user_details]
update_user = None
def check_user(username) -> bool:
    """
    Check if user exists in the database
    """
    check = users.fetch({'email': username})
    if check.items:
        return True
    else:
        return False

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
   
    # admin only
    if admin_status == True:
        st.header('Admin Dashboard')
        st.write('This is an admin dashboard')

        menu = ['Select','None','Add', 'View', 'Edit', 'Delete']

        choice = st.sidebar.selectbox('Admin Select an option', menu)

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
                if name and username and password and admin != 'Select':
                    if not check_user(username):
                        new_user = users.put({'name': name, 'email': username, 'password': hashed_passwords,'admin': admin})
                        print(new_user)
                        if new_user:
                            st.success('User added successfully')
                        else:
                            st.error('User could not be added')
                    else:
                        st.error('User already exists')
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
            
            edit_user = st.selectbox('Select a user to edit',selection)
            if edit_user != 'Select':
                user_detail = users.fetch({'email': edit_user}).items[0]
                name = st.text_input('Name', user_detail['name'])
                username = st.text_input('Username', user_detail['email'])
                password = st.text_input('Password', user_detail['password'])
                if user_detail['admin'] == True:
                    index = 1
                else:
                    index = 2
                admin = st.selectbox('Admin', ['Select',True, False], index)
                
            update_user = st.button('Update User')
            if update_user:
                if name and username and password and admin != 'Select':
                    dict = {'name': name, 'email': username, 'password': password, 'admin': admin}
                    users.update(dict, user_detail['key'])
                    st.success('User edited successfully')
                else:
                    st.error('Please fill in all fields')

        elif choice == 'Delete':
            
            
            st.subheader('Delete a user')
            
            username = st.selectbox('Select a user to delete', selection)
            delete_user = st.button('Delete')
            

          
            if delete_user:
                
                key = users.fetch({'email': username}).items[0]['key']
                users.delete(key)
                st.success(f'User {username} deleted successfully')
                
           
                 
    non_admin.non_admin_view()
#     # users only
#     user_menu = ['Select','None', 'View', 'Edit', 'Delete']
#     user_choice = st.sidebar.selectbox('Select an option', user_menu)
#     if user_choice == 'View':
#         st.subheader('View your details')
#         data_df = pd.DataFrame(data)
#         st.table(data_df)
    
    
# # Data to be written to Deta Base
#     with st.form("form"):
#         name = st.text_input("Your name")
#         age = st.number_input("Your age")
#         submitted = st.form_submit_button("Store in database")




#     # # Create a new database "example-db"
#     # # If you need a new database, just use another name.
#     db = deta.Base("example-db")

#     # # If the user clicked the submit button,
#     # # write the data from the form to the database.
#     # # You can store any data you want here. Just modify that dictionary below (the entries between the {}).
#     if submitted:
#         # db.put({"name": name, "age": age})
#         age_test = db.fetch({"age": 8})
#         print(age_test.items)

       
#     "---"
#     # "Here's everything stored in the database:"
#     # # This reads all items from the database and displays them to your app.
#     # # db_content is a list of dictionaries. You can do everything you want with it.
#     db_content = db.fetch().items

#     df = pd.DataFrame(db_content)
#     print(df)
#     df.to_excel("example.xlsx")
#     menu_data = df['name'].unique()
#     option = st.selectbox('Select a name', menu_data)
#     st.table(df[df['name'] == option])
#     # st.dataframe(df)
#     st.table(df)
    
#     selected_index = st.multiselect("Select a column", df.columns)

#     if selected_index:
#         st.write(df[selected_index])