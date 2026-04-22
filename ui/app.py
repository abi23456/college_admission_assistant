import streamlit as st
import requests
import json
import uuid

# Configuration
# Change this to your n8n webhook URL once you've started the n8n workflow
N8N_WEBHOOK_URL = "https://abi1012.app.n8n.cloud/webhook/admission-chat"

st.set_page_config(page_title="College Admission Assistant", page_icon="🎓", layout="centered")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; }
    .css-1v0mbdj.etr89bj1 { text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 College Admission Assistant")
st.markdown("Ask me about eligibility, required documents, deadlines, or request a step-by-step checklist! (Powered by RAG & n8n)")

# Initialize chat history and session ID
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I am your AI College Admission Assistant. How can I help you today?"
    })

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("E.g., What are the deadlines for Stanford?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to n8n backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        payload = {
            "sessionId": st.session_state.session_id,
            "chatInput": prompt
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                # Assuming n8n returns JSON with 'output' key. If n8n returns raw text, use response.text
                try:
                    data = response.json()
                    # n8n sometimes wraps responses in a list
                    if isinstance(data, list) and len(data) > 0:
                        data = data[0]
                    
                    if isinstance(data, dict):
                        assistant_reply = data.get("output", str(data))
                    else:
                        assistant_reply = str(data)
                except ValueError:
                    assistant_reply = response.text
                message_placeholder.markdown(assistant_reply)
            else:
                assistant_reply = f"**Error**: Received status code {response.status_code} from backend. Make sure your n8n workflow is active."
                message_placeholder.markdown(assistant_reply)
        except Exception as e:
            assistant_reply = f"**Connection Error**: Could not connect to n8n backend ({str(e)}). Make sure the webhook URL is correct and n8n is running."
            message_placeholder.markdown(assistant_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
