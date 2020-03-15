import time
import multiprocessing
import random

from drone import start_drone
from server import start_server

if __name__ == "__main__": 
	q = multiprocessing.Queue() 

	p1 = multiprocessing.Process(target=start_server, args=(q,)) 
	p2 = multiprocessing.Process(target=start_drone, args=(q,)) 

	p1.start() 
	p2.start() 

	p1.join() 
	p2.join() 
