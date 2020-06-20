
def start_drone(q):
	cur_state = {}
	while True:
		if not q.empty():
			cur_state = q.get()
			print('NEW', cur_state)
		else:
			print(cur_state)
