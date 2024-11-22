import requests
import streamlit as st
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access the API_KEY
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is missing! Please set it in the .env file.")
# Retrieve the API key from an environment variable

# API Configuration

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {API_KEY}"}
similarity_score = 0

if "my_text" not in st.session_state:
    st.session_state.my_text = ""
if "score_up" not in st.session_state:
    st.session_state.score_up = 0

def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""  # Reset input after submission

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Page Styling
st.set_page_config(page_title="Semantic Similarity Game", layout="centered")
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            color: white;
        }
        .stButton > button {
            background-color: #FF6F61;
            color: white;
            border-radius: 5px;
        }
        .stTextInput > div > input {
            border: 2px solid #FF6F61;
            border-radius: 5px;
            color: #333;
        }
        .card {
            background-color: #ffffff22;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .progress-bar {
            height: 8px;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.timer = 30
    st.session_state.source_sentence = "Happy"
    st.session_state.tries = []  # Store tries

# Levels
LEVELS = {
    1: {"sentence": "Happy"},
    2: {"sentence": "Bright sun"},
    3: {"sentence": "Dark night"},
    4: {"sentence": "Rainy day"},
    5: {"sentence": "Playful dog"},
    6: {"sentence": "Green grass"},
    7: {"sentence": "Blue ocean"},
    8: {"sentence": "Cold winter"},
    9: {"sentence": "Lazy cat"},
    10: {"sentence": "Warm fire"},
    11: {"sentence": "Giant tree"},
    12: {"sentence": "Golden beach"},
    13: {"sentence": "Mountain peak"},
    14: {"sentence": "Sweet smile"},
    15: {"sentence": "Fast car"},
    16: {"sentence": "Brave knight"},
    17: {"sentence": "Snowy mountain"},
    18: {"sentence": "Beautiful sky"},
    19: {"sentence": "Loud thunder"},
    20: {"sentence": "Flying bird"},
    21: {"sentence": "Silent night"},
    22: {"sentence": "Huge wave"},
    23: {"sentence": "Lonely road"},
    24: {"sentence": "Misty forest"},
    25: {"sentence": "Pink flowers"},
    26: {"sentence": "Warm hug"},
    27: {"sentence": "Shooting star"},
    28: {"sentence": "Bright moon"},
    29: {"sentence": "Blue sky"},
    30: {"sentence": "Rolling hills"},
    31: {"sentence": "Old castle"},
    32: {"sentence": "Little bird"},
    33: {"sentence": "Jungle path"},
    34: {"sentence": "Glowing firefly"},
    35: {"sentence": "Starry night"},
    36: {"sentence": "Calm lake"},
    37: {"sentence": "Ancient ruins"},
    38: {"sentence": "Distant thunder"},
    39: {"sentence": "Crystal lake"},
    40: {"sentence": "Shimmering stars"},
    41: {"sentence": "Frozen lake"},
    42: {"sentence": "Magic forest"},
    43: {"sentence": "Pirate ship"},
    44: {"sentence": "Golden treasure"},
    45: {"sentence": "Mysterious cave"},
    46: {"sentence": "Secret garden"},
    47: {"sentence": "Deep ocean"},
    48: {"sentence": "Wild adventure"},
    49: {"sentence": "Stormy clouds"},
    50: {"sentence": "Whispering winds"},
}


# Game Logic
st.title("Word Guessing Game")

# Hint explaining how the game works
st.info("""
    **How it works:**
    - You are given a sentence for each level.
    - Your task is to enter a guess based on the given sentence.
    - The system will calculate how similar your guess is to the sentence.
    - Your goal is to improve the similarity with each guess and progress through the levels!
    - Keep trying, and good luck!
""")
st.divider()
# User Input
st.markdown(f"### Level {st.session_state.level}")
columns = st.columns([2,1,2])
with columns[1]:
    st.metric("Score", st.session_state.score, st.session_state.score_up)
st.subheader("Submit Your Guess")
user_input = st.text_input("Please enter your guess below:", key="widget", on_change=submit)

user_input = st.session_state.my_text
if user_input:
    # API Call
    output = query({
        "inputs": {
            "source_sentence": LEVELS[st.session_state.level]["sentence"],
            "sentences": [user_input]
        },
    })
    similarity_score = output[0]
    lastTry = {
        "guess": user_input,
        "similarity": similarity_score
    }
    # Store the guess and similarity in tries
    st.session_state.tries.append(lastTry)


    # Check if the guess is correct
    sorted_tries = sorted(st.session_state.tries, key=lambda x: x['similarity'], reverse=True)

    if similarity_score >= 0.95:
        st.balloons()
        time.sleep(2)
        st.session_state.score_up = int(similarity_score * 100)
        st.session_state.score += st.session_state.score_up
        st.session_state.level += 1
        st.session_state.tries = []  # Reset tries for the next level
        st.session_state.my_text = ""  # Clear the previous guess for the next round

        st.rerun()



def displayTry(attempt):
    similarity = attempt['similarity'] * 100  # Similarity in percentage

    # Calculate the RGB color based on similarity
    if similarity <= 50:
        red = 255  # Start with red
        green = int(similarity * 5.1)  # Gradually increase green as similarity increases
    else:
        red = int((100 - similarity) * 5.1)  # Decrease red as similarity increases
        green = 255  # Use full green when similarity is high
    color = f"rgb({red}, {green}, 0)"  # Combine red and green for the color

    # Display the current try
    st.markdown(
        f"""
                <div style="background-color: rgba(255, 255, 255, 0.8); 
                            padding: 15px; 
                            margin-bottom: 10px; 
                            border-radius: 8px; 
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                            color: black;">
                    <strong>{attempt['guess'].title()}</strong>
                    <div style="width: 100%; background-color: #ddd; border-radius: 5px; overflow: hidden; height: 20px; margin-top: 10px;">
                        <div style="height: 100%; background-color: {color}; text-align: right; 
                                    padding-right: 5px; color: white; font-weight: bold; line-height: 20px; 
                                    width: {similarity}%; ">
                            {similarity:.2f}%
                        </div>
                    </div>
                </div>
                """,
        unsafe_allow_html=True,
    )

# Display Tries
if st.session_state.tries:
    st.divider()
    displayTry(lastTry)
    st.divider()
    for attempt in sorted_tries:
        displayTry(attempt)

# End Game
if st.session_state.level > len(LEVELS):
    st.balloons()
    st.markdown(f"🎉 **Congratulations! You've completed the game.**")
    st.markdown(f"🏆 **Your final score is: {st.session_state.score}**")
else:
    st.markdown(f"**Score:** {st.session_state.score}")


# Footer
st.markdown(
    """
    <hr style="border: 1px solid #ddd; margin: 20px 0;">
    <div style="
        text-align: center;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #555;
        line-height: 1.6;
    ">
        <p><strong>© 2024 Jan Bremec. All rights reserved.</strong></p>
        <p>
            This website is developed by <strong>Jan Bremec</strong> as part of a creative initiative to design an engaging and intellectually stimulating game. For inquiries, feedback, or potential collaborations, please feel free to contact us.
        </p>
        <p style="margin-top: 10px; font-size: 12px; color: #888;">
            We appreciate your visit and hope you enjoy the experience.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
