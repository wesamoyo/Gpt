\import streamlit as st
import time
from datetime import datetime
import pyjokes
import requests
import tensorflow as tf

# Load pre-trained TensorFlow model
model_path = "Gpt/tf_model.h5"
model = tf.keras.models.load_model(model_path)

# Set page configuration with title and icon
st.set_page_config(
    page_title="HoundAI",
    page_icon="e9f83341-9417-4910-887f-e865c6d3e876.jpeg",
    layout="centered",
    initial_sidebar_state="collapsed"  # Optional: Start with the sidebar collapsed
)

# ... (rest of your code)

# Inside the section where you handle user prompts and generate responses
if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ""

    # Check for greetings, weather, news, etc. as before...
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
        st.write(response)
    elif "weather" in prompt.lower():
        # ... (weather code)
    elif "news" in prompt.lower():
        # ... (news code)
    else:
        with st.spinner("Generating response..."):
            # Generate response using the TensorFlow model
            input_text = [prompt]
            # Preprocess your input text if needed
            # ...

            # Make predictions using your model
            output_text = model.predict(input_text)
            # Postprocess your output text if needed
            # ...

            # Display only the first 800 characters of the generated content
            truncated_content = output_text[:800]

            st.markdown(truncated_content, unsafe_allow_html=True)

    # If no specific response, check for a generic response
    if not response:
        response = "I'm here to assist you. If you have any specific questions or tasks, feel free to let me know!"

    st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
