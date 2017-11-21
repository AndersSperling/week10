import re
import glob
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher
import thread

#Create sets/lists for the words, the topics and the wordbag
words = set()
topics = []
wordbag = []

#Get all unique words
def addToWordList(filename):
    wordList = set()
    with open(filename) as file:
        data = json.load(file)
        for entry in data:
            #Only entries with both the 'topics' and 'body' keys present
            #Is used, the rest are discarded.
            if 'topics' in entry and 'body' in entry:
                body = entry['body'].lower().split()
                wordList = wordList.union(set(body))
                #In order to comply with the classifier and feature hasher only one topic is saved,
                #Given the future task regarding earn, this is taken as the most important.
                if('earn' in entry['topics']):
                    topics.append('earn')
                else:
                    topics.append(entry['topics'][0])
        return wordList


#Build wordbag from the word list.
def addToWordbag(filename):
    internalWordbag = list()
    with open(filename) as file:
        data = json.load(file)
        for entry in data:
            #Only entries with both the 'topics' and 'body' keys present
            #Is used, the rest are discarded.
            if 'topics' in entry and 'body' in entry:
                body = entry['body'].lower().split()
                wordbagEntry = []
                for i in range(0, len(words)):
                    wordbagEntry.append(body.count(words[i]))
                internalWordbag.append(wordbagEntry)
        return internalWordbag

#A matrix to list of dicts helper-function used by the feature hashing algorithm.
def matrixToDict(matrix):
    returnDict = []
    for line in matrix:
        intermidiateDict = {}
        for i in range(0,len(line)):
            intermidiateDict[words[i]] = line[i]
        returnDict.append(intermidiateDict)
    return returnDict

def partWordBagFunc(file):
    partWordBag = addToWordbag(file)
    for line in partWordBag:
        wordbag.append(line)

#Getting the filenames of all the files in the full-folder
files = glob.glob("reuters-21578-json/data/full/*.json")
#From each file, the wordlist generator is used to get the unique words.
#The union of the existing wordlist and the newly generated is then saved.
for i in range(0, len(files)):
    words = words.union(addToWordList(files[i]))

#For conviniece the wordlist set, is converted to a list.
words = list(words)

#Once again running through the files, however this time the word list is used
#To create a bag-of-words representation.
for i in range(0, len(files)):
    print i
    partWordBagFunc(files[i])
    
#The random forest classifier is created with 50 estimators and bootstrapping set to true
forest = RandomForestClassifier(n_estimators=50, bootstrap=True)
#80 percent of the data is taken from both the wordbag, and the class labels
x = wordbag[0:int(len(wordbag)*0.8)]
y = topics[0:int(len(topics)*0.8)]

#The randopm forest classifier is fit to the data
forest.fit(x,y)

#Now the fitted classifier is made to predict the labels of the final 20% of the data
#And the real labels are also found.
predictedAnswers = forest.predict(wordbag[int(len(wordbag)*0.8):])
realAnswers = topics[int(len(wordbag)*0.8):]

#Once the prediction is done, the predicted labels are compared to the real ones.
hit = 0
miss = 0
for i in range(0, len(predictedAnswers)):
    if predictedAnswers[i] == realAnswers[i]:
        hit +=1
    else:
        miss +=1
#The hit and miss rate is printed
print("Hits: " + str(hit) + "\nMisses: " + str(miss))

#Now the feature hasher with 1000 features is created.
fHasher = FeatureHasher(n_features=1000)

#The hashed "wordbag" is created, using the feature hasher,
#And the helper function matrixToDict()
hashedBag = fHasher.transform(matrixToDict(wordbag))
arrayHashedBag = hashedBag.toarray()

#Once again 80% of the data is sourced.
x = arrayHashedBag[0:int(len(arrayHashedBag)*0.8)]
y = topics[0:int(len(topics)*0.8)]

#The classifer from before is now fit to the transformed data
forest.fit(x,y)

#And the fitted classifier is once again set to predict the class labels.
predictedAnswers = forest.predict(arrayHashedBag[int(len(arrayHashedBag)*0.8):])
realAnswers = topics[int(len(arrayHashedBag)*0.8):]

#Finally the new hit- and miss-rate is calculated.
hit = 0
miss = 0
for i in range(0, len(predictedAnswers)):
    if predictedAnswers[i] == realAnswers[i]:
        hit +=1
    else:
        miss +=1

print("Hits: " + str(hit) + "\nMisses: " + str(miss))