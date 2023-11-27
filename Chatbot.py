import streamlit as st
from transformers import pipeline

# Set up the Inference API pipeline with your API key
api_key = "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"  # Replace with your actual API key
generator = pipeline('text-generation', model=f'gpt2/{api_key}')

# Streamlit app
st.title("GPT-2 Streamlit App")

# Get user input
user_input = st.text_input("Enter text:")

# Generate response using GPT-2
if user_input:
    response = generator(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
    st.write("GPT-2 Response:", response)



