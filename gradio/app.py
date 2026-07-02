import sys
sys.path.append('../')

import os
import gradio as gr
import requests
import json
import io
import base64
import cv2
import numpy as np

from gradio.components import Image
from PIL import Image, ExifTags
from engine.header import *

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
root_path = os.path.dirname(dir_path)

device_id = get_deviceid().decode('utf-8')
print_info('\t <Hardware ID> \t\t {}'.format(device_id))

g_activation_result = -1

screenReplayThreshold = 0.5
portraitReplaceThreshold = 0.5
printedCopyThreshold = 0.5

css = """
.example-image img{
    display: flex; /* Use flexbox to align items */
    justify-content: center; /* Center the image horizontally */
    align-items: center; /* Center the image vertically */
    height: 300px; /* Set the height of the container */
    object-fit: contain; /* Preserve aspect ratio while fitting the image within the container */
}
.example-image img{
    display: flex; /* Use flexbox to align items */
    justify-content: center; /* Center the image horizontally */
    align-items: center; /* Center the image vertically */
    height: 300px; /* Set the height of the container */
    object-fit: contain; /* Preserve aspect ratio while fitting the image within the container */

.block-background {
    # background-color: #202020; /* Set your desired background color */
    border-radius: 5px;
}
}
"""

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

def check_id_liveness(frame):
    global g_activation_result
    if g_activation_result != 0:
        gr.Warning("SDK Activation Failed!")
        return {"status": "error", "result": "activation error!"}
    try:
        image = Image.open(frame)
        image = apply_exif_rotation(image.convert('RGB'))
    except:
        raise gr.Error("Please select image file!")
    
    image_np = np.asarray(image)
    result = processImage(image_np, image_np.shape[1], image_np.shape[0])
    result_dict = json.loads(result.decode('utf-8'))
    status = result_dict["status"]
    if status == "Ok":
        screenReply = float(result_dict["screenReply"])
        portraitReplace = float(result_dict["portraitReplace"])
        printedCopy = float(result_dict["printedCopy"])
        detResult = "genuine"

        # Check for "Spoof" condition
        if screenReply < screenReplayThreshold or portraitReplace < portraitReplaceThreshold or printedCopy < printedCopyThreshold:
            detResult = "spoof"

        # Update json_result with the modified process_results
        return {"status": "ok", "data": {"result": detResult, "screenreplay_integrity_score": screenReply, "portraitreplace_integrity_score": portraitReplace, "printedcutout_integrity_score": printedCopy}}
            
    return {"status": "error", "result": "document not found!"}


def launch_demo(activate_result):
    with gr.Blocks(css=css) as demo:   
        with gr.Group():
            if activate_result == 0:
                gr.Markdown("""<p style="text-align: left; font-size: 20px; color: green;">&emsp;Activation Success!</p>""")         
            else:
                gr.Markdown("""<p style="text-align: left; font-size: 20px; color: red;">&emsp;Activation Failed!</p>""") 
                    
            gr.Textbox(device_id, label="Hardware ID")
            

        with gr.Row():
            with gr.Column(scale=1):
                image_input= gr.Image(label="Image", type='filepath', elem_classes="example-image")
                gr.Examples([os.path.join(root_path,'examples/1.jpg'), 
                                    os.path.join(root_path,'examples/2.jpg'), 
                                    os.path.join(root_path,'examples/3.jpg')], 
                                    inputs=image_input)

            with gr.Blocks():
                with gr.Column(scale=1, elem_classes="block-background"):     
                    process_button = gr.Button("Check ID Liveness", variant="primary", size="lg")
                    json_output = gr.JSON()
                process_button.click(check_id_liveness, inputs=image_input, outputs=[json_output])

    demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False, share=True)

if __name__ == '__main__':
    g_activation_result = activate_sdk()
    launch_demo(g_activation_result)