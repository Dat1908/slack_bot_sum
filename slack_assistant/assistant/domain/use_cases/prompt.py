recommend_prompt = """
You are an AI assistant helping to craft polite and engaging responses in a \
conversation.
Your task is to suggest a thoughtful reply based on the given context for \
{user_id}

Please generate a response that is:
1. Friendly and positive in tone
2. Relevant to the conversation topic
3. Encouraging further dialogue
4. Appropriate for the context (casual/formal)
5. Concise but not overly brief

Additional guidelines:
- Avoid controversial topics or offensive language
- Do not mention/tag any other user in your response
- Tailor the language to match the style of previous messages

Here's the conversation:

"""

classify_prompt = """Analyze the following user input and classify it into \
one of two categories: 'summarize' or 'recommend'. Determine if the user is \
asking for a summary of information or requesting a recommendation.

User Input:
{user_input}

Based on the user's input, classify the request as either 'summarize' or \
'recommend'. Respond with a JSON object where 0 means false and 1 means true \
for each category.

Your response should be in the following JSON format:
{{
  "summarize": 0 or 1,
  "recommend": 0 or 1
}}

If user's input doesn't falls into any type of request, set both to 0. Do not \
include any explanation or additional text in your response, \
only the JSON object.
"""
