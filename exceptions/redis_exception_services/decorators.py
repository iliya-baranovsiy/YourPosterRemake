import inspect
from functools import wraps

from events.redis_exeption_event import redis_exception


def cache_exception(*ids: str, default_return=None):
    def decorator(func):
        signature = inspect.signature(func)

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)

            except Exception:
                bound = signature.bind(self, *args, **kwargs)
                bound.apply_defaults()

                for path in ids:
                    value = bound.arguments

                    for attr in path.split("."):
                        if isinstance(value, dict):
                            value = value.get(attr)
                        else:
                            value = getattr(value, attr, None)

                        if value is None:
                            break

                    if value is not None:
                        await self.mongo.write_id(value)

                redis_exception.set()
                return default_return

        return wrapper

    return decorator
