import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the tokenizer and model from Hugging Face's GPT-2 (or any other model you prefer)
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Predefined answers (optional, for example questions)
PREDEFINED_ANSWERS = {
    "hello": "Hi! How can I help you today?",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "what is AI": "AI (Artificial Intelligence) is the simulation of human intelligence in machines."
}

# Function to check if a query is valid (optional, here it checks for a minimum number of words)
def is_valid_query(query):
    return len(query.split()) > 3

# Function to get predefined answers if available (optional)
def get_predefined_answer(query):
    query = query.lower().strip()
    return PREDEFINED_ANSWERS.get(query, None)

# Function to generate a response using GPT-2
def generate_response(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    gen_tokens = model.generate(
        input_ids,
        max_length=100,
        num_return_sequences=1,
        no_repeat_ngram_size=3,  # Avoid repeating ngrams
        temperature=0.7,  # Control randomness (higher = more random)
        do_sample=True  # Ensure sampling instead of greedy decoding
    )
    return tokenizer.decode(gen_tokens[0], skip_special_tokens=True)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the user input and provide a response
@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query", "")
    
    if not is_valid_query(user_query):
        return jsonify({"response": "Please provide a more detailed query."})
    
    # Check if the query is in predefined answers (optional)
    predefined_answer = get_predefined_answer(user_query)
    if predefined_answer:
        return jsonify({"response": predefined_answer})

    # Generate a response using GPT-2 if no predefined answer is found
    prompt = f"Answer the following question concisely: {user_query}"
    generated_text = generate_response(prompt)
    
    return jsonify({"response": generated_text})

if __name__ == "__main__":
    app.run(debug=True)
