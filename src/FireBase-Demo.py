import firebase_admin
from firebase_admin import db, credentials
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://recipeawaste-default-rtdb.firebaseio.com/"})

ref = db.reference("/")
ref.get()

#get the value here
db.reference("/name").get()

#set the value here
db.reference("/videos").set(3)
ref.get()

#update existing vlaue for key
db.reference("/").update({"language": "python"})
ref.get()

#update operation when not existing, key and value created
db.reference("/").update({"subscribed":True})
ref.get()

#push operation
db.reference("/titles").push().set("create modern ui in Python")

#transaction
def increment_transaction(current_val):
    return current_val + 1

db.reference("/title_count").transaction(increment_transaction)
print(ref.get("/title_count"))

#delete
db.reference("/subscribed").delete()



