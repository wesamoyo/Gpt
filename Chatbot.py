import streamlit as st
from datetime import datetime
import pyjokes
import requests
import tensorflow as tf
from transformers import GPT2Tokenizer

# Load the GPT-2 tokenizer
model_name = "gpt2"  # or replace with the name of your specific GPT model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Load the TensorFlow model
model_path = "https://github.com/wesamoyo/Gpt/blob/main/tf_model.h5"
model = tf.keras.models.load_model(model_path)

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

# ... (rest of your code remains unchanged)

# Add the following logic for text generation using the GPT-2 model
# ... (rest of your code remains unchanged)

if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ""

    # Check for greetings, commands, or specific queries
    # ... (rest of your code remains unchanged)

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
                st.write(f"Response: {generated_response}")
            except Exception as e:
                st.write(f"Error generating response: {str(e)}")

    # If no specific response or generated response, provide a default message
    if not response and not generated_response:
        response = "I'm here to assist you. If you have any specific questions or tasks, feel free to let me know!"

    st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
