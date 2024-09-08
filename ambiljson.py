import firebase_admin
from firebase_admin import credentials, firestore
import json
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

# Inisialisasi Firebase
cred = credentials.Certificate('bot-unnes-telegram-firebase-adminsdk-7f07u-ae6d5dcc83.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def convert_datetime(obj):
    if isinstance(obj, DatetimeWithNanoseconds):
        # Convert to ISO 8601 format
        return obj.isoformat()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def fetch_data():
    # Ambil semua dokumen dari koleksi 'messages'
    collection_ref = db.collection('active_chats')
    docs = collection_ref.stream()

    data = {}

    # Iterasi melalui setiap dokumen dalam koleksi
    for doc in docs:
        # Menambahkan pengecekan untuk memastikan setiap dokumen ditangani dengan benar
        doc_dict = doc.to_dict()
        print(f"Document ID: {doc.id}, Data: {doc_dict}")  # Debugging print
        data[doc.id] = doc_dict

    # Serialize with custom conversion for datetime
    output_file = 'data.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, default=convert_datetime)

    print(f'Data saved to {output_file}')

fetch_data()
