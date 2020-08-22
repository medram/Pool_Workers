import time
import threading
import random

from queue import Queue
from pool_workers import Worker

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
	# task is a tuple of a function, args and kwargs.
	our_task = (our_process, (i,), {})
	q.put(our_task)

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