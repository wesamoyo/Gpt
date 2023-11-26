import streamlit as st
import requests
from datetime import datetime
import pyjokes
import tensorflow as tf
from transformers import GPT2Tokenizer

# Load the GPT-2 tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Specify the URL for the TensorFlow model
model_url = "https://github.com/wesamoyo/Gpt/raw/main/tf_model.h5"
model_local_path = "tf_model.h5"

# Download the model locally
with st.spinner("Downloading model..."):
    response = requests.get(model_url)
    with open(model_local_path, 'wb') as model_file:
        model_file.write(response.content)

# Load the TensorFlow model
model = tf.keras.models.load_model(model_local_path)

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

    if "who created you" in prompt.lower() or "who made you" in prompt.lower():
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
        key = "5ba8205acbf84994d62dddf851dd652b"
        weather_url = "http://api.openweathermap.org/data/2.5/weather?"
        ind = prompt.split().index("in")
        location = prompt.split()[ind + 1:]
        location = "".join(location)
        url = weather_url + "appid=" + key + "&q=" + location
        js = requests.get(url).json()
        if js["cod"] != "404":
            weather = js["main"]
            temperature = weather["temp"]
            temperature = temperature - 273.15
            humidity = weather["humidity"]
            desc = js["weather"][0]["description"]
            weather_response = f"The temperature in Celsius is {temperature:.2f}. The humidity is {humidity}%, and the weather description is {desc}."
            # Display immediate result
            st.write(weather_response)
        else:
            st.write("City Not Found")
    elif "news" in prompt.lower():
        news_url = (
            "http://newsapi.org/v2/top-headlines?"
            "country=us&"
            "apiKey=9656f1e97d55448392508fb1366d4f55"
        )
        try:
            news_response = requests.get(news_url)
            news_data = news_response.json()
            articles = news_data.get("articles", [])

            if articles:
                response = "Here are the latest news headlines:\n"

                for i, article in enumerate(articles[:5], start=1):
                    title = article.get("title", "N/A")
                    description = article.get("description", "No description available.")
                    response += f"{i}. **{title}**\n   {description}\n"
            else:
                response = "No news articles found."
        except requests.exceptions.RequestException as e:
            response = "Error fetching news. Please check your connection."
        
        # Display immediate result
        st.write(response)
    else:
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

    st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
