import os, sys
from flask import Flask, request,render_template
# from utils import wit_response
# from pymessenger import Bot
# from pprint import pprint

app = Flask("Copping")

FB_ACCESS_TOKEN = "EAAEwM5KUIVsBAGKZCeZBfaYPalWRQ0XxhKxJB7zZAN0UmSAz6PAJ70puNvAA2awndynoZCCXTNPLPitQF89cmitLXH5HhbQ4enX4WfeCxw5RZAReZCvh60JBW57BkCjwp5wCao321ZASYa6BU6xMj8DR9wLPnMPwjlo9x7ORuK3lQZDZD"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

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

					response = None

					entity, value = wit_response(messaging_text)
					if entity == 'newstype':
						response = "Ok, I will send you the {} news".format(str(value))
					elif entity == 'location':
						response = "Ok, so you live in {0}. Here are top headlines from {0}".format(str(value))

					if response == None:
						response = "Please Ask the question what is relevant to our product formalin remover"

					bot.send_text_message(sender_id, response)

	return "ok", 200



def log(message):
	print(message)
	sys.stdout.flush()



if __name__ == "__main__":
	app.run(port=80, use_reloader = True)