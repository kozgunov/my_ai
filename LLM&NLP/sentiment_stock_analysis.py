from transformers import pipeline
import requests
import time

#API_KEY = open("API_KEY.....").read() #take your API from HuggingFace
API_KEY = "API_KEY" # token from https://newsapi.org/account 

#change these parameters
keyword = "Tesla"
date = "2024-09-12"
ticker = "TSLA"

pipe = pipeline("text-classification", model="ProsusAI/finbert")

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
sum_of_score = 0

for i, article in enumerate(articles):
    print(f'Title: {article["title"]}')
    print(f'Link: {article["url"]}')
    print(f'Description: {article["description"]}')

    sentiment = pipe(article['content'])[0]  # make decision here with 3 marks(by confidence of them)

    print(f'Sentiment {sentiment["label"]}, Score: {sentiment["score"]}')
    print('-' * 100)
    sum_of_score += sentiment["score"]

    if sentiment['label'] == 'positive':
        total_score += sentiment['score']
        num_articles += 1
    elif sentiment['label'] == 'negative':
        total_score -= sentiment['score']
        num_articles += 1

# given parameters may be easily recreated
final_score = total_score/num_articles if num_articles != 0 else 0
print(f'Overall Sentiment: {"Positive" if final_score >= 0.1 else "Negative" if final_score <= -0.1 else "Neutral "}{final_score} and sentiment score is {sum_of_score} for {num_articles} articles')



