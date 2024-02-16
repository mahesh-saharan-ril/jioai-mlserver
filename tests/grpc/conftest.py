import os
import pytest

from grpc import aio
from typing import AsyncGenerator, Dict
from google.protobuf import json_format
from prometheus_client.registry import CollectorRegistry

from jioai_mlserver.parallel import InferencePool
from jioai_mlserver.batching import load_batching
from jioai_mlserver.handlers import DataPlane, ModelRepositoryHandlers
from jioai_mlserver.settings import Settings, ModelSettings
from jioai_mlserver.registry import MultiModelRegistry
from jioai_mlserver.grpc import dataplane_pb2 as pb
from jioai_mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from jioai_mlserver.grpc import GRPCServer

from ..conftest import TESTDATA_PATH
from ..fixtures import SumModel
from ..metrics.conftest import prometheus_registry  # noqa: F401

TESTDATA_GRPC_PATH = os.path.join(TESTDATA_PATH, "grpc")


def _read_testdata_pb(payload_path: str, pb_klass):
    model_infer_request = pb_klass()
    with open(payload_path) as payload:
        json_format.Parse(payload.read(), model_infer_request)

    return model_infer_request


@pytest.fixture
async def model_registry(
    sum_model_settings: ModelSettings, inference_pool: InferencePool
) -> MultiModelRegistry:
    model_registry = MultiModelRegistry(
        on_model_load=[inference_pool.load_model, load_batching],
        on_model_reload=[inference_pool.reload_model],
        on_model_unload=[inference_pool.unload_model],
    )

    model_name = sum_model_settings.name
    await model_registry.load(sum_model_settings)

    yield model_registry

    try:
        # It could be that the model is not present anymore
        await model_registry.unload(model_name)
    except Exception:
        pass


@pytest.fixture
def model_infer_request() -> pb.ModelInferRequest:
    payload_path = os.path.join(TESTDATA_GRPC_PATH, "model-infer-request.json")
    return _read_testdata_pb(payload_path, pb.ModelInferRequest)


@pytest.fixture
def grpc_parameters() -> Dict[str, pb.InferParameter]:
    return {
        "content_type": pb.InferParameter(string_param="np"),
        "foo": pb.InferParameter(bool_param=True),
        "bar": pb.InferParameter(int64_param=46),
    }


@pytest.fixture
def grpc_repository_index_request() -> pb.RepositoryIndexRequest:
    return pb.RepositoryIndexRequest(ready=None)


@pytest.fixture
async def inference_service_stub(
    grpc_server, settings: Settings
) -> AsyncGenerator[GRPCInferenceServiceStub, None]:
    async with aio.insecure_channel(f"{settings.host}:{settings.grpc_port}") as channel:
        yield GRPCInferenceServiceStub(channel)


@pytest.fixture
async def grpc_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    sum_model: SumModel,
    prometheus_registry: CollectorRegistry,  # noqa: F811
):
    server = GRPCServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    server._create_server()

    await server._server.start()

    yield server

    await server._server.stop(grace=None)
