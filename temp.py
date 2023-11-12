import base64

def encode_image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            # 画像ファイルをbase64エンコード
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_image
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# 画像ファイルのパスを指定
image_path = 'tomato.jpg'

# 画像をbase64エンコード
base64_encoded_image = encode_image_to_base64(image_path)

# エンコードされた画像データを表示
if base64_encoded_image:
    print("Base64 Encoded Image:")
    print(base64_encoded_image)
