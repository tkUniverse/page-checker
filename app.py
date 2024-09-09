from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import threading
import json
import os

app = Flask(__name__)
CORS(app)

if os.path.exists('lastPage.json'):
    with open('lastPage.json') as f:
        try:
            data = json.load(f)
            lastPage = int(data.get('lastPage', 1234))
        except (json.JSONDecodeError, ValueError):
            print("Error decoding JSON or converting to int, using default lastPage value", flush=True)
            lastPage = 1234
else:
    print("JSON file not found, using default lastPage value", flush=True)
    lastPage = 1234

def get_last_page():
    global lastPage
    print("Thread started", flush=True)
    while True:
        url = f"https://github.com/tkUniverse/en/blob/main/pages/{lastPage}.png"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Page {lastPage} exists", flush=True)
                lastPage += 1
                json.dump({'lastPage': lastPage}, open('lastPage.json', 'w'))
            else:
                #print(f"Page {lastPage} does not exist, status code: {response.status_code}", flush=True)
                pass
        except requests.RequestException as e:
            print(f"An error occurred: {e}", flush=True)
        time.sleep(1)

@app.route('/', methods=['GET'])
def update_last_page():
    global lastPage
    return jsonify({'lastPage': lastPage - 1})

if __name__ == '__main__':
    print("Starting Flask app", flush=True)
    thread = threading.Thread(target=get_last_page, daemon=True)
    thread.start()
    print("Thread started", flush=True)
    app.run(debug=False)