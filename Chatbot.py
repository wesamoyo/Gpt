import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = 'gpt2'  # You can replace this with the name of the GPT-2 model you want to use
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Rest of your Streamlit app code...

# Inside the section where you handle user prompts and generate responses
if prompt := st.chat_input():
    st.session_state["chats"][-1]["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ""

    # Check for greetings, weather, news, etc. as before...
    if any(word in prompt.lower() for word in ["hello", "hi", "what's up", "whats up", "how are you", "how's it going"]):
        response = "Hello! I'm here to assist you. How can I help you today?"
    elif "tell me a joke" in prompt.lower() or "joke" in prompt.lower():
        joke = "Your joke goes here"  # Replace with your joke generation logic
        response = f"Sure, here's a joke for you: {joke}."
    else:
        with st.spinner("Generating response..."):
            # Generate response using the GPT-2 model
            input_ids = tokenizer.encode(prompt, return_tensors="pt")
            output = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

            # Display only the first 800 characters of the generated content
            truncated_content = generated_text[:800]

            st.markdown(truncated_content, unsafe_allow_html=True)

    # If no specific response, check for a generic response
    if not response:
        response = "I'm here to assist you. If you have any specific questions or tasks, feel free to let me know!"

    st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
