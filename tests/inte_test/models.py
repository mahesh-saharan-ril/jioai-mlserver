from jioai_mlserver import MLModel
from jioai_mlserver.types import InferenceRequest, InferenceResponse
from jioai_mlserver.codecs import NumpyCodec
from jioai_deepface import JioFace

class FaceDetectModel(MLModel):
    async def load(self) -> bool:
        self._predictive = JioFace.JioFaceDetector('retinaface')
        self.ready = True
        return self.ready

    async def predict(self, imglist: InferenceRequest) -> InferenceResponse:
        imgs = self.decode(imglist.inputs[0])
        predictions = self._predictive.detect_faces(imgs)
        resps = []
        resps.append(NumpyCodec.encode_output(name=imglist.inputs[0].name, payload=predictions))
        return InferenceResponse(model_name=self.name, outputs=resps)

class FaceRepresentModel(MLModel):
    async def load(self) -> bool:
        self._predictive = JioFace.JioFaceRepresentation('Facenet')
        self.ready = True
        return self.ready

    async def predict(self, faces: InferenceRequest) -> InferenceResponse:
        imgs = self.decode(faces.inputs[0])
        print(imgs.shape)
        predictions = self._predictive.get_representation(imgs)
        resps = []
        resps.append(NumpyCodec.encode_output(name=faces.inputs[0].name, payload=predictions))
        return InferenceResponse(model_name=self.name, outputs=resps)