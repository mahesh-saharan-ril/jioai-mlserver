import requests
from jioai_mlserver.types import InferenceRequest, InferenceResponse
from jioai_mlserver.codecs import NumpyCodec
import numpy as np
import urllib
import cv2
req = urllib.request.urlopen('https://raw.githubusercontent.com/takiyu/portrait_matting/master/sample_images/color_vis_5.jpg')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)
img = np.expand_dims(img, axis=0)

inference_request = InferenceRequest(inputs=[NumpyCodec.encode_input(name="imglist", payload=img)])
endpoint = "http://localhost:8080/v2/models/face-detect/infer"
response = requests.post(endpoint, json=inference_request.dict())
raw_response = response.json()
response = InferenceResponse(**raw_response)
decoded_imgs = []
for output in response.outputs:
    decoded_imgs.append(NumpyCodec.decode_output(output))

decoded_imgs = decoded_imgs[0]

for face in decoded_imgs:
    for f in face:
        cv2.imshow('wow', f)
        cv2.waitKey(0)
        img = f

img = np.expand_dims(img, axis=0)
inference_request = InferenceRequest(inputs=[NumpyCodec.encode_input(name="imglist", payload=img)])
endpoint = "http://localhost:8080/v2/models/face-represent/infer"
response = requests.post(endpoint, json=inference_request.dict())
raw_response = response.json()
response = InferenceResponse(**raw_response)

