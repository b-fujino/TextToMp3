import requests
import logging
import json
from pydub import AudioSegment
from io import BytesIO
import base64
from text import text


GOOGLE_TTS_API_KEY="AIzaSyAeE_98nvthHC08_JzYkxAhdHLxN-t9lro"


def text_to_speech(text, number):
    """
    テキストを音声合成してファイルに保存する

    Parameters
    ----------
    text : str

    Returns
    -------
    None
    """

    # APIキーの取得
    API_KEY = GOOGLE_TTS_API_KEY

    langcode = "en-US"
    voicetype = "en-US-Wavenet-D"
    speed = 0.8
    pitch = -0.05

    # APIエンドポイント
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"

    # 音声合成のリクエストデータ
    pitch = pitch*20
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": langcode,
            "name": voicetype,  
    #            "ssmlGender": "MALE"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speed,
            "pitch": pitch
        }
    }

    # リクエスト送信
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # 結果を取得
    if response.status_code == 200:
        # Base64エンコードされた音声データをデコード
        audio_content = json.loads(response.text)["audioContent"]
        audio_data = base64.b64decode(audio_content)
        
        # バイナリデータを pydub の AudioSegment に変換
        mp3_data  =BytesIO(audio_data)
        mp3_data .seek(0)  

        # ファイルを保存
        sound = AudioSegment.from_file(mp3_data, format="mp3")
        sound.export(f"output_{number}.mp3", format="mp3") 

        print("音声ファイルを保存しました。")
    else:
        print("エラーが発生しました。")
        print(response.text)


if __name__ == "__main__":
    #　テキストを[eop]で分割
    text = text.split("[eop]")
    # テキストを音声合成してファイルに保存
    for i, t in enumerate(text):
        text_to_speech(t, i)
        print(f"{i+1}/{len(text)}")
    print("全ての音声ファイルを保存しました。") 

    # ファイルの結合
    sound = AudioSegment.empty()
    for i in range(len(text)):
        sound += AudioSegment.from_file(f"output_{i}.mp3", format="mp3")   
    sound.export("output.mp3", format="mp3")
    print("音声ファイルを結合しました。")   
