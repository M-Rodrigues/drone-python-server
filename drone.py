cur_state = {}

def start_drone(q):
	while True:
		if not q.empty():
			cur_state = q.get()
			print('NEW', cur_state)
		else:
			print(cur_state)
