from locust import HttpUser, task
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

class FaceMatchStress(HttpUser):
    @task
    def face_match_verify(self):
        response = self.client.post('/infer', json=inference_request.dict())
