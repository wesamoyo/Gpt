import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer from raw GitHub URL
model_url = 'https://github.com/wesamoyo/Gpt/raw/main/tf_model.h5'
tokenizer = GPT2Tokenizer.from_pretrained(model_url)
model = GPT2LMHeadModel.from_pretrained(model_url)

# Set page configuration with title and icon
st.set_page_config(
    page_title="HoundAI",
    page_icon="e9f83341-9417-4910-887f-e865c6d3e876.jpeg",
    layout="centered",
    initial_sidebar_state="collapsed"  # Optional: Start with the sidebar collapsed
)

# Hide the Streamlit logo, main menu, and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {display: none;}
        .viewerBadge_container__1QSob {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Initialize "chats" in st.session_state if it doesn't exist
if "chats" not in st.session_state:
    st.session_state["chats"] = [{"messages": []}]

# Display messages from the selected chat page
chat = st.session_state["chats"][0]
for msg in chat["messages"]:
    if msg["role"] == "assistant":
        st.chat_message("Hound").write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

# Add "New Chat" button to the sidebar
new_chat_button = st.sidebar.button("New Chat")

# Clear previous chats if the button is clicked
if new_chat_button:
    st.session_state["chats"][-1]["messages"] = []
    # Set the button state to False to avoid immediate clearing on subsequent interactions
    st.session_state["new_chat_button"] = True

# Store the state of the new chat button
st.session_state["new_chat_button"] = new_chat_button

if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate response using the GPT-2 model
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=150, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
    generated_response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Display the generated response
    st.chat_message("Hound").write(generated_response)

st.session_state["new_chat_button"] = new_chat_button
