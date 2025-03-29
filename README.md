# Chat Bot - Dining Concierge

## Overview
This project is a **Dining Concierge Chatbot**, developed as part of the Cloud Computing coursework at the University of Michigan-Dearborn. The chatbot is designed to provide users with personalized restaurant recommendations based on their preferences such as location, cuisine, and time. 

The chatbot operates as a **serverless, microservice-driven application**, leveraging AWS cloud services to ensure scalability and reliability. The core functionalities are built using **AWS Lambda, API Gateway, Amazon Lex, and DynamoDB**, while the Yelp API is integrated to fetch real-time restaurant suggestions. 

The chatbot interacts with users via **Amazon Lex**, processing natural language queries to extract relevant details about their dining preferences. The user input is processed by AWS Lambda functions, which retrieve data from **DynamoDB and Elasticsearch**, ensuring quick and accurate responses. The chatbot also integrates **Amazon Simple Notification Service (SNS)** to send restaurant recommendations directly to users via SMS. 

Additionally, the frontend is hosted on **AWS S3**, providing a web-based interface for users to interact with the chatbot. The overall architecture follows a fully serverless paradigm, reducing infrastructure overhead and ensuring cost efficiency.

## Features
- **Conversational Interface:** Interacts with users via Amazon Lex.
- **Restaurant Recommendations:** Uses Yelp API to fetch restaurant suggestions.
- **Serverless Architecture:** Hosted using AWS Lambda, API Gateway, and S3.
- **Data Storage:** Stores restaurant data in DynamoDB and Elasticsearch.
- **SMS Notifications:** Sends restaurant suggestions via AWS SNS.

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript (hosted on AWS S3)
- **Backend:** AWS Lambda (Python/Node.js)
- **API Gateway:** REST API for handling chatbot requests
- **Database:** Amazon DynamoDB for storing restaurant data
- **External APIs:** Yelp API for fetching restaurant details
- **Other AWS Services:** Lex (Chatbot), SNS (Notifications), Elasticsearch (Search Optimization)

## Installation & Setup
### 1. Clone the repository
```bash
 git clone https://github.com/Sourabh-Harapanahalli/Chat_Bot.git
 cd Chat_Bot
```
### 2. Setup AWS Services
#### 2.1 Create an S3 Bucket for Frontend Hosting
1. Open the AWS Management Console and go to the **S3** service.
2. Click **Create Bucket**, enter a unique name, and choose a region.
3. Disable **Block all public access** to allow hosting.
4. Enable **Static website hosting** in the bucket properties.
5. Upload your frontend files (HTML, CSS, JS) and note the S3 endpoint URL.
6. Update the **bucket policy** to allow public read access:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```
#### 2.2 Deploy AWS Lambda Functions
1. Open AWS Lambda and click **Create Function**.
2. Choose **Author from scratch**, name the function (e.g., `ChatBotHandler`), and select a runtime (Python or Node.js).
3. Write or upload the chatbot handling code.
4. Assign necessary permissions for invoking Lambda via API Gateway.
5. Deploy the function and note the ARN.

#### 2.3 Configure Amazon API Gateway
1. Open API Gateway in the AWS Console.
2. Click **Create API** → Select **REST API**.
3. Define an **API Resource** and create a **POST method**.
4. Integrate the API with the Lambda function created in step 2.2.
5. Enable **CORS** for API Gateway to allow requests from the frontend.
6. Deploy the API and obtain the API endpoint URL.

#### 2.4 Set Up Amazon Lex Chatbot
1. Open **Amazon Lex** and click **Create Bot**.
2. Define intents such as `GreetingIntent`, `DiningSuggestionsIntent`, and `ThankYouIntent`.
3. Configure **utterances** for each intent (e.g., "I need restaurant suggestions").
4. Attach a **Lambda function** (created in step 2.2) as a fulfillment code hook.
5. Train and deploy the chatbot.

#### 2.5 Store Data in Amazon DynamoDB
1. Open **DynamoDB** and create a table named `yelp-restaurants`.
2. Define a **Primary Key** (e.g., `RestaurantID`).
3. Use AWS SDK or Lambda functions to populate the table with restaurant data from Yelp API.

#### 2.6 Integrate Yelp API
1. Register for a **Yelp API Key** from [Yelp Developers](https://www.yelp.com/developers).
2. Fetch restaurant data using:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
 "https://api.yelp.com/v3/businesses/search?location=Manhattan&categories=sushi&limit=1000"
```
3. Store fetched data in **DynamoDB** for fast access.

#### 2.7 Enable SMS Notifications with Amazon SNS
1. Open **SNS** in the AWS Console.
2. Create a **Topic** for notifications.
3. Subscribe users to the topic (via phone numbers).
4. Modify the Lambda function to send restaurant suggestions via SNS.

#### 2.8 Optimize Search with Amazon Elasticsearch
1. Open **Amazon OpenSearch (formerly Elasticsearch)** in AWS.
2. Create an **Elasticsearch domain**.
3. Define an index named `restaurants`.
4. Store restaurant metadata for fast lookups.

## Usage
1. Open the chatbot interface hosted on **AWS S3**.
2. Start a conversation (e.g., "I need restaurant suggestions").
3. Provide details like location, cuisine, and number of people.
4. Receive real-time restaurant suggestions.
5. The bot sends a confirmation SMS with recommendations.

## File Structure
```
Chat_Bot/
│── ChatBotHandler(LF0).py       # AWS Lambda function for API interactions
│── BotResponse(LF1).py          # AWS Lambda function for chatbot responses
│── yelp_api_insert.py           # Yelp API integration script
│── frontend/                    # Frontend directory
│   │── index.html               # Main UI for the chatbot
│   ├── assets/                  # Static assets
│       ├── css/                 # Styling files
│       ├── javascript/          # JavaScript files
│── README.md                    # Project documentation
│── CHANGELOG.md                 # Version changes and updates
│── ECE528_SOURABH_HW1.pdf       # Report on project details
```

## Future Enhancements
- Implement OAuth for user authentication.
- Add voice interaction using **Alexa Skills Kit**.
- Improve recommendation system with **Machine Learning**.
- Expand to more cities and cuisines.


## License
This project is licensed under the **MIT License**.

