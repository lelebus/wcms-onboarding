import requests
from typing import Union


def query_conditions(name: str, winery_name: str, wine_type: str):
    # build query
    conditions = [
        {
            "multi_match": {
                "query": name,
                "fields": [
                    "name"
                ],
                "type": "best_fields",
                "operator": "or",
                            "fuzziness": "AUTO"
            }
        },
        {
            "multi_match": {
                "query": winery_name,
                "fields": [
                    "winery_name^2"
                ],
                "type": "best_fields",
                "operator": "or",
                            "fuzziness": "1"
            }
        }
    ]

    if wine_type is not None and wine_type != 'nan':
        conditions.append(
            {
                "constant_score": {
                    "filter": {
                        "term": {
                            "type.keyword": wine_type.upper()
                        }
                    },
                    'boost': 0
                }
            })

    return conditions


def query_es(name: str, winery_name: str, wine_type: str, num_matches: int = 1):
    """Perform query on ElasticSearch index.

    Parameters
    ----------
    name : str
        name of the wine
    winery_name : str
        name of the winery
    wine_type : str
        wine type, e.g. RED, WHITE etc
    num_matches : int
        Number of matches, sorted by decreasing score. by default 1

    Returns
    -------
    response : list of dict
        Response json of the ElasticSearch query.

        `None` if no match is found.
    
        Run `query_es_clean` for getting the first match and the score as separated values.

    """
    # perform query
    url = 'https://es.vinoteqa.com/wines/_search'
    headers = {'Content-Type': 'application/json'}
    query = {
        "query": {
            "bool": {
                "must": query_conditions(name, winery_name, wine_type),
            }
        },
        "size": num_matches
    }

    try:
        response = requests.post(url, headers=headers, json=query)
        return response.json()
    except Exception as e:
        print(f'ERROR ({name} - {winery_name})', e)
        return None


def query_es_clean(name: str, winery_name: str, wine_type: str):
    """Perform query on ElasticSearch index.

    Parameters
    ----------
    name : str
        name of the wine
    winery_name : str
        name of the winery
    wine_type : str
        wine type, e.g. RED, WHITE etc

    Returns
    -------
    match : dict
        Matching entry in the index.

        `None` if no match is found.

        Otherwise, the keys are:
        - `id`
        - `type`
        - `name`
        - `seo_name`
        - `winery_id`
        - `winery_name`
        - `winery_seo_name`

    score : float
        Matching score as calculated by ElasticSearch.

        `0` if no match is found.

        Run `query_explanation`
        for the explanation of the score.
    """
    response_json = query_es(name, winery_name, wine_type, 1)

    if response_json is None:
        return None, 0

    hits = response_json['hits']['hits']
    if len(hits) > 0:
        match = hits[0]['_source']
        return match, hits[0]['_score']
    return None, 0


def query_explain(name: str, winery_name: str, wine_type: str, matched_id: str = None):
    """Perform query on ElasticSearch index
    and get explanation for how the score is computed.

    Parameters
    ----------
    name : str
        name of the wine
    winery_name : str
        name of the winery
    wine_type : str
        wine type, e.g. RED, WHITE etc
    matched_id : str, optional
        id of matched wine. If not provided,
        a query to the ElasticSearch index is performed
        to find the closest match

    Returns
    -------
    explanation : dict
        Breakdown of the score components.
        `None` if no match is found.
    """

    if matched_id is None:
        match, score = query_es_clean(name, winery_name, wine_type)
        if match is None:
            print('No match')
            return
        matched_id = match['id']

    # perform explanation query
    url = 'https://es.vinoteqa.com/wines/_explain/' + matched_id
    headers = {'Content-Type': 'application/json'}
    query = {
        "query": {
            "bool": {
                "must": query_conditions(name, winery_name, wine_type),
            }
        }
    }

    return requests.post(url, headers=headers, json=query).json()


def query_by_id(wine_id: Union[str, list]):
    """Query the ElasticSearch index by `'wine_id'`.

    Parameters
    ----------
    wine_id : str | list of str

    Returns
    -------
    response : dict
        response of the query.
    """

    url = 'https://es.vinoteqa.com/wines/_search'
    headers = {'Content-Type': 'application/json'}

    query = {
        "query": {
            "ids": {
            "values": wine_id
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=query)

        hits = response.json()['hits']['hits']
        if len(hits) == 0:
            return []
        return [hit['_source'] for hit in hits]

    except Exception as e:
        print(f'ERROR', e)
        return None
