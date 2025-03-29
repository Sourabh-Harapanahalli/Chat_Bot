import boto3
import requests

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yelp-restaurants')

# Yelp API key and endpoint
YELP_API_KEY = 'NrC15sScKfUkzWKdeqKRcwrgkJMYLcttkc_6JsEGBZmNV6ojQojTNmI_vKbJGbf5k7e1FkZzPkbYqWl0rq-t86L4Q0oHTqVu8LxlM7eUZWzkmusngPnBhr-w2-wTZ3Yx'
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'

headers = {
    'Authorization': f'Bearer {YELP_API_KEY}'
}

# Function to get Yelp data
# def get_yelp_data(location, categories, limit=50):
#     params = {
#         'location': location,
#         'categories': categories,
#         'limit': limit
#     }
#     response = requests.get(YELP_API_URL, headers=headers, params=params)
#     return response.json()['businesses']

def get_yelp_data(location, categories, cuisine, limit=50):
    params = {
        'location': location,
        'categories': categories,
        'limit': limit
    }
    response = requests.get(YELP_API_URL, headers=headers, params=params)
    
    businesses = response.json().get('businesses', [])
    
    # Append the cuisine to each restaurant's data
    for business in businesses:
        business['cuisine'] = cuisine
    
    return businesses

# Function to insert data into DynamoDB
def extract_cuisine(categories):
    return ', '.join([category['title'] for category in categories])

def insert_into_dynamodb(restaurant):
    cuisine = extract_cuisine(restaurant.get('categories', []))
    table.put_item(
        Item={
            'RestaurantID': restaurant['id'],
            'Name': restaurant['name'],
            'Address': restaurant['location']['address1'],
            'City': restaurant['location']['city'],
            'State': restaurant['location']['state'],
            'ZipCode': restaurant['location']['zip_code'],
            'Phone': restaurant.get('phone', 'N/A'),
            'Rating': str(restaurant['rating']),
            'ReviewCount': str(restaurant['review_count'])
            ,'Cuisine':restaurant['cuisine']
            ,'NumberOfPeople':4
            ,
        }
    )

# Example usage
#yelp_data = get_yelp_data('Manhattan', 'sushi','sushi', 10)
#yelp_data = get_yelp_data('Manhattan', 'chinese','chinese', 10)
# yelp_data = get_yelp_data('Manhattan', 'italian','italian', 10)
# yelp_data = get_yelp_data('Brooklyn', 'sushi','sushi', 10)
# yelp_data = get_yelp_data('Brooklyn', 'chinese','chinese', 10)
yelp_data = get_yelp_data('Brooklyn', 'italian','italian', 10)

#print(get_yelp_data('Manhattan', 'sushi', 1))
# for restaurant in yelp_data:
#     print(restaurant['cuisine'])
#     #print(extract_cuisine(restaurant.get('categories', [])))

#cuisines = ['indian', 'thai', 'mediterranean', 'chinese', 'italian']

for restaurant in yelp_data:
    insert_into_dynamodb(restaurant)
    print(f"Inserted {restaurant['name']} into DynamoDB")
