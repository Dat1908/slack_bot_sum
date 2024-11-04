prompt = """Rules:
    1. Only return 1 if important and 0 if not important.
    2. The texts are given as a list, and the content is placed in '.
        Exmaple: ['tài liệu','vâng ạ', 'bai bai'] , texts are tài liệu, vâng ạ, bai bai. 
    3. One text is considered important if it includes:  documents, sample articles, or some texts related to reference, learning, test,....
    4. One text is considered not important if it includes: normal saying(hi, hello,...), text is not important, normal conversations, empty text, and text only include special characters such as: ',@,!,#,*.
    5. You must always return a list of numbers 0 or 1, refer to some examples below
        Examples:
            Ex1: Input: ['tài liệu','vâng ạ', 'bai bai']
                 Output: ['1','0','0']
            Ex2: Input:['bài kiểm tra','hi', 'hello','tài liệu','']
                 Output: ['1','0','0','1','0']
    6. If there are many text with the same content, you must return the same value.
    7. You must analyze all languages.
You will be penalized if you don't follow these rules. 
Based on the rules above, evaluate and return the list bellow:
{human_input}"""