#!/usr/bin/env python
# coding: utf-8

import google.generativeai as genai
import pandas as pd
import multiprocessing
import time
from tqdm import tqdm
from get_prompt import (
    generate_commentary_translation_prompt,
    generate_combined_commentary_prompt,
    generate_plain_translation_prompt,
    generate_sanskrit_translation_prompt,
    generate_standardized_translation_prompt,
    generate_word_by_word_translation_prompt
)

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Mapping content types to corresponding prompt functions
PROMPT_FUNCTIONS = {
    "4 commentary translation english": generate_commentary_translation_prompt,
    "combined commentary english": generate_combined_commentary_prompt,
    "plain english": generate_plain_translation_prompt,
    "sanskrit translation": generate_sanskrit_translation_prompt,
    "standardised translation": generate_standardized_translation_prompt,
    "word by word translation": generate_word_by_word_translation_prompt
}

# Default target language
DEFAULT_TARGET_LANGUAGE = "English"


def build_prompt(row: pd.Series, target_language: str = DEFAULT_TARGET_LANGUAGE) -> str:
    """
    Selects and calls the appropriate prompt generator function based on content type.

    Args:
        row (pd.Series): A row from the DataFrame containing content.
        target_language (str): The target language for translation (default: "English").

    Returns:
        str: The generated prompt.
    """
    content_type = row.get("content type", "").strip().lower()
    prompt_function = PROMPT_FUNCTIONS.get(content_type, generate_plain_translation_prompt)
    return prompt_function(row, target_language)


def run_gemini_task(task_prompt: str, model_name: str = "gemini-pro", max_retries: int = 5, wait_time: int = 5) -> str:
    """
    Sends an API request to Gemini with retry logic.

    Args:
        task_prompt (str): The input prompt defining the task.
        model_name (str): Gemini model to use (default: "gemini-pro").
        max_retries (int): Maximum retry attempts if API call fails.
        wait_time (int): Seconds to wait before retrying.

    Returns:
        str: The AI-generated response or an error message.
    """
    retries = 0
    while retries < max_retries:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(task_prompt)

            if response and response.text:
                return response.text  # Successful response
            
            print(f"Attempt {retries + 1}: No response received. Retrying...")

        except Exception as e:
            print(f"Attempt {retries + 1}: Error - {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1

    return "Error: Maximum retries reached. Unable to get a response from Gemini."


def process_dataframe(df: pd.DataFrame, target_language: str = "English", num_workers: int = 5) -> pd.DataFrame:
    """
    Processes the DataFrame by generating prompts and sending API requests in parallel.

    Args:
        df (pd.DataFrame): DataFrame containing source texts and commentaries.
        target_language (str): The target language for translation.
        num_workers (int): Number of parallel processes.

    Returns:
        pd.DataFrame: Updated DataFrame with translation results.
    """
    # Step 1: Generate prompts for each row
    df["Prompt"] = df.apply(lambda row: build_prompt(row, target_language), axis=1)

    # Step 2: Send API requests in parallel using multiprocessing
    with multiprocessing.Pool(num_workers) as pool:
        results = list(tqdm(pool.imap(run_gemini_task, df["Prompt"]), total=len(df), desc="Processing Rows"))

    # Step 3: Store results in DataFrame
    df["Translated Text"] = results
    return df


def main():
    """
    Main execution function to load data, process translation, and display results.
    """
    # Load CSV Data
    input_csv = "buddhist_text_translation.csv"
    df = pd.read_csv(input_csv)

    # Process batch translation
    translated_df = process_dataframe(df, target_language=DEFAULT_TARGET_LANGUAGE, num_workers=5)

    # Save results to CSV
    output_csv = "translated_buddhist_text.csv"
    translated_df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Translation completed! Results saved to {output_csv}")


if __name__ == "__main__":
    main()
