import os 
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from infrastructure.SlackClient import SlackClient
from domain.use_cases.interact_bot import interact
from domain.use_cases.summarize_doc import Summarize_doc
from domain.use_cases.summarize_thread import Summarize
from domain.use_cases.classify_file import classify_file
import re
from slack_sdk import WebClient

load_dotenv('.env')
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
model_name = os.environ.get("MODEL_NAME")
api_key = os.environ.get("GOOGLE_API_KEY")
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def extract_user_id_from_event(event):
    # Duyệt qua các phần tử trong blocks để tìm user_id
    for block in event['blocks']:
        for element in block['elements']:
            for sub_element in element['elements']:
                if sub_element['type'] == 'user':
                    return sub_element['user_id']
client = WebClient(token=slack_bot_token)
bot = SlackClient(slack_bot_token)         
bot_classify = classify_file(model_name, api_key)
bot_sum_thread = Summarize(model_name, api_key)
bot_sum_doc = Summarize_doc(model_name, api_key)
bot_interact = interact(model_name, api_key)
max_tokens = 1000
documents = None

@app.event("app_mention")
def handle_app_mention_events(body, logger):
    global documents
    logger.info(body)  
    print(body)  
    channel_id = body['event']['channel']
    thread_id = body['event']['thread_ts']
    user = body['event']['user']
    # print(channel, event_ts, user)
    response = app.client.conversations_open(users=user)
    result_text = bot_sum_thread.summarize_thread(slack_bot_token, channel_id, thread_id,max_tokens)
    texts_doc, links_doc = bot_classify.links_and_texts_of_doc(slack_bot_token, channel_id, thread_id)
    result_doc = bot_sum_doc.summarize_doc(links_doc,texts_doc)
    result = result_text + result_doc
    documents = result
    if response['ok']:
        direct_channel_id = response['channel']['id']
        
        app.client.chat_postMessage(
            channel=direct_channel_id,
            text= result
        )
    else:
        print("Can't open conversation.", response['error'])
        

@app.message(".*")
def message_handler(payload,say):
    # print(payload)
    text_with_mention = payload['text']
    pattern = r"<@\w+>\s*(.*)"
    match = re.match(pattern, text_with_mention)
    if match:
        text_without_mention = match.group(1)
        # print(text_without_mention)  
    else:
        print("No match found")
    result = bot_interact.interact_with_human(data = documents, human_input = text_without_mention)
    say(result)
    
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()