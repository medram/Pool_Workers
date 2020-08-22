import time
import threading
import random

from queue import Queue
from pool_workers import Pool

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
p = Pool(name='Pool_1', queue=q, max_workers=2, wait_queue=False, execption_handler=execption_handler)

# adding some tasks the the queue.
for i in range(10):
	# task is a tuple of a function, args and kwargs.
	our_task = (our_process, (i,), {})
	q.put(our_task)

try:
	# start the Pool
	p.start()
	# go back to the main thread from time to another to check the KeyboardInterrupt
	while p.is_alive():
		p.join(0.5)

except (KeyboardInterrupt, SystemExit):
	# shutdown the pool by aborting its Workers/threads.
	p.shutdown()


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