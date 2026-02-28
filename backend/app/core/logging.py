import time, uuid
from contextlib import contextmanager

@contextmanager
def traced_span(name: str):
    trace_id = str(uuid.uuid4())
    start = time.perf_counter()
    try:
        yield trace_id
    finally:
        end = time.perf_counter()
        _ = (name, trace_id, (end - start))