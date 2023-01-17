from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import json
import os
import sys
import logging

import process_search_query

app = Flask(__name__)
es_client = Elasticsearch('http://localhost:9200', http_auth=("elastic", "6vml0xMVoxE7kM+0kSd2"))

INDEX = 'sinhala-songs'

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'girl.png')
Flask_Logo_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'boy.png')


@app.route('/')
def homepage():
    return render_template('index.html', girl_image=Flask_Logo_1, boy_image=Flask_Logo_2)


@app.route('/', methods=['POST', 'GET'])
def search_box():
    print(request)
    if request.method == 'POST':
        source_query = request.form.get('source')
        target_query = request.form.get('target')
        genre = request.form.get('genre')
        singer = request.form.get('singer')
        include = request.form.get('include')
        exclude = request.form.get('exclude')

        if target_query is None:
            query_body = process_search_query.process_search_query(source_query)
        elif source_query is None:
            query_body = process_search_query.process_search_query(target=target_query)
        elif singer is not None :
            query_body = process_search_query.process_advancesearch_query(source_query,target_query,singer,genre,include,exclude)
        else:
            query_body = process_search_query.process_search_query(source_query, target_query)
        response = es_client.search(
            index=INDEX,
            body=query_body
        )
        hits = response['hits']['hits']

        hits_data = []

        for hit in hits:
            song_name = hit["_source"]["title"]
            Metaphors = hit["_source"]["Metaphors"]
            filterd_metaphors = []
            for met in Metaphors:
                if target_query == '':
                    if source_query in met["Source domain"]:
                        filterd_metaphors.append({"Metaphor": met["Metaphor"], "Meaning": met["Meaning"]})
                elif source_query == '':
                    if target_query in met["Target domain"]:
                        filterd_metaphors.append({"Metaphor": met["Metaphor"], "Meaning": met["Meaning"]})
                else:
                    if target_query in met["Target domain"] and source_query in met["Source domain"]:
                        filterd_metaphors.append({"Metaphor": met["Metaphor"], "Meaning": met["Meaning"]})
            hits_data.append({"title": song_name, "Metaphors": filterd_metaphors})

        num_results = len(hits)

        # hits
        for i in hits:
            print(i)

        # hit count
        print("number of results found :", num_results)

        return render_template('index.html', hits=hits_data, num_results=num_results, girl_image=Flask_Logo_1,
                               boy_image=Flask_Logo_2)

    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == "__main__":
    app.run(debug=True)
