from typing import Awaitable, Callable, Union

from dishka.integrations.taskiq import setup_dishka
from fastapi import FastAPI, Request
from starlette.requests import HTTPConnection
from taskiq import AsyncBroker, TaskiqEvents, TaskiqState
from taskiq.cli.utils import import_object

from app.logic.container import container


def startup_event_generator(
        broker: AsyncBroker,
        app_or_path: Union[str, FastAPI],
) -> Callable[[TaskiqState], Awaitable[None]]:
    """
    Generate shutdown event.

    This function takes FastAPI application path
    and runs startup event on broker's startup.

    :param broker: current broker.
    :param app_or_path: fastapi application path.
    :returns: startup handler.
    """

    async def startup(state: TaskiqState) -> None:
        if not broker.is_worker_process:
            return
        if isinstance(app_or_path, str):
            app = import_object(app_or_path)
        else:
            app = app_or_path

        if not isinstance(app, FastAPI):
            app = app()  # type: ignore

        if not isinstance(app, FastAPI):
            raise ValueError(f"'{app_or_path}' is not a FastAPI application.")

        state.fastapi_app = app
        await app.router.startup()  # type: ignore
        state.lf_ctx = app.router.lifespan_context(app)  # type: ignore
        await state.lf_ctx.__aenter__()
        populate_dependency_context(broker, app)

    return startup


def shutdown_event_generator(
        broker: AsyncBroker,
) -> Callable[[TaskiqState], Awaitable[None]]:
    """
    Generate shutdown event.

    This function takes FastAPI application
    and runs shutdown event on broker's shutdown.

    :param broker: current broker.
    :return: shutdown event handler.
    """

    async def shutdown(state: TaskiqState) -> None:
        if not broker.is_worker_process:
            return
        await state.fastapi_app.router.shutdown()
        await state.lf_ctx.__aexit__(None, None, None)

    return shutdown


def populate_dependency_context(broker: AsyncBroker, app: FastAPI) -> None:
    """
    Populate dependency context.

    This function injects the Request and HTTPConnection
    into the broker's dependency context.

    It may be need to be called manually if you are using InMemoryBroker.

    :param broker: current broker to use.
    :param app: current application.
    """
    broker.dependency_overrides.update(
        {
            Request: lambda: Request(scope={"app": app, "type": "http"}),
            HTTPConnection: lambda: HTTPConnection(scope={"app": app, "type": "http"}),
        },
    )


def configure_broker(broker: AsyncBroker) -> AsyncBroker:
    app = "app.main:create_app"

    broker.add_event_handler(
        TaskiqEvents.WORKER_STARTUP,
        startup_event_generator(broker, app),
    )

    broker.add_event_handler(
        TaskiqEvents.WORKER_SHUTDOWN,
        shutdown_event_generator(broker),
    )

    setup_dishka(container=container, broker=broker)

    return broker