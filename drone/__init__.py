import time
import random

def start_drone(q):
	state = 0.0
	while True:
		if not q.empty():
			state = q.get()
			print('State processed at', time.time())
		print('State: {}'.format(state))
