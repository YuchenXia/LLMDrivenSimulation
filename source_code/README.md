This folder contains the source code for reproducibility.

## Installation
To set up the project locally, follow these steps:

1. Download the code and open with IDE

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
