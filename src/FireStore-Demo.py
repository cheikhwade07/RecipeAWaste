import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os # For environment variables, good practice



try:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    print("Please ensure the path to your service account key is correct and accessible.")
    exit() # Exit if initialization fails


db = firestore.client()

collection_name = "food_items_collection"

print("Project ID from key:", cred.project_id)

print(f"\nAttempting to read all documents from collection: '{collection_name}'")

try:

    docs = db.collection(collection_name).get()


    if not docs:
        print(f"No documents found in collection '{collection_name}'.")
    else:

        for doc in docs:
            print(f"Document ID: {doc.id}")
            print(f"Document Data: {doc.to_dict()}")
            print("-" * 30)

except Exception as e:
    print(f"An error occurred while reading documents: {e}")

