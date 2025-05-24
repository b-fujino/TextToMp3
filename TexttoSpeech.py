import requests
import json
from pydub import AudioSegment
from io import BytesIO
import base64
from dotenv import load_dotenv
import os
import argparse

# 環境変数の読み込み
load_dotenv()



def text_to_speech(text, number, langcode, speed, pitch, voicetype):
    """
    テキストを音声合成してファイルに保存する

    Parameters
    ----------
    text : str
        音声合成するテキスト
    number : int
        音声ファイルの番号（出力ファイル名に使用）
    langcode : str
        言語コード（例: "en-GB"）
    speed : float
        話速（例: 0.9） 
    pitch : float
        ピッチ（例: 0.0）
    voicetype : str
        ボイスタイプ（例: "en-GB-Wavenet-D"）

    Returns
    -------
    None
    """

    # APIキーの取得
    API_KEY = os.getenv("GOOGLE_TTS_API_KEY")

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
        print(f"response.status_code:{response.status_code}" )
        print(f"response.text:{ response.text}") 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Text to Speech Converter\n\n"
            "このプログラムは引数で与えたテキストファイルを音声に変換します。\n"
            "音声合成にはGoogle Cloud Text-to-Speech APIを使用します。\n"
            "音声ファイルはMP3形式で保存されます。\n\n"
            "例: python TexttoSpeech.py -f text.txt -l en-GB -s 0.9 -p 0.0 -v en-GB-Wavenet-D -c True \n\n"
            "テキストファイルの中に、\"[eop]\"(end-of-page)がある場合，その個所でファイルが切り分けられます。\n\n"
        ),
        epilog=(
            "言語コードやボイスタイプは，次のリンクを確認してください\n\n"
            "https://cloud.google.com/text-to-speech/docs/voices \n\n"
            "使用する際にはGoogle TTS APIのAPIキーが必要です。\n"
            "APIキーの取得は次のリンクを参考にしてください\n\n"
            "https://qiita.com/fujino-fpu/items/f5deca52e8f708867f79 \n\n"
            "APIキーは環境変数\"GOOGLE_TTS_API_KEY\"に設定してください。\n"
            ".envファイルを使用する場合は、.envファイルに\"GOOGLE_TTS_API_KEY=your_api_key\"の形式で記述してください。\n\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
        
    )
    parser.add_argument("-f", "--file", required=True, help="テキストファイルのパス")
    parser.add_argument("-l", "--langcode", default="en-GB", help="言語コード (例: en-GB(デフォルト))")
    parser.add_argument("-s", "--speed", type=float, default=0.9, help="話速 (例: 0.9（デフォルト）)")
    parser.add_argument("-p", "--pitch", type=float, default=0.0, help="ピッチ (例: 0.0（デフォルト）)")
    parser.add_argument("-v", "--voicetype", default="en-GB-Wavenet-D", help="ボイスタイプ（例: en-GB-Wavenet-D（デフォルト））")
    parser.add_argument("-c", "--combine", default="True", help="結合ファイルを作成するか (True/False)（デフォルト: True）")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    # テキストを[eop]で分割
    text_split = text.split("[eop]")
    
    # テキストを音声合成してファイルに保存
    for i, t in enumerate(text_split):
        # テキストを各行に分けて，各行の行頭に#がある場合は削除し，再結合．
        if not t:
            continue
        t = "\n".join([line.lstrip("#").strip() for line in t.split("\n") if line.strip()])


        text_to_speech(t, i, args.langcode, args.speed, args.pitch, args.voicetype)
    

    # ファイルの結合
    if args.combine.lower() != "true":
        print("音声ファイルの結合はスキップされました。")
        exit(0)
    else:
        sound = AudioSegment.empty()
        for i in range(len(text_split)):
            sound += AudioSegment.from_file(f"output_{i}.mp3", format="mp3")
        sound.export(f"output_combined.mp3", format="mp3")
    
    print("全ての処理が終了しました。")