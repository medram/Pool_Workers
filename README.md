# Pool_Workers
Pool_Workers is a small package for dealing with pools, workers and queues.

## Installation:
```bash
pip install pool_workers
```

## How to Use?
Please see some examples at 'examples' folder.

## More info:
Describe some useful functions at pool & worker objects

```python
"""
Default params:
Pool(max_workers=os.cpu_count() + 4, name=None, queue=None, wait_queue=True,
        result_queue=None, workers_sleep=0.5, callback=None, execption_handler=execption_handler)
"""
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

## License
MIT License


