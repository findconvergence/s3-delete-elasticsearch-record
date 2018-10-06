# aws_s3_es_delete_record
# deletes an AWS Elasticsearch record when sent an AWS s3 'ObjectDelete' event via AWS Lambda

import json
import urllib
import boto3
from elasticsearch import Elasticsearch

s3 = boto3.client('s3')

# user constants
ES_ENDPOINT = 'xxxx-xxxx-region.es.amazonaws.com' # Your Elasticsearch endpoint URL
ES_PORT = 80 # AWS Elasticsearch port 80; default Elasticsearch port 9200
ES_INDEX = 's3' # Your Elasticsearch index
ES_DOC = 'object' # Your Elasticsearch doc type


def lambda_handler(lambda_event, context):
    print('Received Lambda Event: ' + json.dumps(lambda_event))
    es = connect_elasticsearch(ES_ENDPOINT, ES_PORT)
    delete_rec(es, lambda_event)


def connect_elasticsearch(ES_ENDPOINT, ES_PORT):
    _es = None
    _es = Elasticsearch(hosts=[{'host': ES_ENDPOINT, 'port': ES_PORT}])

    try:
        _es.ping()
        print('Elasticsearch Connected')
        return _es
    except Exception as e:
        print('Elasticsearch Not Connected - Abort')
        raise e
        exit()


def delete_rec(es, lambda_event):
    es_bucket = lambda_event['Records'][0]['s3']['bucket']['name']
    es_key = urllib.parse.unquote_plus(lambda_event['Records'][0]['s3']['object']['key'])

    es_search_body = {
        'query': {
            'bool': {
                'must': {
                    'match_all': {}
                },
                'filter': [
                    {'term': {'objectKey.keyword': es_key}},
                    {'term': {'bucket.keyword': es_bucket}}
                ]
            }
        }
    }

    try:
        print('Searching for: ' + es_bucket + '/' + es_key)
        retval = es.search(index=ES_INDEX, doc_type=ES_DOC, body=es_search_body, _source='_id')
        total = retval['hits']['total']
        print(total, 'hits for ' + es_bucket + '/' + es_key)
        count = 0
        while (count < total):
            es_doc_id = retval['hits']['hits'][count]['_id']
            delete_rec_item(es, es_doc_id)
            count = count + 1
        return 1
    except Exception as e:
        print('Search for Record Failed')
        raise e
        exit(5)


def delete_rec_item(es, es_doc_id):
    try:
        retval = es.delete(index=ES_INDEX, doc_type=ES_DOC, id=es_doc_id)
        print('Deleted: ' + es_doc_id)
        return 1
    except Exception as e:
        print('Deleting Record Failed')
        raise e
        exit(5)
