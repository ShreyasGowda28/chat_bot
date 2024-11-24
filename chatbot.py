from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from googlesearch import search

app = Flask(__name__)

# Function to process voice input
def process_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Error fetching results; {e}"

# Function to tokenize and stem text
def tokenize_and_stem(text):
    tokens = word_tokenize(text)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

# Function to search Google and retrieve information
def search_google(query):
    try:
        result = next(search(query, num=1, stop=1, pause=2, tld="com"), None)
        return result
    except StopIteration:
        return None

# Function to check for greetings
def check_greeting(user_input):
    greetings = ['hello', 'hi', 'hey', 'greetings', 'what\'s up', 'howdy']
    for greeting in greetings:
        if greeting in user_input.lower():
            return "Hello! How can I assist you today?"
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')

    # If user input is empty, process voice input
    if not user_input:
        user_input = process_voice_input()
    
    # Check for greetings
    greeting_response = check_greeting(user_input)
    if greeting_response:
        return jsonify({"response": greeting_response})

    tokens = tokenize_and_stem(user_input)
    query = " ".join(tokens)

    # Check for exit command
    if 'exit' in query.lower():
        return jsonify({"response": "Goodbye!"})

    # Perform Google search based on user's query
    search_result = search_google(query)

    if search_result:
        response_message = f"Here's what I found: <a href='{search_result}' target='_blank'>{search_result}</a>"
        return jsonify({"response": response_message})
    else:
        return jsonify({"response": "No results found for your query."})

if __name__ == "__main__":
    app.run(debug=True)