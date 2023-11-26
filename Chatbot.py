import streamlit as st
import time
from datetime import datetime
import pyjokes
import requests
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the GPT-2 tokenizer and model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set page configuration with title and icon
st.set_page_config(
    page_title="HoundAI",
    page_icon="e9f83341-9417-4910-887f-e865c6d3e876.jpeg",
    layout="centered",
    initial_sidebar_state="collapsed"
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

if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ""

    # Check for greetings, commands, or specific queries
    # ... (rest of your code remains unchanged)

    # If no specific response, check for text generation using the Transformers model
    if not response:
        with st.spinner("Generating response..."):
            try:
                # Tokenize user input
                input_ids = tokenizer.encode(prompt, return_tensors="pt")

                # Generate response using the Transformers model
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
