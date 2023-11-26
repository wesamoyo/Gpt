import streamlit as st
from datetime import datetime
import pyjokes
import requests
import tensorflow as tf
from transformers import GPT2Tokenizer

# Load the GPT-2 tokenizer
model_name = "gpt2"  # or replace with the name of your specific GPT model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to download the model file from GitHub
def download_model():
    model_url = "https://github.com/wesamoyo/Gpt/raw/main/tf_model.h5"
    response = requests.get(model_url)
    
    with open("tf_model.h5", "wb") as model_file:
        model_file.write(response.content)

# Download the model file
download_model()

# Load the TensorFlow model
model = tf.keras.models.load_model("tf_model.h5")

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

def wish_me():
    hour = datetime.now().hour

    if 0 <= hour < 12:
        return "Good Morning boss☀️!"
    elif 12 <= hour < 18:
        return "Good Afternoon boss 🥵!"
    else:
        return "Good Evening boss☁️!"

# Display greeting
greeting = wish_me()
st.title(f"{greeting}")
st.caption("HOUNDGPT from HoundAi")

# Add "About," "Contact," and "HoundGPT Abilities" sections
# ... (rest of your code remains unchanged)

if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ""

    # Check for greetings, commands, or specific queries
    if any(word in prompt.lower() for word in ["hello", "hi", "what's up", "whats up", "how are you", "how's it going"]):
        response = "Hello! I'm here to assist you. How can I help you today?"
    elif "who created you" in prompt.lower() or "who made you" in prompt.lower():
        response = "I was created by Louis Wesamoyo. And he told me to tell you I am still under development."
    elif "current time" in prompt.lower() or "time now" in prompt.lower():
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}."
    elif "tell me a joke" in prompt.lower() or "joke" in prompt.lower():
        response = f"Sure, here's a joke for you: {pyjokes.get_joke()}."
    elif "what's your name" in prompt.lower() or "what is your name" in prompt.lower():
        response = "I'm called HoundAi, your research-based assistant. Try me for any research; I've got you!"
    elif "weather" in prompt.lower():
        # Add weather code logic here
        pass
    elif "news" in prompt.lower():
        # Add news code logic here
        pass
    else:
        # If no specific response, check for text generation using the GPT-2 model
        if not response:
            with st.spinner("Generating response..."):
                try:
                    # Tokenize user input
                    input_ids = tokenizer.encode(prompt, return_tensors="tf")

                    # Generate response using the TensorFlow model
                    output_ids = model.generate(
                        input_ids,
                        max_length=100,
                        num_beams=5,
                        no_repeat_ngram_size=2,
                        top_k=50,
                        top_p=0.95,
                        temperature=0.7
                    )

                    # Decode and display the generated response
                    generated_response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
                    response = f"Response: {generated_response}"
                except Exception as e:
                    response = f"Error generating response: {str(e)}"

        # If no specific response or generated response, provide a default message
        if not response:
            response = "I'm here to assist you. If you have any specific questions or tasks, feel free to let me know!"

    st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
