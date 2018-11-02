import sys
from flask import Flask, request, render_template
from pprint import pprint
from pymessenger import Bot
from utils import wit_response, get_news_elements


app = Flask(__name__)

FB_ACCESS_TOKEN = "EAAagZBYCBTiMBAB4g8uZBOiS2DwnjCSVTPEwBZA9wdJyfCbZBVeWg0FPMMjYoUDwZAZBHGQ8lAfbIZBmCmOaOsNLu2XJkVHwJIrUd6Bu48GN096mO3VKVDf6A6VtFJywHxJk7IRb3RqLiHRT2Ry8OAWbA39mUwm45onyaYjx2g1AgZDZD"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # Necessary Code that extract json data facebook send
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # Code for Messenger Template
                    categories = wit_response(messaging_text)
                    elements = get_news_elements(categories)
                    bot.send_generic_message(sender_id, elements)

    return "ok", 200


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()

# for facebook apps Privacy-Policy necessary
@app.route('/Privacy-Policy')
def PrivacyPolicy():
	return render_template("Privacy-Policy.html")

# For heroku deployment Remove port
if __name__ == "__main__":
    app.run(use_reloader=True)
