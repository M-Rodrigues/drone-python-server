def start_drone(q):
	while True:
		if not q.empty():
			state = q.get()
			print('Orientation state updated', state)
