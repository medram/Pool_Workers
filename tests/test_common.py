import os
import time
from queue import Queue
from typing import Dict, List, Union

import pytest

from pool_workers import MAX_WORKERS, Pool, Task, Worker


def work_function(x: int, y: int = 0) -> int:
    time.sleep(0.2)
    return x * y


@pytest.fixture
def task():
    return Task(work_function, args=(5,), kwargs={"y": 3})


@pytest.fixture
def worker():
    return Worker("worker", Queue())


@pytest.fixture
def pool():
    queue = Queue()
    # Add some tasks
    for i in range(50):
        queue.put(Task(work_function, args=(5 * i,), kwargs={"y": 3 * i}))

    def callable_function(result: int) -> None:
        assert result  # Value exists

    def log_exception(name: str, e: Exception) -> None:
        # Log data for example
        assert name != ""
        assert str(e) != ""

    return Pool(
        name="Pool",
        queue=queue,
        callback=callable_function,
        execption_handler=log_exception,
    )


def test_task_creation(task: Task):
    assert callable(task.callable)
    assert task.args == [5]
    assert task.kwargs == {"y": 3}


def test_task_run(task: Task):
    assert task.run() == task.args[0] * task.kwargs.get("y")


def test_task_run_as_function(task: Task):
    assert task() == task.args[0] * task.kwargs.get("y")


def test_worker_delete(worker: Worker):
    del worker


def test_pool_creation():
    pool = Pool(name="Pool")

    assert pool.is_idle() == True
    assert pool.is_done() == True
    assert pool.is_alive() == False
    assert pool.is_paused() == True
    assert pool.count() == 0


def test_pool_exception():
    # Clear the queue
    queue = Queue()
    error_massage = "Custom Error :D"

    def work_function():
        raise Exception(error_massage)

    def log_exception(name: str, e: Exception) -> None:
        assert str(e) == error_massage

    queue.put(Task(work_function), block=False)
    pool = Pool(name="Pool", queue=queue, execption_handler=log_exception)
    pool.start()
    pool.shutdown()


def test_pool_shutdown(pool: Pool):
    pool.shutdown()
    time.sleep(1)
    assert pool.queue.qsize() > 0
    assert pool.count() == 0
    assert pool.is_paused() == True


def test_pool_results():
    def custom_work_function(id, x=0, y=0):
        return {"id": id, "result": x * y}

    queue = Queue()
    tasks: List[Task] = []
    # Add some tasks
    for i in range(50):
        task = Task(
            custom_work_function,
            args=(os.urandom(10).hex(),),
            kwargs={"x": 5 * i, "y": 3 * i},
        )
        queue.put(task)
        tasks.append(task)

    pool = Pool(name="Pool", queue=queue)
    pool.start()
    results: List[Dict[str, Union[str, int]]] = pool.result(block=True)
    pool.shutdown()

    for task in tasks:
        task_id: str = task.args[0]
        result: int = 0
        for r in results:
            if r.get("id") == task_id:
                result = int(r.get("result", 0))

        assert result == task.run().get("result")


def test_pool_update(pool: Pool):
    pool.start()
    # Let's the empty the queue (Process all tasks)
    pool.join()
    # Let's updates the number of workers
    pool.update(10)
    assert pool.count() == 10
    pool.update(12)
    assert pool.count() == 12
    pool.update(5, block=True)
    assert pool.count() == 5
    pool.shutdown()


def test_pool_functionality(pool: Pool):
    # Starting the workers (processing tasks)
    pool.start()

    assert pool.count() == MAX_WORKERS
    assert pool.is_idle() == False
    assert pool.is_done() == False
    assert pool.is_alive() == True
    assert pool.is_paused() == False
    assert pool.queue.qsize() > 0

    pool.pause()
    assert pool.is_paused() == True
    time.sleep(1)
    assert pool.count() == MAX_WORKERS
    assert pool.is_idle() == True
    assert pool.is_done() == False
    assert pool.is_alive() == True
    assert pool.queue.qsize() > 0

    pool.resume()
    assert pool.count() == MAX_WORKERS
    assert pool.is_done() == False
    assert pool.is_paused() == False
    assert pool.is_idle() == False
    assert pool.is_alive() == True

    pool.join()
    assert pool.count() == MAX_WORKERS
    assert pool.is_done() == True
    # assert pool.is_idle() == True
    assert pool.is_alive() == True
    assert pool.queue.qsize() == 0

    pool.shutdown(block=True)
    assert pool.is_paused() == True
