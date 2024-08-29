# Requirement Analyzer

Welcome to the Requirement Analyzer GUI! This application allows users to upload Excel or CSV files containing requirements and analyze them using Natural Language Processing (NLP) and Machine Learning (ML) models, specifically a BERT-based model. The tool identifies ambiguous requirements for further processing, and uses NLP tools to find possible candidates resolve anaphora.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
  
## Features

**User-Friendly GUI**: Easy-to-use interface built with Tkinter for uploading files and running models.
**Ambiguity Detection**: Employs a custom BERT-based model to identifies and processes ambiguous requirements separately.
**Automated NLP Analysis**: Uses SpaCy to process text and find possible candidates resolve anaphora.
**CSV Output**: Saves processed results in CSV format for further analysis.

## Installation

## ~ Download link for the model checkpoint and label encoder here ~

### Step 1: Set Up the Virtual Environment

On the first run, you need to set up the virtual environment and install the required dependencies. Run the following command:

python setup_venv.py

### This script will:

1. Check if a virtual environment is already activated.
2. If not, it will create a new virtual environment in the current directory.

### Step 2: set the interpreter to the venv

### Step 3: Run the Application
After setting up the virtual environment, 
you can run the GUI application:
python GUI_v3.py

## Explanation
**First Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/requirement-analyzer-gui.git
   cd requirement-analyzer-gui
   ```

### setup_venv.py
This script checks if a virtual environment is activated. If not, it creates a new virtual environment in the current directory

### GUI_v3.py
This script provides a GUI for the Requirement Analyzer application. It includes the following functionalities:
  - installs all the required packages listed in requirements.txt.
 	- NLP Model Initialization: Loads the en_core_web_sm model from spaCy, downloading it if necessary.
 	- File Upload: Allows users to upload an Excel or CSV file containing requirements.
 	- Model Execution: Processes the uploaded file using a BERT model to identify intents and resolve ambiguous intents.
 	- NLP Processing: Uses spaCy to resolve anaphora in the requirements and saves the results to CSV files.
  
### BERT_Arch.py
 	- This script defines a custom BERT architecture for the requirement analysis model. It includes:

 	- A dropout layer for regularization.
 	- ReLU activation functions.
 	- Dense layers for transforming the BERT embeddings.
 	- A softmax activation function for the output layer.

## Usage
1. Upload File: Click the "Upload File" button to upload an Excel or CSV file containing the requirements.
2. Run Model: Click the "Run Model" button to process the uploaded file and analyze the requirements.
### Features
 	- NLP Model Initialization: Automatically initializes and downloads the required NLP model if not already installed.
 	- File Upload: Supports uploading Excel and CSV files.
 	- Requirement Analysis: Processes the requirements and identifies intents using a pre-trained model.
 	- Ambiguous Intent Resolution: Resolves ambiguous intents using NLP techniques and saves the results to CSV files.


