import os
import requests
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def analyze_date_range(start_date, end_date):
    prompt = f"""
    Analyze the financial trends for a company between {start_date} and {end_date}. 
    Consider the following aspects:
    1. Internal company factors (e.g., product launches, management changes)
    2. Industry trends
    3. Macroeconomic factors
    4. Political events that might have influenced the company's performance

    Provide a concise summary of potential explanations for the observed financial trends during this period.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": "You are a financial analyst AI that provides insights on company performance and market trends."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.RequestException as e:
        return f"Error: Unable to get analysis. {str(e)}"
