import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
data = {
    'name': 'Apple',
    'calorie': 95,
    'protein': 0,
    'carbs': 25,
    'fat': 0,
    'expiry_date': '2023/12/31'
}


doc_ref = db.collection('food_items_collection').document()
doc_ref.set(data)

print('Document ID:', doc_ref.id)