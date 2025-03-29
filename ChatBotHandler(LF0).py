import json
import boto3
import uuid

def lambda_handler(event, context):
    # Parse the incoming event body
    body = json.loads(event['body'])
    user_message = body.get('message', '')

    lex_client = boto3.client('lexv2-runtime')
    

    try:
        # Call the Lex bot to recognize the text
        response = lex_client.recognize_text(
            botId='UVHRPUWQOA',  
            botAliasId='TSTALIASID',  
            localeId='en_US', 
            sessionId='sourabh',  
            text=user_message  
        )

        # Extract the response message
        messages = response.get('messages', [])
        message = messages[0].get('content', '') if messages else 'No response from bot.'

        return {
            'statusCode': 200,
            'body': json.dumps({'message': message}),
            'headers': {
            'Access-Control-Allow-Origin': '*'
                
            }
        }

    except Exception as e:
 
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred: ' + str(e)})
        }

