# Pool_Workers
Pool_Workers is a small package for dealing with pools, workers and queues.

## Installation:
```bash
pip install pool-workers
```
## More info:
Usefull functions for Pool as well as Worker.

```python
"""
Default params:
Pool(max_workers=os.cpu_count() + 4, name=None, queue=None, wait_queue=True,
	result_queue=None, workers_sleep=0.1, callback=None, execption_handler=execption_handler)
"""
from pool_workers import Pool

pool = Pool(...)

pool.start()		# Start all workers to process queue tasks.
pool.is_alive()		# Return true if is there any alive worker, else false.
pool.is_idle()		# Return true if is there any worker in idle mode, else false.
pool.is_done()		# Return true if the queue is empty (no tasks left to process).
pool.is_paused()	# Return true if the all workers have been paused, else false.
pool.shutdown()		# Abort all workers
pool.join()			# Wait for all workers to finish the all queue tasks.
pool.result()		# return a list result
pool.pause()		# pause the all workers
pool.resume()		# resume the all workers
pool.count()		# count workers
pool.update()		# adjust the number of workers

"""
default params:
Worker(name, queue, result=None, wait_queue=False, sleep=0.5, callback=None,
	execption_handler=execption_handler)
"""
from pool_workers import Worker

worker = Worker(...)

worker.start()
worker.abort()		# stop worker in a safe way
worker.aborted()
worker.pause()
worker.paused()
worker.resume()
# And like a normal thread, worker has also:
worker.is_alive()
worker.join()


```

## Usage
### Example 1:
```python
import time
import threading
import random

from queue import Queue
from pool_workers import Pool, Task

# Our logic to be performed Asynchronously.
def our_process(a):
	t = threading.current_thread()
	# just to semulate how mush time this logic is going to take to be done.
	time.sleep(random.uniform(0, 3))
	print(f'{t.getName()} is finished the task {a} ...')


# Our function to handle thrown exceptions from 'our_process' logic.
def execption_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


# create a queue & pool.
q = Queue()
pool = Pool(name='Pool_1', queue=q, wait_queue=False, execption_handler=execption_handler)

# adding some tasks the the queue.
for i in range(10):
	# Creating task with args and kwargs and push it into the queue.
	task = Task(our_process, args=(i,), kwargs={})
	q.put(task)

try:
	# start the Pool
	pool.start()
	# go back to the main thread from time to another to check the KeyboardInterrupt
	while pool.is_alive():
		pool.join(0.5)

except (KeyboardInterrupt, SystemExit):
	# shutdown the pool by aborting its Workers/threads.
	pool.shutdown()


"""output result
Worker_1_Pool_1 is finished the task 1 ...
Worker_1_Pool_1 is finished the task 2 ...
Worker_0_Pool_1 is finished the task 0 ...
Worker_0_Pool_1 is finished the task 4 ...
Worker_0_Pool_1 is finished the task 5 ...
Worker_1_Pool_1 is finished the task 3 ...
Worker_0_Pool_1 is finished the task 6 ...
Worker_1_Pool_1 is finished the task 7 ...
Worker_0_Pool_1 is finished the task 8 ...
Worker_0_Pool_1: The Queue is empty.
Worker_1_Pool_1 is finished the task 9 ...
Worker_1_Pool_1: The Queue is empty.
Worker_0_Pool_1 is stopped
Worker_1_Pool_1 is stopped
Pool_1 is shutted down
"""
```

### Example 2:
```python
import time
import threading
import random

from queue import Queue
from pool_workers import Worker, Task

# Our logic to be performed Asynchronously.
def our_process(a):
	t = threading.current_thread()
	# just to semulate how mush time this logic is going to take to be done.
	time.sleep(random.uniform(0, 3))
	print(f'{t.getName()} is finished the task {a} ...')


# Our function to handle thrown exceptions from 'our_process' logic.
def execption_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


# create a queue & pool.
q = Queue()
t = Worker(name='worker', queue=q, wait_queue=False, sleep=0.1, execption_handler=execption_handler)

# adding some tasks the the queue.
for i in range(10):
	# Creating task with args and kwargs and push it into the queue.
	task = Task(our_process, args=(i,), kwargs={})
	q.put(task)

try:
	# start the Pool
	t.start()
	# block the code execution here to check the KeyboardInterrupt (to stop the worker safely)
	while t.is_alive():
		t.join(0.5)

	# Can't go here until the worker finishes his work.

except (KeyboardInterrupt, SystemExit):
	# stop the Worker/thread.
	t.abort()

"""output result
worker is finished the task 0 ...
worker is finished the task 1 ...
worker is finished the task 2 ...
worker is finished the task 3 ...
worker is finished the task 4 ...
worker is finished the task 5 ...
worker is finished the task 6 ...
worker is finished the task 7 ...
worker is finished the task 8 ...
worker is finished the task 9 ...
"""
```

## License
MIT License


