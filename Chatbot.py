import streamlit as st
import time
from datetime import datetime
import pyjokes
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

# Load pre-trained GPT-2 model and tokenizer from raw URL
model_url = "https://raw.githubusercontent.com/wesamoyo/Gpt/main/tf_model.h5"

# Load the TensorFlow model directly
model = TFGPT2LMHeadModel.from_pretrained(model_url)

# Load the GPT-2 tokenizer (use the default GPT-2 tokenizer)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set page configuration with title and icon
st.set_page_config(
    page_title="HoundAI",
    page_icon="e9f83341-9417-4910-887f-e865c6d3e876.jpeg",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ... (rest of your existing Streamlit app code)

# Inside the if statement where you process user input and generate responses:
if prompt := st.text_input("User Input"):
    response = ""

    # Check for greetings
    if any(word in prompt.lower() for word in ["hello", "hi", "what's up", "whats up", "how are you", "how's it going"]):
        response = "Hello! I'm here to assist you. How can I help you today?"
    elif "who created you" in prompt.lower() or "who made you" in prompt.lower():
        response = "I was created by Louis Wesamoyo. And he told me to tell you I am still under development."
    elif "current time" in prompt.lower() or "time now" in prompt.lower():
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}."
    elif "tell me a joke" in prompt.lower() or "joke" in prompt.lower():
        joke = pyjokes.get_joke()
        response = f"Sure, here's a joke for you: {joke}."
    elif "what's your name" in prompt.lower() or "what is your name" in prompt.lower():
        assname = "HoundAi"
        response = f"I'm called {assname}, your research-based assistant. Try me for any research, I've got you!"
        # Display immediate result
        st.text_area("Model Response", response)
    elif "weather" in prompt.lower():
        # Your weather code here (replace with GPT-2 compatible code)
        pass
    elif "news" in prompt.lower():
        # Your news code here (replace with GPT-2 compatible code)
        pass
    else:
        # Use GPT-2 model to generate a response
        input_ids = tokenizer.encode(prompt, return_tensors="tf")  # Use TensorFlow encoding
        output = model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Display the generated response
    st.text_area("Model Response", response)
