# import logging
# import streamlit as st
# import random
# import hashlib
# import os

# from src.utils.langchain import generate_response
# from src.utils.ocr import convert_pdf_to_images

# # from src.utils.langchain import generate_response
# # from src.utils.ocr import convert_pdf_to_images


# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()


# # Function to check if the username already exists
# def username_exists(username):
#     return username in st.session_state.users


# def initialize_st():
#     if "users" not in st.session_state:
#         st.session_state.users = {}
#     if "current_user" not in st.session_state:
#         st.session_state.current_user = None
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "chat_enabled" not in st.session_state:
#         st.session_state.chat_enabled = False
#     if "file_uploaded" not in st.session_state:
#         st.session_state.file_uploaded = False

#     st.set_page_config(page_title="RAG App")

#     st.markdown(
#         """
#         <style>
#         .stTextInput>div>div>input {
#             background-color: #f0f2f6;
#         }
#         .stChatMessage {
#             background-color: #f0f2f6;
#             border-radius: 10px;
#             padding: 10px;
#             margin-bottom: 10px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#     if st.session_state.current_user is None:
#         login_signup()
#     else:
#         chat_interface()


# def login_signup():
#     if st.session_state.current_user is None:
#         st.title("Welcome to RAG")
#         choice = st.radio("Login/Signup", ["Login", "Sign Up"])

#         if choice == "Sign Up":
#             st.subheader("Create New Account")
#             new_user = st.text_input("Username")
#             new_password = st.text_input("Password", type="password")
#             if st.button("Signup"):
#                 if username_exists(new_user):
#                     st.error("Username already exists. Please choose a different one.")
#                 else:
#                     st.session_state.users[new_user] = hash_password(new_password)
#                     st.success("You have successfully created a valid Account")
#                     st.info("Go to Login Menu to login")

#         else:
#             st.subheader("Login Section")
#             username = st.text_input("User Name")
#             password = st.text_input("Password", type="password")
#             if st.button("Login"):
#                 if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
#                     st.session_state.current_user = username
#                     st.success("Logged In as {}".format(username))
#                     st.rerun()
#                 else:
#                     st.warning("Incorrect Username/Password")


# # Chat Interface
# def chat_interface():
#     st.title(f"Welcome, {st.session_state.current_user}!")

#     st.sidebar.title("RAG")
#     uploaded_file = st.sidebar.file_uploader("Choose a file", type="pdf")

#     if uploaded_file is not None and not st.session_state.file_uploaded:
#         # Store bytes data in session state to persist it after reruns
#         st.session_state.bytes_data = uploaded_file.getvalue()
#         st.session_state.file_uploaded = True
#         st.session_state.chat_enabled = False
#         st.rerun()

#     # Proceed if the file has been uploaded
#     if st.session_state.file_uploaded and not st.session_state.chat_enabled:
#         st.sidebar.button("Start chat", disabled=True)
#         with st.spinner("Processing file..."):
#             # Access bytes_data from session state
#             context = convert_pdf_to_images(st.session_state.bytes_data)
#             st.session_state.context = context
#         st.session_state.chat_enabled = True
#         st.rerun()

#     # Chat functionality after enabling chat
#     if st.session_state.chat_enabled:
#         if st.sidebar.button("Start chat"):
#             st.session_state.chat_started = True

#         if st.session_state.get("chat_started", False):
#             for message in st.session_state.messages:
#                 with st.chat_message(message["role"]):
#                     st.markdown(message["content"])

#             if prompt := st.chat_input("What is your message?"):
#                 st.chat_message("user").markdown(prompt)
#                 st.session_state.messages.append({"role": "user", "content": prompt})

#                 context_path = st.session_state.context
#                 response = generate_response(prompt, context_path)
#                 with st.chat_message("assistant"):
#                     st.markdown(response)
#                 st.session_state.messages.append({"role": "assistant", "content": response})

#     # Logout functionality
#     if st.button("Logout"):
#         st.session_state.current_user = None
#         st.session_state.messages = []
#         st.session_state.chat_enabled = False
#         st.session_state.file_uploaded = False
#         if "chat_started" in st.session_state:
#             del st.session_state.chat_started
#         st.rerun()


# def run_st():
#     try:
#         initialize_st()
#         if st.session_state.current_user is None:
#             login_signup()
#         else:
#             chat_interface()
#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}")
import logging
import streamlit as st
import hashlib
from src.utils.langchain import generate_response
from src.utils.ocr import convert_pdf_to_images

# Set page config at the very beginning
st.set_page_config(page_title="RAG App")


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# Function to check if the username already exists
def username_exists(username):
    return username in st.session_state.users


def initialize_session_state():
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_enabled" not in st.session_state:
        st.session_state.chat_enabled = False
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = False


def login_signup():
    st.title("Welcome to RAG")
    choice = st.radio("Login/Signup", ["Login", "Sign Up"])

    if choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if username_exists(new_user):
                st.error("Username already exists. Please choose a different one.")
            else:
                st.session_state.users[new_user] = hash_password(new_password)
                st.success("You have successfully created a valid Account")

    else:
        st.subheader("Login Section")
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
                st.session_state.current_user = username
                st.success("Logged In as {}".format(username))
                st.rerun()
            else:
                st.warning("Incorrect Username/Password")


def chat_interface():
    st.title(f"Welcome, {st.session_state.current_user}!")

    st.sidebar.title("RAG")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="pdf")

    if uploaded_file is not None and not st.session_state.file_uploaded:
        st.session_state.bytes_data = uploaded_file.getvalue()
        st.session_state.file_uploaded = True
        st.session_state.chat_enabled = False
        st.rerun()

    if st.session_state.file_uploaded and not st.session_state.chat_enabled:
        if st.sidebar.button("Process file"):
            with st.spinner("Processing file..."):
                context = convert_pdf_to_images(st.session_state.bytes_data)
                st.session_state.context = context
            st.session_state.chat_enabled = True
            st.rerun()

    if st.session_state.chat_enabled:
        if not st.session_state.get("chat_started", False):
            if st.sidebar.button("Start chat"):
                st.session_state.chat_started = True
                st.rerun()

        if st.session_state.get("chat_started", False):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            prompt = st.chat_input("What is your message?")
            if prompt:
                st.chat_message("user").markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                context_path = st.session_state.context
                response = generate_response(prompt, context_path)
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def run_st():
    initialize_session_state()

    st.markdown(
        """
        <style>
        .stTextInput>div>div>input {
            background-color: #f0f2f6;
        }
        .stChatMessage {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.current_user is None:
        login_signup()
    else:
        chat_interface()
