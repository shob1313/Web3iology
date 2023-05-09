from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

model = load_model('model.h5')

def preprocess_image(image):
    # Preprocess the image as required (resize, normalization, etc.)
    processed_image = image.resize((256, 256))
    processed_image = np.array(processed_image) / 255.0
    return processed_image

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    image = request.files['image']
    img = Image.open(image)

    processed_img = preprocess_image(img)
    print(processed_img.shape)  # Verify the shape of the processed image
    processed_img = np.expand_dims(processed_img, axis=0)

    prediction = model.predict(processed_img)
    # Assuming binary classification with 0 as negative class and 1 as positive class
    result = 'Positive' if prediction[0][0] >= 0.5 else 'Negative'
    image_cid = IPFSupload(image)
    print(result +"   "+image_cid)
    response = jsonify({'prediction': result, 'image_cid': image_cid})
    response.headers.add('Access-Control-Allow-Origin', '*')  # Add CORS header
    return response

def IPFSupload(image):
    print("hello its shobith")
    client = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDNGMTNiZTBhODZBOEM4QzBCZmMyMzI3NzVFM0JhMzY1ZGVFNTNGQTQiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODIzMDkxODMzNTYsIm5hbWUiOiJQcm9qZWN0U2Nob29sIn0.eY7wm0K0KhDerqo9NoHrm8bH0Crd4acYTwiw8GoUCnA"
    files = {'file': image}

    headers = {
        "Authorization": f"Bearer {client}"
    }

    try:
        response = requests.post("https://api.web3.storage/upload", headers=headers, files=files)

        if not response.ok:
            raise Exception(f"HTTP error! status: {response.status_code}")

        hashvalue = response.json()
        print(hashvalue)

        return hashvalue['cid']
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == '__main__':
    app.run()
