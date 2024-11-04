prompt = """Rules:
    1. You must summarize same language with the content.
    2. You must not to use special characters such as *, $, %, #.
    3. In case, there are special characters such as *, $, %, # in the content, you can use them when you really need.
    4. The summary is always shorter than the content.
    5. Clearly state the sections related to the meeting schedule (all details of the meeting),everything has a specific time and location, and notices.
    6. If the summarize is long, it can be diveided into small sections according to the corresponding sections(can be divided into sections 1. 2. 3.).
You will be penalized if you don't follow these rules.
You are a assistant. Based on the rules above, summarize the following content (you must awnswer in the same language with content):
{human_input}"""