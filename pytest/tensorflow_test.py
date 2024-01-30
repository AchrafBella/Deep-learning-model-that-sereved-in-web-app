import sys
import os

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the directory of the current script
current_script_directory = os.path.dirname(current_script_path)

# Get the project root by going up one level
project_root = os.path.dirname(current_script_directory)

# Add the project root to the Python path
sys.path.append(project_root)

from APP.apply_model import *
from pathlib import Path


def test_model_prediction():

    image_path = 'C://Users/Eye patch/Desktop/project DL deployement/pytest/0001.jpg'
    dimensions = (128, 128)
    model_version = 1

    img_res = preprocess_image(image_path, dimensions)
    img = img_res.get('img')

    tensorflow_server_input = { 
        "signature_name": "serving_default", 
        "instances": img.tolist()}
    
    predictions_results = tensorflow_serving_models(link='localhost:8501',version=model_version, tensorflow_server_input=tensorflow_server_input)

    assert len(predictions_results) != 1


