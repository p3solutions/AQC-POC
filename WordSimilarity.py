import requests

class WordSimilarity:
    url = "http://localhost:8080/wordnet/Similarity"
    headers = {'content-type': 'application/json'}
    data = dict()
    def __init__(self):
        pass

    def getSimilarity(self, word1, word2):

        WordSimilarity.data["word1"] = word1
        WordSimilarity.data["word2"] = word2

        response = requests.post(WordSimilarity.url, params=WordSimilarity.data, headers=WordSimilarity.headers)
        return response.text

wordSimilarity = WordSimilarity()
wordSimilarity.getSimilarity("scopes", "book")
