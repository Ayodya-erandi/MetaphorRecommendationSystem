# Sinhala song metaphors search engine

## Usage

1. Start Elasticsearch
2. Create the index by running utils.py
3. Start search engine app by running app.py 

## Metadata

Following 10 metadata with the metaphors fo 150 songs are used to create the index in Elasticsearch.

1. Title
2. Singer
3. Genre
4. Lyricist
5. Composer
6. song_lyrics
7. Metaphor
    8. Source domain
    9. Target domain
    10. Meaning of the metaphor

## Data

- data directory - song-corpus/

## Main Usecases

* Normal Search. 
    - search metaphors by source domain
    - search metaphors by target domain
    - search metaphors by both source domain and target domain

* Advanced Search
    - Addition to the normal search, you can filter songs by,
        singer
        genre
    
    -Additionally, 
        you can include word in metaphor
        you can exclude word in metaphor

## Indexing techniques

Elasticsearch analysers are used in indexing.


