import sys
sys.path.append('../')

import os
import numpy as np
import base64
import json
import io

from PIL import Image, ExifTags
from flask import Flask, request, jsonify

from engine.header import *

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
root_path = os.path.dirname(dir_path)

app = Flask(__name__) 

device_id = get_deviceid().decode('utf-8')
print_info('\t <Hardware ID> \t\t {}'.format(device_id))

def activate_sdk():
    online_key = os.environ.get("LICENSE_KEY")
    offline_key_path = os.path.join(root_path, "license.txt")

    model_path = os.path.join(root_path, "engine/model")

    ret = -1
    if online_key is None:
        print_warning("Online license key not found!")
    else:
        print_info(f"LICENSE_KEY: {online_key}")
        ret = set_activation(online_key.encode('utf-8'))

    if ret == 0:
        print_log("Successfully online activation SDK!")
    else:
        print_error(f"Failed to online activation SDK, Error code {ret}\n Trying offline activation SDK...");
        if os.path.exists(offline_key_path) is False:
            print_warning("Offline license key file not found!")
            print_error(f"Falied to offline activation SDK, Error code {ret}")
            return ret
        else:
            file=open(offline_key_path,"r")
            offline_key = file.read().strip()
            file.close()
            ret = set_activation(offline_key.encode('utf-8'))
            if ret == 0:
                print_log("Successfully offline activation SDK!")
            else:
                print_error(f"Falied to offline activation SDK, Error code {ret}")
                return ret
    
    init_ret = init_sdk(model_path.encode('utf-8'))
    print_log(f"Init SDK: {ret}")
    return ret

def apply_exif_rotation(image):
    try:
        exif = image._getexif()
        if exif is not None:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            # Get the orientation value
            orientation = exif.get(orientation, None)

            # Apply the appropriate rotation based on the orientation
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)

    except AttributeError:
        print("No EXIF data found")

    return image


@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']

    try:
        image = apply_exif_rotation(Image.open(file)).convert('RGB')        
    except:
        result = "Failed to open file"
        response = jsonify({"resultCode": "Error", "result": result})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    image_np = np.asarray(image)
    result = processImage(image_np, image_np.shape[1], image_np.shape[0])

    if result is None:
        result = "Failed to process image"
        response = jsonify({"resultCode": "Error", "result": result})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    else:
        result_dict = json.loads(result.decode('utf-8'))
        response = jsonify({"resultCode": "Ok", "result": result_dict})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@app.route('/process_image_base64', methods=['POST'])
def process_image_base64():
    try:
        content = request.get_json()
        base64_image = content['base64']

        image_data = base64.b64decode(base64_image)
        image = apply_exif_rotation(Image.open(io.BytesIO(image_data))).convert("RGB")
    except:
        result = "Failed to parse base64"
        response = jsonify({"resultCode": "Error", "result": result})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    image_np = np.asarray(image)
    result = processImage(image_np, image_np.shape[1], image_np.shape[0])

    if result is None:
        result = "Failed to process image"
        response = jsonify({"resultCode": "Error", "result": result})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    else:
        result_dict = json.loads(result.decode('utf-8'))
        response = jsonify({"resultCode": "Ok", "result": result_dict})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

if __name__ == '__main__':
    ret = activate_sdk()
    if ret != 0:
        exit(-1)

    port = int(os.environ.get("PORT", 9000))
    app.run(host='0.0.0.0', port=port)