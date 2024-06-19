This folder contains the source code for reproducibility and demostration. 

You can run the simulation multiple times to observe how LLM agents perform different parameter settings, trying to achieve the objective.

Among many LLMs, using GPT-4 is recommended, as the reasoning capability of the LLM is essential for satisfactory results.

## Installation
To set up the project locally, follow these steps:

1. Download the code and open with IDE, **python 3.9** is recommended for the environment to avoid package incompatibility.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the **app_socketio.py** after you integrating an LLM to the model, this can be simply done by using an LLM API, for example, a GPT4 model from OpenAI:
   
   create an *.env* file at the project folder and add your OpenAI API key in it.
   ```
   in .env:
   OPENAI_API_KEY="your_key_here"
   ```
4. run **app_socketio.py**
