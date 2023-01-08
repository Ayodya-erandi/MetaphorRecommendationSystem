from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json

es_client = Elasticsearch('http://localhost:9200', http_auth =("elastic","6vml0xMVoxE7kM+0kSd2"))
INDEX = 'sinhala-songs'

# define mappings and configs

configs = {
    "settings" : {
        "index" : {
            "analysis" : {
            "analyzer" : {
                "plain" : {
                "filter" : [],
                "tokenizer" : "standard"
                },
                "case_insensitive" : {
                "filter" : ["lowercase"],
                "tokenizer" : "standard"
                },
                "inflections" : {
                  "filter" : ["porter_stem"],
                  "tokenizer" : "standard"
                },
                "case_insensitive_and_inflections" : {
                  "filter" : ["lowercase", "porter_stem"],
                  "tokenizer" : "standard"
                }
            }
          }
        }
    },
    "mappings": {
        "properties": {
            "review_title": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
            "review_body": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
            "product_id": {
              "type": "keyword"
            },
            "language": {
              "type": "keyword"
            },
            "product_category": {
              "type": "keyword"
            },
            "stars": {
              "type": "integer"
            },
            "published_date": {
              "type": "date",
              "format": "MM/dd/yyyy"
            }
        }
    }
}

def index():
    res = es_client.indices.create(index=INDEX, body=configs)
    print(res)

    helpers.bulk(es_client, create_bulk())
    print(res)

def create_bulk():
    with open('song-corpus/songs.json') as json_file:
            json_data = json.load(json_file)
    for i in range(len(json_data)):
        yield {
            "_index": INDEX,
            "_source": {
                "title": json_data[i]['title'],
                "Singer_en": json_data[i]['Singer_en'],
                "Singer_si": json_data[i]['Singer_si'],
                "Genre_en": json_data[i]['Genre_en'],
                "Genre_si": json_data[i]['Genre_si'],
                "Lyricist_en": json_data[i]['Lyricist_en'],
                "Lyricist_si": json_data[i]['Lyricist_si'],
                "Composer_en": json_data[i]['Composer_en'],
                "Composer_si": json_data[i]['Composer_si'],
                #"Movie_en": json_data[i]['Movie_en'],
                #"Movie_si": json_data[i]['Movie_si'],
                "song_lyrics": json_data[i]['song_lyrics'],
                "Metaphors": json_data[i]['Metaphors']
            },
        }

# Call elasticsearch bulk API to create the index
if __name__ == "__main__":
    index()
