import streamlit as st
from deta import Deta
import streamlit_authenticator as stauth
import non_admin
import admin


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
db = deta.Base("example-db")
users = deta.Base("users")
data = db.fetch().items
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
   
    # admin only
    if admin_status == True:
        admin.admin(users)
                
           
    # non_admin_view             
    non_admin.non_admin_view()
