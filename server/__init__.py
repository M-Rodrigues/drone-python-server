import time
import random

def start_server(q):
	random.seed(0)
	while True:
		n = random.randint(1, 10)
		q.put(n)
		print('State received at', time.time())
		time.sleep(random.random() / 10)
