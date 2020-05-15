import csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()

more_stopword = []
 

with open('stopword.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
	more_stopword.append(row[0])

print more_stopword

dictionary = ArrayDictionary(more_stopword)
str = StopWordRemover(dictionary)

with open('marketing.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
	out = stemmer.stem(row[0])
	out = str.remove(out)
       	print(out)
	
	f = open("marketing.txt", "a")
	f.write(out+"\n")



