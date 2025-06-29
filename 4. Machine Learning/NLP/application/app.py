from flask import Flask, render_template,request
import joblib
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def main():
    classifier = joblib.load('classifier.pkl')
    tfidfVectorizer = joblib.load('tfidfVectorizer.pkl')
    lemmatizer = WordNetLemmatizer()

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        review = request.form['review']
        corpus = []
        review = review.lower()
        review = review.split()
        review = [lemmatizer.lemmatize(word) for word in review if word not in stopwords.words('english')]
        review = ' '.join(review)
        corpus.append(review)
        x_tfid = tfidfVectorizer.transform(corpus).toarray()
        answer = classifier.predict(x_tfid)
        answer = str(answer[0])

        if answer == '1':
            return 'That looks like a postive review'
        else:
            return 'You do not seem to have liked that restaurant'


if __name__ == '__main__':
    app.run()

