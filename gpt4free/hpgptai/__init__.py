# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/22 14:04
@Auth ： Hp_mzx
@File ：__init__.py.py
@IDE ：PyCharm
"""
import json
import requests
import random
import string

class ChatCompletion:
    @staticmethod
    def create(
            messages: list,
            context: str="Converse as if you were an AI assistant. Be friendly, creative.",
            restNonce:str="9d6d743bd3",
            proxy:str=None
    ):
        url = "https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat"
        headers = {
            "Content-Type": "application/json",
            "X-Wp-Nonce": restNonce
        }
        proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy} if proxy else None
        data = {
            "env": "chatbot",
            "session": "N/A",
            "prompt": ChatCompletion.__build_prompt(context,messages),
            "context": context,
            "messages": messages,
            "newMessage": messages[-1]["content"],
            "userName": "<div class=\"mwai-name-text\">User:</div>",
            "aiName": "<div class=\"mwai-name-text\">AI:</div>",
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "maxTokens": 1024,
            "maxResults": 1,
            "apiKey": "",
            "service": "openai",
            "embeddingsIndex": "",
            "stop": "",
            "clientId": ChatCompletion.randomStr(),
        }
        res = requests.post(url=url, data=json.dumps(data), headers=headers, proxies=proxies)
        if res.status_code == 200:
            return res.json()
        return res.text


    @staticmethod
    def randomStr():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=34))[:11]

    @classmethod
    def __build_prompt(cls, context: str, message: list, isCasuallyFineTuned=False, last=15):
        prompt = context + '\n\n' if context else ''
        message = message[-last:]
        if isCasuallyFineTuned:
            lastLine = message[-1]
            prompt = lastLine.content + ""
            return prompt
        conversation = [x["who"] + x["content"] for x in message]
        prompt += '\n'.join(conversation)
        prompt += '\n' + "AI: "
        return prompt




class Completion:
    @staticmethod
    def create(prompt: str,proxy:str):
        messages = [
            {
                "content": prompt,
                "html": prompt,
                "id": ChatCompletion.randomStr(),
                "role": "user",
                "who": "User: ",
            },
        ]
        return ChatCompletion.create(messages=messages,proxy=proxy)