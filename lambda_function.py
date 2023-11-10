import boto3
import json
import urllib.request
import urllib.parse
import urllib.error
from decimal import Decimal

# Add layer
import requests

print('Loading function')

# --------------- Helper Functions ------------------

def detect_label(bucket, photo):
    rekognition = boto3.client('rekognition')
    labels = rekognition.detect_labels(
        Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {"LabelInclusionFilters":["Food and Beverage"]}
        }
        # "ImageProperties": {"MaxDominantColors":10}}
        )
    return labels

def get_resipes(keyword):
    # Web APIのURL
    api_url = "https://api.edamam.com/api/recipes/v2"

    # リクエストヘッダー
    headers = {
        "Content-Type": "application/json",
        "Accept-Language": "en"
    }

    # クエリパラメータ
    params = {
        "type": "public",
        "q": keyword,
        "app_id": "57fe55de",
        "app_key": "6e8e01d0eb4e2633ee5f223561c9c325",
        }

    try:
        # 外部のWeb APIを呼び出し
        response = requests.get(api_url, headers=headers, params=params)

        # レスポンスコードの確認
        if response.status_code == 200:
            # Web APIからのレスポンスを取得
            api_response = response.json()
            return {
                "statusCode": 200,
                "body": json.dumps(api_response)
            }
        else:
            return {
                "statusCode": response.status_code,
                "body": None
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }


def translate_text(original_text):
  translate = boto3.client('translate')  
  translation_text = translate.translate_text(
    Text=original_text,
    SourceLanguageCode='en',
    TargetLanguageCode='ja'
  )
  
  return translation_text['TranslatedText']

# --------------- Main handler ------------------

def lambda_handler(event, context):
    '''
    '''

    try:
        pass        
    except Exception as e:
        raise e

if __name__ == '__main__':
    resp = get_resipes("chikin")
    # 必要な要素
    # resp["hits"][*]["recipe"]["label"]["images"]["url"]["ingredientLines"]
    print(resp)