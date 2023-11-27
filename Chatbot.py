import streamlit as st
from transformers import GPT2Tokenizer, TFGPT2Model
import tensorflow as tf

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = TFGPT2Model.from_pretrained("gpt2")

# Streamlit app
st.title("GPT-2 Streamlit App")

# Get user input
user_input = st.text_input("Enter text:")

# Generate response using GPT-2
if user_input:
    # Tokenize and convert to tensor
    inputs = tokenizer(user_input, return_tensors="tf")
    
    # Generate output
    output = model.generate(**inputs)
    
    # Decode and display response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    st.write("GPT-2 Response:", response)


