import boto3
import json
import base64
import requests # Add layer


print('Loading function')

# --------------- Helper Functions ------------------
def upload_imag_S3(s3_bucket, s3_key, image_file, image_data):
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=s3_bucket,
        Key=s3_key + image_file,  # アップロード後のオブジェクトキー
        Body=image_data,
        ContentType='image/png'  # 画像のコンテントタイプを適切なものに変更
    )
    return


def detect_label(bucket, image):
    rekognition = boto3.client('rekognition')
    labels = rekognition.detect_labels(
        Image={'S3Object':{'Bucket':bucket,'Name':image}},
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {"LabelInclusionFilters":["Food and Beverage"]}
        }
    )
    return labels


def detect_label_binary(image_binary):
    rekognition = boto3.client('rekognition')
    labels = rekognition.detect_labels(
        Image={'Bytes':image_binary},
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {"LabelInclusionFilters":["Food and Beverage"]}
        }
    )
    return labels


def get_resipes(keyword, cuisineType=None, mealType=None, dishType=None):
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
        "app_id": "57fe55de",
        "app_key": "6e8e01d0eb4e2633ee5f223561c9c325",
        "q": keyword,
        "cuisineType": cuisineType,
        "mealType": mealType,
        "dishType": dishType,
    }

    try:
        # 外部のWeb APIを呼び出し
        response = requests.get(api_url, headers=headers, params=params)

        # レスポンスコードの確認
        if response.status_code == 200:
            # Web APIからのレスポンスを取得
            api_response = response.json()
            return api_response
        else:
            return {
                "statusCode": response.status_code,
                "body": None
            }
    except Exception as e:
        raise e


def translate_text(text_list, source_language="en", target_language="ja"):
    text = ' _ '.join(text_list)
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    translated_list = response['TranslatedText']
    return translated_list.split(' _ ')


# --------------- Main handler ------------------
def lambda_handler(event, context):
    '''
    '''
    print(event)

    try:
        # API Gatewayからのリクエストボディを取得
        request_body = json.loads(event['body'])
        image_body = request_body.get('image')
        image_bin = base64.b64decode(image_body)
        cuisine_type = request_body.get('cuisineType')
        meal_type = request_body.get('mealType')
        dish_type = request_body.get('dishType')

        # 画像をS3にアップロードする
        # image_file = request_body.get('image_file')
        # s3_bucket = "menu-suggestion-group1"
        # s3_key = "images/"
        # upload_imag_S3(s3_bucket, s3_key, image_file, image_data)
        
        # 画像から食材を検出する
        labels = detect_label(image_bin)
        
        # レシピAPIからレスポンスを取得する
        respons = get_resipes(labels, cuisine_type, meal_type, dish_type)
        
        recipes = respons["hits"]
        for i, recipe in enumerate(recipes):
            ingredientLines = recipe["ingredientLines"]
            # レシピを日本語に翻訳する
            ingredientLines_ja = translate_text(ingredientLines)
            respons["hits"][i]["recipe"]["ingredientLines"] = ingredientLines_ja
        
        return {
            'statusCode': 200,
            'body': json.dumps(respons)
        }       
    except Exception as e:
        raise e

# if __name__ == '__main__':
#     resp = get_resipes("chikin")
#     print(resp)

