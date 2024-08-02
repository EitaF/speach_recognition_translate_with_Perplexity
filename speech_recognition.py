import speech_recognition as sr
import requests
import re

#Translate Japanese to English with Perplexity.

def tamego_to_teineigo_Perplexity(api, text, model = "llama-3-sonar-large-32k-online"):

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": """あなたは日本語の先生です。与えられたテキストを丁寧語に修正して下さい。説明などは不要。
                            例 :
                            {"だね$" : "ですね",
                             "こんにちは" : "ごきげんよう",
                             "だ" : "です"}"""
            },
            {
                "role": "user",
                "content": text
            }
       ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + api
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()["choices"][0]["message"]["content"]

#Use speech recognition.

r = sr.Recognizer()

is_first_time = True

while True:
    with sr.Microphone() as source:
        if is_first_time:
            r.adjust_for_ambient_noise(source, duration = 1)
            is_first_time = False
        print("Please speak to the microphone")
        audio = r.listen(source)

    try:
        recognized_text = r.recognize_google(audio, language='ja')
        print(f"Casual result[{recognized_text}]")
        teinei_text = tamego_to_teineigo_Perplexity(api = my_api, text = recognized_text)
        print(f"Formal result : [{teinei_text}]")

        #Say プログラム終了, then the loop will stop.
        if "プログラム終了" in recognized_text:
            break
    except sr.UnknownValueError:
        print("No recognition")
    except sr.Recognizer as e:
        print("Network error")
