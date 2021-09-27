import firebase_admin
from firebase_admin import credentials, firestore
import requests
from random import randrange
import json


cred = credentials.Certificate(
    "brydge-2021-firebase-adminsdk-eg8ur-0fbdf437dc.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brydge-2021.firebaseio.com/'
})
db = firestore.client()
workerRef = db.collection('users').document('workerNames')

def generateWorkerName():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    word1 = response.content.splitlines()[randrange(10000)].decode('utf-8').capitalize()
    word2 = response.content.splitlines()[randrange(10000)].decode('utf-8').capitalize()
    randNumber = str(randrange(100))
    return word1 + word2 + randNumber

def parseRequest(request):
    data = request.data.decode('utf-8')
    payload = json.loads(data)
    return payload['wallet']

def addWorkerToDB(request):
    wallet = parseRequest(request)
    workerName = generateWorkerName()
    workerRef.set({ wallet: workerName }, merge=True)
    print('wallet: ', wallet, ' given workerName: ', workerName)
    return wallet