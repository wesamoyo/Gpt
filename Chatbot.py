import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time
from datetime import datetime
import pyjokes
import wikipedia
import requests

# Load pre-trained GPT-2 model and tokenizer from raw GitHub URL
model_url = 'https://raw.githubusercontent.com/wesamoyo/Gpt/main/tf_model.h5'
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

# Add "About" section in the sidebar
with st.sidebar.expander("About"):
    st.info(
        "HoundGPT was created by Louis Wesamoyo to assist with research. And it's still under development but mostly it's a research bot. It's not yet approved to answer an examination, so just use it for research purposes for now, as other features are to be added soon."
        "Feel free to ask questions or request information.😎"
    )

# Add "Contact" section in the sidebar
with st.sidebar.expander("Contact"):
    st.info(
        "For inquiries or assistance, please contact us at:"
        "\n\n"
        "📧 Email: [hound4753@gmail.com](mailto:hound4753@gmail.com)"
    )

# Add "AI Capabilities" section in the sidebar
with st.sidebar.expander("HoundGPT Abilities"):
    st.info(
        "HoundAI can assist you with various tasks. Try asking about:"
        "\n\n"
        "🕒 Current Time"
        "\n"
        "🤣 Jokes"
        "\n"
        "🌦️ Weather of any country in the world (real-time)"
        "\n"
        "📰 News Headlines (Real-time)"
        "\n"
        "📚 Research on any Topics"
        "\n\n"
        "Feel free to explore and discover more!"
    )

    # Subsections for AI capabilities
    st.subheader("Time Related")
    st.write("🕒 Current Time")

    st.subheader("Entertainment")
    st.write("🤣 Jokes")

    st.subheader("Weather")
    st.write("🌦️ Weather of any country in the world (real-time)")

    st.subheader("News")
    st.write("📰 News Headlines (Real-time)")

    st.subheader("Research")
    st.write("📚 Research on any Topics")

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
            weatherResponse = f"The temperature in Celsius is {temperature:.2f}. The humidity is {humidity}%, and the weather description is {desc}."
            # Display immediate result
            st.write(weatherResponse)
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
        with st.spinner("Fetching information..."):
            try:
                time.sleep(2)
                # Use the GPT-2 model for generating responses
                inputs = tokenizer(prompt, return_tensors="pt")
                outputs = model.generate(**inputs, max_length=250, num_beams=5, no_repeat_ngram_size=2)
                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                st.markdown(generated_text, unsafe_allow_html=True)
            except Exception as e:
                content = f"Error: {str(e)}"
                st.markdown(content)

        # If no specific response, check for a generic response
        if not response:
            response = "I'm here to assist you. If you have any specific questions or tasks, feel free to let me know!"

        st.chat_message("Hound").write(response)

st.session_state["new_chat_button"] = new_chat_button
