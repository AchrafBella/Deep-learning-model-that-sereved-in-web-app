import requests
from PIL import Image
import numpy as np

MODELS_config = {'Model 1': (128, 128), 'Model 2': (31, 31)}
MODELS_version = {'Model 1': 1, 'Model 2': 2}
LABELS = ['Cucumber', 'Pumpkin', 'Carrot', 'Radish', 'Potato', 'Broccoli', 'Papaya',
        'Cabbage', 'Bitter_Gourd', 'Bean', 'Capsicum', 'Cauliflower',  'Tomato', 'Bottle_Gourd', 'Brinjal']

def preprocess_image(image_path, dimensions):
    """
    Preprocesses an image by loading it from the specified path, converting it to grayscale,
    resizing it to the given height and width, normalizing pixel values, and reshaping for model input.

    Parameters:
    - image_path (str): The path to the image file.
    - height (int): The desired height of the preprocessed image.
    - width (int): The desired width of the preprocessed image.

    Returns:
    - numpy.ndarray: A preprocessed image ready to be used as input for a neural network.
    """
    try:
        height, width = dimensions
        img = Image.open(image_path).convert("L")
        img_resized = img.resize(dimensions)
        img_array = np.array(img_resized, dtype=np.float32) / 255.0
        img_dim = img_array.reshape(-1, height, width, 1)
        return {'Error': False, 'img':img_dim}
    except Exception as e:
        return {'Error': True, 'Message': str(e)}

def tensorflow_serving_models(version, tensorflow_server_input, link='tensorflow-serving:8501'):
    """
    Send a POST request to a TensorFlow Serving endpoint for model inference.

    Parameters:
    - version (str): The version of the TensorFlow model.
    - image_data (dict): The input data for model inference in JSON format.

    Returns:
    dict: The prediction obtained from the TensorFlow serving server in JSON format.
    """
    try:
        model_name = 'model' # Use the model name exist in saved_models in tensorflow server
        model_version = MODELS_version[version]
        serving_url = f'http://{link}/v1/models/{model_name}/versions/{model_version}:predict'
        response = requests.post(serving_url, json=tensorflow_server_input)
        prediction = response.json()
        return {'Error': False, 'Prediction': prediction.get('predictions')}
    except Exception as e:
        return {'Error': True, 'Message': str(e)}
    
def predictor(model_version, img_path):
    """
    Predicts the type of vegetable in an image using a specified version of a TensorFlow serving model.

    Parameters:
    - model_version (int): The version of the TensorFlow serving model to use for prediction.
    - img_path (str): The file path of the input image for prediction.

    Returns:
    dict: A dictionary containing the prediction result.
        - If an error occurs, the dictionary will have keys 'Error' (True) and 'Message' (str) with details.
        - If successful, the dictionary will have keys 'Error' (False) and 'vegetables' (str) indicating the predicted vegetable.

    Note:
    - The function relies on external functions preprocess_image and tensorflow_serving_models.
    - The model version should be an integer, and if it's not, an error dictionary is returned.
    - The input image is preprocessed using dimensions specified in MODELS_config.
    - The TensorFlow server input is prepared with the preprocessed image, and predictions are obtained.
    - The predicted vegetable is determined from the obtained predictions using the LABELS array.
    """
    dimensions = MODELS_config.get(model_version, '')
    if dimensions == '':
        return {"Error": True, 'Message': 'The version of the model should be like: Model V'}
    
    img_preprocess = preprocess_image(image_path=img_path, dimensions=dimensions)
    if img_preprocess.get('Error'):
        return {'Error': True, 'Message': img_preprocess.get('Message')}
    else:
        img = img_preprocess.get('img')

    tensorflow_server_input = { 
        "signature_name": "serving_default", 
        "instances": img.tolist()}
    
    predictions_results = tensorflow_serving_models(version=model_version, tensorflow_server_input=tensorflow_server_input)
    
    if predictions_results.get('Error'):
        return {'Error': True, 'Message': predictions_results.get('Message')}
    else:
        array_predictions = predictions_results.get('Prediction')
        vegetables = LABELS[np.argmax(array_predictions[0])]
        return {'Error': False, 'vegetables': vegetables}
    