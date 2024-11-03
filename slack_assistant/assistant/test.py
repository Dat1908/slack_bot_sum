# from domain.use_cases.ClassifyRequest import ClassifyRequest
# from dotenv import load_dotenv
# from application.services.summarize_service import SlackSummarizer
# from infrastructure.SlackClient import SlackClient
# from domain.use_cases.summarize_thread import Summarize
# from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
# import os
# load_dotenv()
# llm_token = os.environ.get("GOOGLE_API_KEY")
# slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")

# bot = ClassifyRequest(llm_token)
# bot_sum = SlackSummarizer()
# bot_slack = SlackClient(slack_bot_token)
# # text = "I want to have a summarize for this text: <user123> hello world"
# # result = bot.classify(text)
# # print(result)
# # thread_id = "1724308220.893389"
# # thread_id_file = "1722406429.343739"
# # channel_id = "C07BSH28MB4"
# # max_tokens = 4000
# # # bot = Summarize(model_name, key)
# # # results = bot.get_all_data(slack_bot_token,channel_id,thread_id_file)
# # # print(results[0])
# # # print("^^^^")
# # # print(results[1])
# # data = bot_slack.get_thread(channel_id, thread_id_file)
# # messages = data.messages
# # urls = []
# # texts = []
# from prompt_arrange import prompt

# # # Duyệt qua danh sách tin nhắn và lấy các giá trị
# # for msg in messages:
# #     if msg.attachment is not None:
# #         for att in msg.attachment:
# #             urls.append(att['url_private'])
# #             texts.append(msg.text)

# # In kết quả
# # print("URLs:", urls)
# # print("Texts:", texts)
# input = ['','mẫu tham khảo','cv của em đây ạ','tài liệu tham khảo','','']
# formatted_template = prompt.format(human_input=input)
# result = bot_arrange.invoke(formatted_template)
# print("*********")
# print(result.text)
# # result = [
# #     {"text": msg.text, "url_private": att['url_private']}
# #     for msg in messages if msg.attachment is not None
# #     for att in msg.attachment
# # ]
# # print(result)
# # # In kết quả
# # for item in result:
# #     print(f"Text: {item['text']}, URL: {item['url_private']}")
# # attachments = [msg.attachment for msg in messages if msg.attachment is not None]
# # messages_without_attachment = [msg for msg in messages if msg.attachment is None]
# # print(messages)
# # link_file = []
# # text_file = []
# # if attachments != []:
# #     for i in range(len(attachments)):
# #         link_file.append(attachments[i][0]['url_private'])
# # print(attachments)   


# # print(link_file)
# # print(text_file)
# # print("**********")
# # print(messages_without_attachment)
# # # if result['summarize'] == 1:
# #     print("Summarizing the text...")
# #     print(bot_sum.run(channel_id, thread_id, max_tokens))
# # elif result['recommend'] == 1:
# #     print("Recommending...")
    
# # else:
# #     print("No action needed.")
    
from infrastructure.SlackClient import SlackClient
from dotenv import load_dotenv
from domain.use_cases.summarize_doc import Summarize_doc
from domain.use_cases.summarize_thread import Summarize
from domain.use_cases.interact_bot import interact
load_dotenv()
import os 
import re 
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")

# bot = SlackClient(slack_bot_token)
channel_id = 'C07U89CQGEA'
thread_id =  '1730594527.347199'
user_id = 'U07UC5R7AFP'
# data = bot.get_thread(channel_id=channel_id, thread_id= thread_id)

# messages = data.messages

# # Lọc và loại bỏ các phần tử khớp với biểu thức chính quy
# # texts = [message.text for message in messages]
# # print(texts)
# # pattern = r'<@.*?>'

# # # Lọc và loại bỏ các phần tử khớp với biểu thức chính quy
# # clear_text = [msg for msg in texts if isinstance(msg, str) and not re.match(pattern, msg)]
# # print(clear_text)
# links = []
# texts = []

# # Duyệt qua danh sách tin nhắn và lấy các giá trị
# for msg in messages:
#     if msg.attachment is not None:
#         for att in msg.attachment:
#             links.append(att['url_private'])
#             texts.append(msg.text)
# print(links)
# print(texts)
# from domain.use_cases.summarize_doc import Summarize_doc
# model_name = os.environ.get("MODEL_NAME")
# key = os.environ.get("GOOGLE_API_KEY")
# bot_sum_doc = Summarize_doc(model_name=model_name, api_key=key)
# result = bot_sum_doc.summarize_doc(links_list= links, texts_list=texts)
# print(result)
max_tokens = 1000
model_name = os.environ.get("MODEL_NAME")
key = os.environ.get("GOOGLE_API_KEY")
bot_sum_text = Summarize(model_name, key)
result2 = bot_sum_text.summarize_thread(slack_bot_token, channel_id,thread_id,max_tokens)
bot_sum_doc = Summarize_doc(model_name = model_name, api_key= key)
result = bot_sum_doc.summarize_doc(slack_bot_token, channel_id, thread_id)
total_result = result + result2
print(total_result)
print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
documents = total_result
human_input = """tôi muốn đường dẫn đến tài liệu"""
bot_interact = interact(model_name=model_name, api_key=key)
result3 = bot_interact.interact_with_human(documents=documents, human_input=human_input)
print(result3)


# from domain.use_cases.ClassifyRequest import ClassifyRequest
# from dotenv import load_dotenv
# from application.services.summarize_service import SlackSummarizer
# from infrastructure.SlackClient import SlackClient
# from domain.use_cases.summarize_thread import Summarize
# from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
# import os
# from prompt_arrange import prompt
# model_name = os.environ.get("MODEL_NAME")
# key = os.environ.get("GOOGLE_API_KEY")
# bot_arrange = GeminiAdapter(key, model_name)
# input = ['','mẫu tham khảo','cv của em đây ạ','tài liệu tham khảo','','']
# formatted_template = prompt.format(human_input=input)
# result = bot_arrange.invoke(formatted_template)
# result_text = result.text
# print(result_text)
# number_result_text = []
# for text in result_text:
#     if ((text == '1') or(text == '0')):
#         number_result_text.append(text)
# print(number_result_text)
# # for i in range(len(number_result_text)):
# #     print(number_result_text[i])

# from domain.use_cases.summarize_thread import Summarize
# from dotenv import load_dotenv
# import os
# load_dotenv()
# model_name = os.environ.get("MODEL_NAME")
# model_api_key = os.environ.get("GOOGLE_API_KEY")
# slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
# bot_sum = Summarize(model_name=model_name, api_key= model_api_key)
# channel_id = 'C07U89CQGEA'
# thread_id =  '1730594527.347199'
# max_tokens = 1000
# sum_text = bot_sum.summarize_thread(slack_token = slack_bot_token, channel_id= channel_id, thread_id = thread_id, max_tokens= max_tokens)
# print(sum_text)