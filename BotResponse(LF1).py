import json
import boto3
import logging
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the DynamoDB resource and SNS client
dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table('yelp-restaurants')
sns_client = boto3.client('sns')

# Helper function to convert Decimal types to float for JSON serialization
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def format_sns_message(suggestions):
    """Formats the restaurant suggestions into a more readable format."""
    message = "Here are the restaurant suggestions:\n\n"
    
    for idx, restaurant in enumerate(suggestions, 1):
        message += f"Restaurant {idx}:\n"
        message += f"Name: {restaurant['Name']}\n"
        message += f"Location: {restaurant['City']}\n"
        message += f"Phone: {restaurant['Phone']}\n"
        message += f"Rating: {restaurant['Rating']}\n"
        message += f"Cuisine: {restaurant['Cuisine']}\n"
        message += "\n"  

    return message

def lambda_handler(event, context):
    # Log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")

    # Extract the intent name
    intent_name = event['sessionState']['intent']['name']

    # Based on the intent, call the appropriate handler function
    if intent_name == 'GreetingIntent':
        return handle_greeting_intent(event)
    elif intent_name == 'ThankYouIntent':
        return handle_thank_you_intent(event)
    elif intent_name == 'DiningSuggestionsIntent':
        return handle_dining_suggestions_intent(event)
    elif intent_name == 'FallbackIntent':
        return handle_fallback_intent(event)
    else:
        return fallback_response("Sorry, I couldn't recognize that intent.")

# Intent Handlers

def handle_greeting_intent(event):
    response_message = "Hi there! How can I assist you today?"
    return close_intent_with_message(event, response_message)

def handle_thank_you_intent(event):
    response_message = "You're welcome! Let me know if there's anything else I can help with."
    return close_intent_with_message(event, response_message)

def handle_dining_suggestions_intent(event):
    slots = event['sessionState']['intent'].get('slots', {})

    # Safely capture the slot values
    location = slots.get('Location', {}).get('value', {}).get('interpretedValue', None) if slots.get('Location') else None
    cuisine = slots.get('Cuisine', {}).get('value', {}).get('interpretedValue', None) if slots.get('Cuisine') else None
    dining_time = slots.get('DiningTime', {}).get('value', {}).get('interpretedValue', None) if slots.get('DiningTime') else None
    party_size = slots.get('NumberOfPeople', {}).get('value', {}).get('interpretedValue', None) if slots.get('NumberOfPeople') else None
    phone_number = slots.get('PhoneNumber', {}).get('value', {}).get('interpretedValue', None) if slots.get('PhoneNumber') else None

    # Check for missing slot values and prompt the user
    if not location:
        return elicit_slot(event, "Location", "Great. I can help you with that. What city or city area are you looking to dine in?")
    
    if not cuisine:
        return elicit_slot(event, "Cuisine", "What type of cuisine would you like to try?")
    
    if not party_size:
        return elicit_slot(event, "NumberOfPeople", "How many people will be in your party?")
    
    if not dining_time:
        return elicit_slot(event, "DiningTime", "What time would you like to dine?")
    
    if not phone_number:
        return elicit_slot(event, "PhoneNumber", "Please provide your email so I can send you the restaurant suggestions.")
    
    
    try:
        # Scan the DynamoDB table for matching restaurants
        response = dynamo_table.scan(
            FilterExpression='City = :location AND Cuisine = :cuisine',
            ExpressionAttributeValues={
                ':location': location,
                ':cuisine': cuisine
            }
        )

        # Get the restaurant suggestions from the response
        restaurant_suggestions = response.get('Items', [])
        

        if restaurant_suggestions:
            limited_suggestions = restaurant_suggestions[:3]
            #logger.info(f"Restaurant suggestions: {limited_suggestions}")
            
            response_message = f"Here are some {cuisine} restaurant suggestions in {location} for {party_size} people at {dining_time}:\n"
            for idx, restaurant in enumerate(limited_suggestions, 1):
                response_message += f"{idx}. {restaurant['Name']}, located at {restaurant['City']}\n"
                
            logger.info(f"Restaurant suggestions: {response_message}")
            
            # Format the message for SNS
            sns_message = format_sns_message(convert_decimals(limited_suggestions))
            
            # Publish the message to SNS
            try:
                sns_response = sns_client.publish(
                    TopicArn='arn:aws:sns:us-east-1:688567269565:BotMessage',
                    Message=sns_message,
                    Subject="Restaurant Suggestions"
                )
                logger.info(f"SNS message published successfully: {sns_response}")
            except Exception as e:
                logger.error(f"Error publishing to SNS: {e}")
        else:
            response_message = f"Sorry, I couldn't find any {cuisine} restaurants in {location}."

    except Exception as e:
        response_message = f"An error occurred while retrieving restaurant suggestions: {str(e)}"

    return close_intent_with_message(event, response_message)

def handle_fallback_intent(event):
    response_message = "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"
    return close_intent_with_message(event, response_message)


def elicit_slot(event, slot_name, message):
    """ Elicit a slot if it's missing """
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_name
            },
            'intent': {
                'name': event['sessionState']['intent']['name'],
                'slots': event['sessionState']['intent']['slots'],
                'state': 'InProgress'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message
            }
        ]
    }

def close_intent_with_message(event, message):
    """ Close the intent with a success message """
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': event['sessionState']['intent']['name'],
                'state': 'Fulfilled'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message
            }
        ]
    }

def fallback_response(message):

    return {
        'statusCode': 200,
        'body': json.dumps({
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': message
                }
            ]
            
        })
        
    }