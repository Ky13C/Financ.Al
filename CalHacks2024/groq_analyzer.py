import os
from groq import Groq

class GroqAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def analyze_news(self, company_name, financial_data, news_data):
        prompt = f"""
        Analyze the following financial data and news for {company_name}:

        Financial Data:
        {financial_data}

        Recent News:
        {news_data}

        Explain how the recent news might be affecting the company's financial performance and stock price movements.
        Provide a concise analysis in 2-3 sentences.
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=150,
        )

        return response.choices[0].message.content

# Usage example:
# analyzer = GroqAnalyzer()
# analysis = analyzer.analyze_news("AAPL", "Q4 Revenue: $100B, EPS: $1.5", "Apple announces new iPhone model")
