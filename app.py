from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json
import os

import process_search_query

app = Flask(__name__)
es_client = Elasticsearch('http://localhost:9200', http_auth =("elastic","6vml0xMVoxE7kM+0kSd2"))

INDEX = 'sinhala-songs'

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route('/')
def search_box():
    #print(request)
    method = 'POST'
    if method == 'POST':
        query = 'මුහුණ'
        query_body = process_search_query.process_search_query()

        response = es_client.search(
            index=INDEX,
            body=json.dumps(query_body)
        )
        hits = response['hits']['hits']
        #aggregations = response['aggregations']
        num_results = len(hits)

        # hits
        for i in hits:
            print(i)

        # aggregations
        #for j in aggregations:
            #print(j)

        # hit count
        print("number of results found :", num_results)

        Flask_Logo_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'girl.png')
        Flask_Logo_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'boy.png')
        return render_template('index.html', hits = hits, num_results = num_results, girl_image = Flask_Logo_1, boy_image = Flask_Logo_2 )

    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == "__main__":
    app.run(debug=True)
