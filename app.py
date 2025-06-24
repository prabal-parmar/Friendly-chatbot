import streamlit as st
import uuid
import chatbot

st.set_page_config(
    page_title="Chatbot",
    initial_sidebar_state="expanded"
)

if "name" not in st.session_state:
    st.session_state.name = None
if "id" not in st.session_state:
    st.session_state.id = None
if "history" not in st.session_state:
    st.session_state.history = []
if "newuser" not in st.session_state:
    st.session_state.newuser = False
 

if st.sidebar.button("Signin/Signup"):
    st.session_state.newuser = not st.session_state.newuser


with st.sidebar.form("login-signup"):
    
    if not st.session_state.newuser:
        name = st.text_input("Enter your name")
        uid = st.text_input("Enter your ID")
    else:
        st.info("Remember your ID")
        name = st.text_input("Enter your name")
        uid = st.text_input(label="Your ID", value=uuid.uuid4())

    language = st.selectbox("Select a language", sorted(["English", "Hindi", "Spanish", "German", "Bhojpuri", "Tamil", "Telugu"]))
    submit = st.form_submit_button('Submit')

if submit:
    st.session_state.history = []


st.session_state.name = name
st.session_state.id = uid

with st.container():
    st.header("Friendly Chatter")
    for i, message in enumerate(st.session_state.history):
        with st.chat_message(message["role"]):
            st.write(message["content"])


prompt = st.chat_input("Say something", key="main")

if prompt and name and uid:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    output = chatbot.send_answer(st.session_state.id, prompt, language, st.session_state.name)

    st.session_state.history.append({"role": "assistant", "content": output})
    with st.chat_message("assistant"):
        st.write(output)

elif not name or not uid:
    st.warning("Enter your name and ID")




