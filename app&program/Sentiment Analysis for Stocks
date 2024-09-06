from transformers import pipeline
import requests

API_KEY = open("API_KEY.....").read() #take your API from HuggingFace

#change these parameters
keyword = "gold"
date = "2024-09-06"
ticker = "GD"

pipe = pipeline("text-classificator", model="ProsusAI/finbert")

# parsing way
url = (
    'https://newsapi.org/v2/everything?'
    #f'ticker={ticker}&'
    f'q={keyword}&'
    f'from={date}&'
    'softBy=popularity&'
    f'apiKey={API_KEY}'
)

response = requests.get(url)

articles = response.json()['articles'] # short articles for visual understanding of sentiment analysis
articles = [article for article in articles if  keyword.lower() in article['title'].lower() or keyword.lower() in article['description'].lower()]

total_score = 0
num_articles = 0

for i, article in enumerate(articles):
    print(f'Title: {article["title"]}')
    print(f'Link: {article["url"]}')
    print(f'Description: {article["description"]}')

    sentiment = pipe(article['content'])[0]  # make decision here with 3 marks(by confidence of them)

    print(f'Sentiment {sentiment["label"]}, Score: {sentiment["score"]}')
    print('-' * 40)

    if sentiment['label'] == 'positive':
        total_score += sentiment['score']
        num_articles += 1
    elif sentiment['label'] == 'negative':
        total_score -= sentiment['score']
        num_articles += 1

# given parameters may be easily recreated 
final_score = total_score/num_articles  
print(f'Overall Sentiment: {"Positive" if final_score >= 0.2 else "Negative" if final_score <= -0.2 else "Neutral"}{final_score}')


