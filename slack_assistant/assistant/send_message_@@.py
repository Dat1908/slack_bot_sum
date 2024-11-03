import os 
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from infrastructure.SlackClient import SlackClient
from slack_sdk import WebClient
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
load_dotenv('.env')
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

print(os.environ.get("SLACK_BOT_TOKEN"))
def extract_user_id_from_event(event):
    # Duyệt qua các phần tử trong blocks để tìm user_id
    for block in event['blocks']:
        for element in block['elements']:
            for sub_element in element['elements']:
                if sub_element['type'] == 'user':
                    return sub_element['user_id']
@app.event("app_mention")
def handle_app_mention_events(body, logger, say):
    logger.info(body)  # Ghi log thông tin sự kiện
    print(body)  # In thông tin ra console
    channel = body['event']['channel']
    event_ts = body['event']['event_ts']
    user = body['event']['user']
    print(channel, event_ts, user)
    response = app.client.conversations_open(users=user)
    
    if response['ok']:
        direct_channel_id = response['channel']['id']
        
        # Gửi tin nhắn vào hộp thư tin nhắn trực tiếp
        app.client.chat_postMessage(
            channel=direct_channel_id,
            text='Cảm ơn bạn đã đề cập đến tôi! Đây là tin nhắn từ bot.'
        )
    else:
        print("Không thể mở cuộc trò chuyện:", response['error'])
@app.message(".*")
def message_handler(message, say):
    print(message)
    
    output = "hi" 
    say(output)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()