import requests
from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# District and Race Page
@app.route('/DR')
def DR():
    return render_template('DR.html')

# Campaign Page
@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

# Campaign Page
@app.route('/mission')
def mission():
    return render_template('mission.html')


# Get Involved
@app.route('/get_involved')
def get_involved():
    return render_template('get_involved.html')


#Fundraising Data Collection
def get_fundraising_total():
    with sqlite3.connect('fundraising.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total, goal FROM fundraising WHERE id = 1")
        result = cursor.fetchone()
        print(result)  # Debugging line
        return result


@app.route('/donate')
def donate():
    total, goal = get_fundraising_total()
    return render_template('donate.html', total=total, goal=goal)

@app.route('/donation_data')
def donation_data():
    total, goal = get_fundraising_total()
    return jsonify(total=total, goal=goal)


@app.route('/process_donation', methods=['POST'])
def process_donation():
    try:
        # Convert the amount to a float to ensure it's a valid number
        amount = float(request.form['amount'])
    except ValueError:
        # If conversion fails, return an error message
        return jsonify(success=False, message="Invalid donation amount!")

    # Update the fundraising total in the database
    with sqlite3.connect('fundraising.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE fundraising SET total = total + ? WHERE id = 1", (amount,))
        conn.commit()

    return jsonify(success=True, message="Thank you for your donation!")



#News API Fetch
def fetch_guardian_articles(query):
    api_url = 'https://content.guardianapis.com/search'
    params = {
        'q': query,
        'api-key': '4c8e9553-8344-46c8-ba87-25cd5b9a01c9',
        'show-fields': 'thumbnail'  # Request the thumbnail field
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
        'api-key': 'dPxCEUUaz5HjZ1qGk2K7erpiog7JzRBw',
        'fl': 'headline,web_url,pub_date,section_name,multimedia,thumbnail,' 

    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get('response', {}).get('docs', [])
    else:
        print(f'Failed to retrieve NYT articles: {response.status_code}')
        return []

@app.route('/news')
def news():
    query = 'Christine Drazan Senator'
    guardian_articles = fetch_guardian_articles(query)
    nyt_articles = fetch_nyt_articles(query)
    # Combine the articles from both sources
    articles = guardian_articles + nyt_articles
    return render_template('news.html', articles=articles)


#Media Page
@app.route('/media')
def media():
    return render_template('media.html')


@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
