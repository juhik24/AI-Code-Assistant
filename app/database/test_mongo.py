from app.database.mongo import db

print("Connected!")

print(db.list_collection_names())
