import random
import string

def lambda_handler(event, context):
    length = event.get('length', 8)
    uppercase = event.get('uppercase', True)
    numbers = event.get('numbers', True)
    symbols = event.get('symbols', False)

    characters = string.ascii_lowercase

    if uppercase:
        characters += string.ascii_uppercase
    if numbers:
        characters += string.digits
    if symbols:
        characters += string.punctuation
    
    password = ''.join(random.choices(characters, k=length))
    
    return {
        'statusCode': 200,
        'body': {
            'password': password,
            'length': length
        }
    }