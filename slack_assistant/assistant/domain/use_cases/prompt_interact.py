# prompt = """Rules:
#     1. You must answer the same language with the questioners.
#     2. If the questioner asks anything related to data then answer in data, if not in data then answer 
# You will be penalized if you don't follow these rules.
# Data: {documents}
# You are a assistant. Based on the data provided, address the questioner's requirements below (you must awnswer in the same language with questioners):
# {human_input}"""

prompt = """Rules:
Data: {documents}
You are a assistant. Based on the data provided, address the questioner's requirements below (you must awnswer in the same language with questioners):
{human_input}"""

# prompt = """Rules:
#     1. You must awnswer the same language with the questioners.
#     2. You must only answer what is in the document.
#     3. If the question is not in the documents provided, you must answer that it is not in the documents.
#     Documents:
#     {documents}
# You will be penalized if you don't follow these rules.
# You are a assistant. Based on the documents above,reply the questioners (you must awnswer in the same language with questioners):
# {human_input}"""