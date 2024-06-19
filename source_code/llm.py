from openai import OpenAI
from dotenv import load_dotenv
import os
import together

load_dotenv()
together.api_key = os.getenv('TOGETHER_API_KEY')
gpt_call_count = 0


client = OpenAI()

def gpt_model_call(prompt, model='gpt-4'):

    model_config = {
        'gpt-3.5': ("gpt-3.5-turbo-0125", 2700),
        'gpt-4': ("gpt-4-0125-preview", 2700),
        'Llama_2_70B_HF': ('meta-llama/Llama-2-70b-hf', 2000),
        'Mixtral_8x7B_Instruct': ("mistralai/Mixtral-8x7B-Instruct-v0.1", 4048),
        'WizardCoder-Python-34B-V1.0': ("WizardLM/WizardCoder-Python-34B-V1.0", 2000)
    }
    model_name, max_tokens = model_config.get(model)

    global gpt_call_count
    gpt_call_count += 1

    if model in ['gpt-4']:
        model_response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        model_output = model_response.choices[0].message.content

    elif model in ['gpt-3.5']:
        model_response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        model_output = model_response.choices[0].message.content
    else:
        model_response = together.Complete.create(
            prompt=prompt,
            model=model_name,
            max_tokens=max_tokens,
            temperature=0,
            stop=["\n\n"]
        )
        model_output = model_response['output']['choices'][0]['text'].strip()
    return model_output
