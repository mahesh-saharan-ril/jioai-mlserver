import asyncio
import pytest

from multiprocessing import Queue

from jioai_mlserver.settings import ModelSettings
from jioai_mlserver.types import InferenceRequest
from jioai_mlserver.utils import generate_uuid
from jioai_mlserver.model import MLModel
from jioai_mlserver.parallel.model import ModelMethods
from jioai_mlserver.parallel.pool import InferencePool
from jioai_mlserver.parallel.worker import Worker
from jioai_mlserver.parallel.utils import cancel_task
from jioai_mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelUpdateType,
    ModelRequestMessage,
)


@pytest.fixture
async def sum_model(inference_pool: InferencePool, sum_model: MLModel) -> MLModel:
    parallel_model = await inference_pool.load_model(sum_model)

    yield parallel_model

    await inference_pool.unload_model(sum_model)


@pytest.fixture
async def error_model(inference_pool: InferencePool, error_model: MLModel) -> MLModel:
    model = await inference_pool.load_model(error_model)

    yield model

    await inference_pool.unload_model(error_model)


@pytest.fixture
async def responses() -> Queue:
    q = Queue()
    yield q

    q.close()


@pytest.fixture
async def worker(
    settings,
    event_loop,
    responses: Queue,
    load_message: ModelUpdateMessage,
) -> Worker:
    worker = Worker(settings, responses)

    # Simulate the worker running on a different process, but keep it to a
    # thread to simplify debugging.
    # Note that we call `worker.coro_run` instead of `worker.run` to avoid also
    # triggering the other set up methods of `worker.run`.
    worker_task = event_loop.run_in_executor(
        None, lambda: asyncio.run(worker.coro_run())
    )

    await worker.send_update(load_message)

    yield worker

    await worker.stop()
    await cancel_task(worker_task)


@pytest.fixture
def load_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Load, model_settings=sum_model_settings
    )


@pytest.fixture
def unload_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Unload, model_settings=sum_model_settings
    )


@pytest.fixture
def inference_request_message(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest
) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name=ModelMethods.Predict.value,
        method_args=[inference_request],
    )


@pytest.fixture
def metadata_request_message(sum_model_settings: ModelSettings) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name=ModelMethods.Metadata.value,
    )


@pytest.fixture
def custom_request_message(sum_model_settings: ModelSettings) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        # From `SumModel` class in tests/fixtures.py
        method_name="my_payload",
        method_kwargs={"payload": [1, 2, 3]},
    )
