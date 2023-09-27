import requests
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')


def fetch_guardian_articles(query):
    api_url = 'https://content.guardianapis.com/search'
    params = {
        'q': query,
        'api-key': '4c8e9553-8344-46c8-ba87-25cd5b9a01c9'
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get('response', {}).get('results', [])
    else:
        print(f'Failed to retrieve Guardian articles: {response.status_code}')
        return []

def fetch_nyt_articles(query):
    api_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {
        'q': query,
        'api-key': 'dPxCEUUaz5HjZ1qGk2K7erpiog7JzRBw'
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get('response', {}).get('docs', [])
    else:
        print(f'Failed to retrieve NYT articles: {response.status_code}')
        return []

@app.route('/news')
def news():
    query = 'Barack Obama'
    guardian_articles = fetch_guardian_articles(query)
    nyt_articles = fetch_nyt_articles(query)
    # Combine the articles from both sources
    articles = guardian_articles + nyt_articles
    return render_template('news.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
