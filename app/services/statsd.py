import os
import inspect
from statsd import StatsClient
from functools import wraps

ENV_STATSD_PREFIX = os.environ.get("STATSD_PREFIX")
ENV_STATSD_ENDPOINT_URL = os.environ.get("STATSD_ENDPOINT_URL")

statsd = StatsClient(host=ENV_STATSD_ENDPOINT_URL, prefix=ENV_STATSD_PREFIX)

def statsd_root_stats(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        funcname = f.__name__
        tm = statsd.timer(f"{funcname}.root.time")
        tm.start()
        called = f(*args, **kwds)
        tm.stop()
        statsd.incr(f"{funcname}.root.count")
        return called
    return wrapper


def statsd_counter(name):
    # TODO: Should check name for .
    calling_funcname = inspect.stack()[1].function
    statsd.incr(f"{calling_funcname}.{name}.count")