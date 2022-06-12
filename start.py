import streamlit as st
import bcrypt
from deta import Deta
deta = Deta(st.secrets["deta_key"])
users = deta.Base("users")
name = 'tommy'
username = 'tommy'
password = 'asdf'
salt = bcrypt.gensalt()
hashed_passwords = bcrypt.hashpw(password.encode('utf-8'), salt)
hashed_passwords = hashed_passwords.decode('utf-8')
admin = True
            
users.put({'name': name, 'email': username, 'password': hashed_passwords,'admin': admin})