import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import spacy

from model_utils.useModel import get_prediction  # Assuming this function is in useModel.py

# Check if running inside a virtual environment
def check_venv():
    if sys.prefix == sys.base_prefix:
        print("It looks like you are not running this script inside a virtual environment.")
        print("It's recommended to create a virtual environment and activate it before running this script.")
        print("Please create a virtual environment by running:\npython -m venv .venv\nAnd then activate it with:\n.venv\\Scripts\\activate (Windows)\nsource .venv/bin/activate (Unix/MacOS)")
        sys.exit(1)

# Install required packages
def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies are installed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

# Initialize NLP model
def initialize_nlp_model():
    global nlp
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Model 'en_core_web_sm' is not installed. Attempting to download.")
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

# Process uploaded file and run BERT model
def run_model(filepath):
    try:
        status_var.set("Processing...")
        df = pd.read_excel(filepath)
        sentences = df['Requirements']  # Assuming requirements are in the 'Requirements' column
        results = {'Sentence': [], 'Intent': []}
        for sentence in sentences:
            intent = get_prediction(sentence)
            results['Sentence'].append(sentence)
            results['Intent'].append(intent)
        results_df = pd.DataFrame(results)
        ambiguous_df = results_df[results_df['Intent'] == 'ambiguous']
        
        # Save to CSV
        # Ensure the processed_data and output directories exist
        processed_data_dir = 'processed_data'
        output_dir = 'output'
        os.makedirs(processed_data_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        # Save the initial processed file in the processed_data directory
        results_df.to_csv(os.path.join(processed_data_dir, 'all_intents.csv'), index=False)
        ambiguous_df.to_csv(os.path.join(processed_data_dir, 'ambiguous_intents.csv'), index=False)
        status_var.set("Model run complete. Proceeding to NLP processing...")

        # Process ambiguous intents and save the resolved anaphora file in the output directory
        process_ambiguous_intents(
            os.path.join(processed_data_dir, 'ambiguous_intents.csv'),
            os.path.join(output_dir, 'resolved_anaphora.csv')
        )
    except Exception as e:
        status_var.set(f"Error during model run: {str(e)}")

# Find pronouns and resolve anaphora using NLP
def findPronouns(sent, pronouns):
    tokens = []
    for t in sent:
        if "PRP" in t.tag_ and t.text.lower() in pronouns and t not in tokens:
            tokens.append(t)
    return tokens

def applynlp(string, nlp):
    tr = np.nan
    try:
        tr = nlp(string)
    except:
        print(string)
    return tr

def getNPs(sent, p, include_nouns=False):
    nps = []
    npstr = []
    chunks = list(sent.noun_chunks)
    for i in range(len(chunks)):
        np = chunks[i]
        if np.end <= p.i:
            if len(np) == 1:
                if np[0].pos_ not in ["NOUN", "PROPN"]:
                    continue
            if np.text.lower() in npstr:
                for x in nps:
                    if x.text.lower() == np.text.lower():
                        nps.remove(x)
                npstr.remove(np.text.lower())
            nps.append(np)
            npstr.append(np.text.lower())
            if i < len(chunks) - 1:
                np1 = chunks[i + 1]
                if np1.start - np.end == 1:
                    if sent.doc[np.end].tag_ == "CC":
                        newnp = sent.doc[np.start:np1.end]
                        if newnp.text.lower() in npstr:
                            for x in nps:
                                if x.text.lower() == newnp.text.lower():
                                    nps.remove(x)
                            npstr.remove(newnp.text.lower())
                        nps.append(newnp)
                        npstr.append(newnp.text.lower())
    if include_nouns:
        for t in sent:
            if t.i < p.i and "subj" in t.dep_ and t.pos_ == "NOUN":
                if t.text.lower() in npstr:
                    for x in nps:
                        if x.text.lower() == t.text.lower():
                            nps.remove(x)
                    npstr.remove(t.text.lower())
                npstr.append(t.text.lower())
                nps.append(sent[t.i:t.i + 1])
    return nps

def create_csv(exampleData, pronouns, output_path):
    li = []
    i, j = 0, 0
    ids = []
    for context in exampleData.Requirement.unique():
        for pronoun in findPronouns(context, pronouns):
            Id = str(i) + "-" + pronoun.text + "-" + str(j)
            while Id in ids:
                j += 1
                Id = str(i) + "-" + pronoun.text + "-" + str(j)
            for candidateAntecedent in getNPs(context, pronoun):
                li.append([Id, context, pronoun, pronoun.i, candidateAntecedent])
                ids.append(Id)
        i += 1
    result_df = pd.DataFrame(li, columns=["Id", "Context", "Pronoun", "Position", "Candidate Antecedent"])
    result_df.to_csv(output_path, index=False)

def process_ambiguous_intents(input_path, output_path):
    try:
        exampleData = pd.read_csv(input_path)
        exampleData["Requirement"] = exampleData["Sentence"].apply(lambda x: applynlp(x, nlp))
        create_csv(exampleData, pronouns, output_path)
        messagebox.showinfo("Success", f"Processing complete. Results saved to {output_path}")
    except Exception as e:
        status_var.set(f"Error during NLP processing: {str(e)}")

# GUI Functions
def upload_file():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
    if filepath:
        status_var.set("File uploaded successfully. Click 'Run Model' to start processing.")

def run_pipeline():
    if not filepath:
        messagebox.showwarning("Input Error", "Please upload an Excel/CSV file first")
        return
    run_model(filepath)

if __name__ == "__main__":
    # Check virtual environment
    check_venv()

    # Install dependencies
    install_requirements()

    # Initialize NLP model
    initialize_nlp_model()

    # Define pronouns
    pronouns = ["I", "me", "my", "mine", "myself", "you", "you", "your", "yours", "yourself", 
                "he", "him", "his", "his", "himself", "she", "her", "her", "hers", "herself", 
                "it", "it", "its", "itself", "we", "us", "our", "ours", "ourselves", "you", 
                "you", "your", "yours", "yourselves", "they", "them", "their", "theirs", "themselves"]

    # Setup GUI
    root = tk.Tk()
    root.title("Requirement Analyzer")

    status_var = tk.StringVar()
    status_var.set("Upload an Excel/CSV file and run the model.")

    upload_button = tk.Button(root, text="Upload File", command=upload_file)
    upload_button.pack()

    run_button = tk.Button(root, text="Run Model", command=run_pipeline)
    run_button.pack()

    status_label = tk.Label(root, textvariable=status_var)
    status_label.pack()

    root.mainloop()
