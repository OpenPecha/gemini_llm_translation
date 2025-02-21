import google.generativeai as genai
import time

# Configure Gemini API
genai.configure(api_key="API_TOKEN")

#Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Translation prompt
source_text = "Hello, how are you?"
target_language = "Tibetan"
prompt = f"Translate the following English text to {target_language}: {source_text}"

# Retry logic
for attempt in range(3):  # Retry up to 3 times
    try:
        response = model.generate_content(prompt)
        text = response.text
        print("Translated Text:", response.text)
        break  # Exit loop if successful
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(2)  # Wait before retrying


# Specify the output file name
output_file = "output.txt"

# Write the text to the file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(text)

print(f"Text successfully written to {output_file}")