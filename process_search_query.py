def process_search_query():

    body = {
            "query": {
                "multi_match": {
                  "query" : "අම්මා",
                  "type" : "best_fields",
                  "fields" : ["Metaphors.Source domain.keyword"]
                    
                }
            }
            }
    return body
