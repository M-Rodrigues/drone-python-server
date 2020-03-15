import time
import multiprocessing
import random

def drone(q):
	state = 0.0
	while True:
		if not q.empty():
			state = q.get()
			print('State processed at', time.time())
		print('State: {}'.format(state))

def server(q):
	random.seed(0)
	while True:
		n = random.randint(1, 10)
		q.put(n)
		print('State received at', time.time())
		time.sleep(random.random() / 10)

if __name__ == "__main__": 
	# creating  Queue 
	q = multiprocessing.Queue() 

	# creating new processes 
	p1 = multiprocessing.Process(target=server, args=(q,)) 
	p2 = multiprocessing.Process(target=drone, args=(q,)) 

	# running process p1 to square list 
	p1.start() 
	p2.start() 

	# running process p2 to get queue elements 
	p1.join() 
	p2.join() 
