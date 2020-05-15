"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified 
texts. So, you have better call this data your training set.
"""
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from flask import Flask
from flask import request
from flask import jsonify




app = Flask(__name__)

@app.route('/')
def api_root():
     return "Hai"

@app.route('/deteksi', methods = ['POST'])
def api_echo():
    if request.method == 'POST':

	# create stemmer
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	factory = StopWordRemoverFactory()

        more_stopword = []
	# add stopword
	with open('dataset/stopword.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=',')
	    for row in readCSV:
		more_stopword.append(row[0])

	dictionary = ArrayDictionary(more_stopword)
	str = StopWordRemover(dictionary)


	newsTrainer = Trainer(tokenizer)


	kesehatan = []
	konsultasi = []
	marketing = []

	with open("dataset/kesehatan.txt", "r") as ins:
	    for line in ins:
		kesehatan.append({'text': line.rstrip(), 'category': 'kesehatan'})


	with open("dataset/konsultasi.txt", "r") as ins:
	    for line in ins:
		konsultasi.append({'text': line.rstrip(), 'category': 'konsultasi'})


	with open("dataset/marketing.txt", "r") as ins:
	    for line in ins:
		marketing.append({'text': line.rstrip(), 'category': 'marketing'})



	# You need to train the system passing each text one by one to the trainer module.
	newsSet = kesehatan + konsultasi + marketing

	for news in newsSet:
	    newsTrainer.train(news['text'], news['category'])

	# When you have sufficient trained data, you are almost done and can start to use
	# a classifier.
	newsClassifier = Classifier(newsTrainer.data, tokenizer)

	query = request.form['query'].encode("utf8")
	#query = "Apa saja level bonus yang didapat bagi seorang agen?"

	# stemming and remove stop word on Query
	out = stemmer.stem(query)
	out = str.remove(out)
	classification = newsClassifier.classify(out)

	# the classification variable holds the detected categories sorted
	#return classification[0][0]
	return jsonify(classification)



if __name__ == '__main__':
    app.run()







