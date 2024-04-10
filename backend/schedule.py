# generate headers
HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': True,
    'Access-Control-Allow-Headers': '*',
}

def get_schedule(): 
    return {
        "statusCode": 200,
        "body": "Get request successful",
        "headers": HEADERS
    }


def post_schedule():
    return {
        "statusCode": 200,
        "body": "Post request successful",
        "headers": HEADERS
    }