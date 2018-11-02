from wit import Wit

access_token = "VE64C2OZJDQHNXAAOA3T2A6R2BDWPP54"

client = Wit(access_token = access_token)


message_text = "I live in canada"

resp = client.message(message_text)

print(resp)