import boto3

def get_functions() -> list[dict]:
    session = boto3.Session(profile_name="jcreyescloud")
    client = session.client("lambda")
    paginator = client.get_paginator('list_functions')
    pages = paginator.paginate()
    list_functions = []

    for page in pages:
        list_functions.extend(page['Functions'])

    return list_functions