import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Prepare the input
prompt = "Once upon a time,"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# Generate text
gen_tokens = model.generate(
    input_ids,
    max_length=50,
    num_return_sequences=1,
    no_repeat_ngram_size=3, # Avoid repeating ngrams
    temperature=0.7,        # Control randomness (higher = more random)
)
generated_text = tokenizer.decode(gen_tokens[0], skip_special_tokens=True)

# Print the generated text
print(generated_text)