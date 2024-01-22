import os
import openai
import sys
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

message = ""
for i in range (1, len(sys.argv)):
    message += " "+sys.argv[i]

if message: 
    message= [{"role": "user", "content": message}]
    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=message
    )
    print(chat.choices[0].message.content)
else:
    raise Exception("please input your message")

# Refer this for setting virtual environment variable
# https://phoenixnap.com/kb/linux-set-environment-variable