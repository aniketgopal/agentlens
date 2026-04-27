from __future__ import annotations

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from inspect import iscoroutinefunction

from agentlens.context import current_client, current_run, default_client


def _as_payload(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return result
    return {"result": result}


def trace_agent(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        if _is_async(fn):
            @wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                client = current_client.get() or default_client.get()
                if client is None:
                    return await fn(*args, **kwargs)
                with client.run(name=name, input={"args": repr(args), "kwargs": kwargs}) as agent_run:
                    result = await fn(*args, **kwargs)
                    agent_run.set_output(_as_payload(result))
                    return result

            return async_wrapper

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            client = current_client.get() or default_client.get()
            if client is None:
                return fn(*args, **kwargs)
            with client.run(name=name, input={"args": repr(args), "kwargs": kwargs}) as agent_run:
                result = fn(*args, **kwargs)
                agent_run.set_output(_as_payload(result))
                return result

        return wrapper

    return decorator


def trace_step(type: str, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        if _is_async(fn):
            @wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                run = current_run.get()
                if run is None:
                    return await fn(*args, **kwargs)
                with run.step(type=type, name=name, input={"args": repr(args), "kwargs": kwargs}) as step:
                    result = await fn(*args, **kwargs)
                    step.set_output(_as_payload(result))
                    return result

            return async_wrapper

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            run = current_run.get()
            if run is None:
                return fn(*args, **kwargs)
            with run.step(type=type, name=name, input={"args": repr(args), "kwargs": kwargs}) as step:
                result = fn(*args, **kwargs)
                step.set_output(_as_payload(result))
                return result

        return wrapper

    return decorator


def _is_async(fn: Callable[..., Any]) -> bool:
    return iscoroutinefunction(fn)
