def process_search_query(source=' ',target=' '):
    if source !='' and target == '':
      body = {
              "query": {
                  "bool": {
                    "must":
                      { "match_phrase": { "Metaphors.Source domain": source}}
                  }
              }
            }


    elif source == '' and target != '':
      body = {
              "query": {
                  "bool": {
                    "must":
                      { "match_phrase": { "Metaphors.Target domain": target} }

                  }
              }
            }
    else:
      body = {
              "query": { 
                  "bool": { 
                    "must":[
                      { "match_phrase": { "Metaphors.Source domain": source}},
                      { "match_phrase": { "Metaphors.Target domain": target}}
                    ]
                  }
              }
            }
    
    return body

def process_advancesearch_query(source,target,singer,genre,include,exclude):

    must_list =[]
    must_not_list = []
    filter_list =[]

    if source != '':
        must_list.append({ "match_phrase": { "Metaphors.Source domain": source}})
    if target != '':
        must_list.append({ "match_phrase": { "Metaphors.Target domain": target}})
    if include != '':
        must_list.append({ "match_phrase": { "Metaphors.Metaphor": include}})

    if exclude != '':
        must_not_list.append({"match_phrase": {"Metaphors.Metaphor": exclude}})

    if singer != "Not Selected":
        filter_list.append({ "match_phrase": { "Singer_en": singer}})
    if genre != "Not Selected":
        filter_list.append({ "match_phrase": { "Genre_en": genre}})

    body = {
        "query": {
            "bool": {
                "must": must_list,
                "must_not" : must_not_list,
                "filter" : filter_list
            }
        }
    }

    return body





