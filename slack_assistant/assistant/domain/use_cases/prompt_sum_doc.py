prompt = """Rules:
    1. You must summarize same language with the content.
    2. The content only includes links and corresponding texts.
    Example:
    Links: ['https://image1.png', 'https://files.pdf', 'https://image2.png']
    Texts: ['tài liệu tham khảo python', 'Bài mẫu cho code c++', 'paper cần đọc']
    You must understand above example that: 
    The link 'https://image1.png' has text is 'tài liệu tham khảo python'.
    The link 'https://files.pdf' has text is 'Bài mẫu cho code c++'.
    The link 'https://image2.png' has text is 'paper cần đọc'. 
    3. You only need summarize the links and the corresponding texts by listing them out in order 1,2,3...
    Example:
    Input:
    Links: ['https://image1.png', 'https://files.pdf', 'https://image2.png']
    Texts: ['tài liệu tham khảo về python', 'Bài mẫu cho code c++', 'paper cần đọc'] 
    Output:
    1. Tài liệu tham khảo cho python là https://image1.png. 
    2. Bài mẫu cho code c++ là https://files.pdf.
    3. Các paper cần đọc là https://image2.png
    4. You can change the text for a smoother description but you must not change the meaning of texts.
You will be penalized if you don't follow these rules.
You are a assistant. Based on the rules above, summarize the following content (you must awnswer in the same language with content):
{links_input}
{texts_input}"""