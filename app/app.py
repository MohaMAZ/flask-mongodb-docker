from flask import Flask, render_template, request, jsonify
import pandas as pd
from detoxify import Detoxify
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clean')
def clean():
    df = pd.read_csv('webscraper/tweets.csv')
    df['child_harassment'] = None
    for index, row in enumerate(df['tweets'].values.tolist()):
        substrings = row.split('\n')
        for i in substrings:
            if '#harassment' in i.lower():
                df.iloc[index,0] = i.strip()
                if ('child' or 'enfant') in i.lower().split(' '):
                    df.iloc[index,1] = 1
                else:
                    df.iloc[index,1] = 0
    df.to_csv("tweets_cleaned.csv", index=False, encoding='utf-8')
    df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('display_cleaned_data.html', df_html=df_html)
@app.route('/analyse')
def analyse():
    df = pd.read_csv('tweets_cleaned.csv')
    df['toxicity'] = None
    for index, row in df.iterrows():
        results = Detoxify('multilingual').predict(row['tweets'])
        df.iloc[index,2] = results['toxicity']
    df.to_csv("tweets_analysed.csv", index=False, encoding='utf-8')
    df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('display_analysed_data.html', df_html=df_html)

@app.route('/insert')
def insert():
    client = MongoClient("mongodb://mongo:27017/")  # "mongo" is the hostname of the MongoDB container

    db = client["database"]
    collection = db["mycollection"]
    # Example data to insert
    df = pd.read_csv('tweets_analysed.csv')

    # Convert DataFrame to dictionary records
    records = df.to_dict(orient='records')
    result = collection.insert_many(records)
    return 'Data inserted successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)