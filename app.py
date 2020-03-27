import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import dialogflow
import os
import google.auth

app = Flask(__name__)

@app.route("/")
def hello():
    return "This is my application for testinguser"

@app.route("/wpmessage", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    #quote = getQuote()
    res = getResponseFromIntent(msg)
    resp.message(str(res))
    return str(resp)

def getQuote():
    try:

        url = "https://quotes15.p.rapidapi.com/quotes/random/"
        querystring = {"language_code":"en"}
        headers = {
            'x-rapidapi-host': "quotes15.p.rapidapi.com",
            'x-rapidapi-key': "db2b1e996bmshfc3b089fc27f101p14313ajsn8b1ee35c9979"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        if(response.status_code ==200):
             res = response.json()
             message = res["content"]
             name = res["originator"].get("name")
             quote = message + " ~ " + name
             return quote
        else:
            return "Feel empowered because that's the best you can do now!"
    except:
        return "A butterfly can't see its beautiful wings. But you can!"

def  detect_intent_texts(project_id, session_id, text, language_code):


    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("checking with dialogflow session command")
    if text:
        # Text Input
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        # Query
        query_input = dialogflow.types.QueryInput(text=text_input)
        # Response
        response = session_client.detect_intent(session=session, query_input=query_input)
        intent = response.query_result.intent.displayName
        fulfillment_text = response.query_result.fulfillment_text
        res = call_api_on_intent(intent, fulfillment_text)
        return res

def getResponseFromIntent(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "whatsapp-bot-akdqru.json"
    project_id = "whatsapp-bot-akdqru"
    session_id ="abcd"
    text = text
    language_code  ="en"
    print("Fetching Result From Dialogflow" )
    print(detect_intent_texts(project_id,session_id, text, language_code))
   # try :
    res = detect_intent_texts(project_id,session_id, text, language_code)
    return res
   # except:
#	return "Thanks for connecting, Let me connect back again :)"

#add the api for the jokes here only 

def call_api_on_intent(intent , fulfillment_text):
    if intent == "getQuote":
        return getQuote()
    else:
	return fulfillment_text

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5968)
