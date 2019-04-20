import json

def my_func(event, context): 
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({ 'username': 'thisistheusername', 'id': 12 })
    }