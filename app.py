from flask import Flask, render_template, request
import os
import pickle
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")
import math
import re
from collections import Counter
import pandas as pd
import pickle

app = Flask(__name__)

# # Load your machine learning model
# with open('model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# with open('mix_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)



# preprocess
def clean_script(script):
    # Remove comments from the script
    script = re.sub(r'#.*$', ' ', script, flags=re.MULTILINE)

    # Remove special characters and reduce consecutive spaces
    cleaned_script = re.sub(r'\s+', ' ', script)

    # Remove tabs and newlines
    cleaned_script = cleaned_script.replace('\t', ' ').replace('\n', ' ')

    # Remove punctuation
    cleaned_script = re.sub(r'[^\w\s]', ' ', cleaned_script).lower()

    return cleaned_script


# Function definitions (copied from your training notebook)
def text_length(script):
    return len(script)


def entropy(script):
    character_counts = Counter(script)
    total_characters = len(script)
    probabilities = [count / total_characters for count in character_counts.values()]
    entropy_value = -sum(probability * math.log2(probability) for probability in probabilities)
    return entropy_value


def punctuation_count(script):
    return len(re.findall(r'[^\w\s]', script))


def function_count(script):
    function_keywords = ['function', 'procedure']
    return sum(script.count(keyword) for keyword in function_keywords)


def numeric_literal_count(script):
    return len(re.findall(r'\b\d+\b', script))


def string_literal_count(script):
    return len(re.findall(r'"([^"]*)"', script))


def has_error_handling(script):
    error_handling_keywords = ['try', 'except', 'catch']
    return any(keyword in script for keyword in error_handling_keywords)


def has_urls_or_ips(script):
    return bool(re.search(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|\d+\.\d+\.\d+\.\d+', script))


def has_obfuscation_indicators(script):
    obfuscation_patterns = [
        r'\b(?:\w+\s*\+\s*\w+)',
        r'\b(?:[a-zA-Z]\s*=\s*[^;]*\bchr\s*\(\s*\w+\s*\+\s*\d+\s*\)\s*;\s*)+',
        r'0x[\da-fA-F]+',
        r'(?:\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})',
        r'\b(?:Add-Type|dllimport|virtualalloc|createthread|memset)\b',
        r'\b(?:eval|exec|decode|encode|obfuscate)\b'
    ]
    return any(re.search(pattern, script) for pattern in obfuscation_patterns)


def has_suspicious_words(script):
    disclosure_keywords = ['downloadfile', 'password', 'secret', 'key', 'token', 'downloadstring',
                           'dllimport', 'programdata', 'new object', 'appdata']
    return any(keyword in script for keyword in disclosure_keywords)


def longest_string_length(script):
    string_literals = re.findall(r'"([^"]*)"', script)
    if not string_literals:
        return 0
    longest_length = max(len(string_literal) for string_literal in string_literals)
    return longest_length


def preprocess(text_input):
    # preprocess
    clean = clean_script(text_input)
    # Load the TF-IDF vectorizer
    # with open('vectorizer.pkl', 'rb') as file:
    #     vectorizer = pickle.load(file)
    with open('mix_vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)
    # Load the SelectKBest instance
    # with open('selector.pkl', 'rb') as file:
    #     selector = pickle.load(file)
    with open('mix_selector.pkl', 'rb') as file:
        selector = pickle.load(file)
    # Load the selected feature names DataFrame
    # X_selected_df = pd.read_pickle('selected_features.pkl')
    X_selected_df = pd.read_pickle('mix_selected_features.pkl')
    # Apply the TF-IDF vectorizer to the new data
    X_tfidf = vectorizer.transform([clean])
    # Apply the loaded SelectKBest instance to the TF-IDF transformed data
    X_new_selected = selector.transform(X_tfidf)
    # Convert the selected features to a DataFrame using the previously selected feature names
    X_new_selected_df = pd.DataFrame(X_new_selected.toarray(), columns=X_selected_df.columns)

    length = text_length(clean)
    ent = entropy(text_input)
    punc_count = punctuation_count(text_input)
    func_count = function_count(clean)
    num_lit_count = numeric_literal_count(clean)
    str_lit_count = string_literal_count(text_input)
    err_handling = has_error_handling(clean)
    urls_ips = has_urls_or_ips(text_input)
    obf_indicators = has_obfuscation_indicators(clean)
    suspicious_words = has_suspicious_words(clean)
    longest_str_length = longest_string_length(text_input)

    # Create a DataFrame with the extracted features
    new_features = pd.DataFrame({
        'text_length': [length],
        'function_count': [func_count],
        'numeric_literal_count': [num_lit_count],
        'has_error_handling': [int(err_handling)],
        'has_obfuscation_indicators': [int(obf_indicators)],
        'has_suspicious_words': [int(suspicious_words)],

        'Entropy': [ent],
        'punctuation_count': [punc_count],
        'longest_string_length': [longest_str_length],
        'string_literal_count': [str_lit_count],
        'has_urls_or_ips': [int(urls_ips)]
    })

    # Concatenate the new features DataFrame with the existing DataFrame containing selected features
    X_new_selected_df_with_features = pd.concat([X_new_selected_df, new_features], axis=1)

    # Load the trained model
    # with open('model.pkl', 'rb') as file:
    #     model = pickle.load(file)
    with open('mix_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Use the model to make predictions
    predicted_label = model.predict(X_new_selected_df_with_features)
    return predicted_label


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    text_input = request.form.get('textInput', '')
    classification_result = ""

    try:
        if len(text_input) > 0:
            predicted_label = preprocess(text_input)
            if predicted_label[0] == 0:
                classification_result = "Malicious"
            else:
                classification_result = "Benign"

        # Check if a file is uploaded
        elif 'fileInput' in request.files:
            file = request.files['fileInput']
            file_content = file.read().decode("utf-8")
            if len(file_content) == 0:
                return "Please enter a text or upload a file"

            # If the uploaded file contains PowerShell script, classify it using the model
            predicted_label = preprocess(file_content)
            if predicted_label[0] == 0:
                classification_result = "Malicious"
            else:
                classification_result = "Benign"

        else:
            classification_result = "Please enter a text or upload a file"

    except Exception as e:
        # Log the exception along with request details
        app.logger.error(f"An error occurred during classification: {str(e)}")
        app.logger.error(f"Request data: {request.form} {request.files}")
        # Return a generic error message
        return "An error occurred during classification. Please try again later.", 500

    return classification_result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
