from django.shortcuts import render
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def index(request):
    response = None
    # print(openai.api_key)
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            response = ask_openai(question)
    return render(request, 'chatbot_simple/index.html', {'response': response})
