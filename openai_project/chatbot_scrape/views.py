import os
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def scrape_website(url):
    # https://www.nidirect.gov.uk/articles/coronavirus-covid-19-testing
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all <article> tags
    articles = soup.find_all('article')
    
    # Initialize a variable to store the HTML content
    html_content = ""
    
    # Concatenate the HTML content of each <article> tag
    for article in articles:
        html_content += str(article)
    
    return html_content

def ask_question(text, question):
    # Formulate the prompt
    prompt = f"Based on the following text, please answer the question:\n\nText:\n{text}\n\nQuestion: {question}\n\nAnswer:"

    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    # Extract the relevant part of the response
    answer = response['choices'][0]['message']['content']
    return answer

def scrape_and_ask(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        question = request.POST.get('question')

        if not url or not question:
            return JsonResponse({'error': 'URL and question are required.'}, status=400)

        scraped_text = scrape_website(url)
        answer = ask_question(scraped_text, question)
        
        return JsonResponse({'answer': answer})

    return render(request, 'chatbot_scrape/scrape_and_ask.html')
