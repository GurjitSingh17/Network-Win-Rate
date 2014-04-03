##python3.3
## Gurjit Singh
## UC Berkeley
## This version runs 8 processes at a time
## You might want to change this number based on the speed of your computer
## chanage line 49 to change the number of processes
##
## place this file in your project 2 folder alongside your Network.class file
## run as python winRate.py or python3 winRate.py
## output is saved to output.py

import subprocess
import time
from multiprocessing import Pool
import os
command = ['java Network -q machine random', 'java Network -q random machine' ]
##command = [['java', 'Network', '-q', 'machine','random'], ['java', 'Network', '-q', 'random','machine'] ]



def run_command(command):
    p = os.popen(command)
    return p.read()
def count(index):
	output = run_command(command[index])
	if(">>>> MachinePlayer <<<< WINS!" in output):
		return 1, output
	elif ("Referee accuses MachinePlayer of cheating." in output):
		print(output)
		return -1,output
	elif ("MachinePlayer returned a null move, quitting." in output):
		print(output)
		return -2,output
	else:
		print(output)
		return 0, output
	

def run(i):
	index = i % 2
	print("Run number: " + str(i))
	wins = count(index)
	return wins

def main():
	number_of_runs = int(input("Enter the number of runs: "))
	results = []
	## change the following line to chnage the number of processes
	process_pool = Pool(processes=8)
	results = process_pool.map(run, range(number_of_runs))
	cheating = 0
	wins = 0
	errors = 0
	output_txt = open('output.txt', 'w')
	for x in range(len(results)):
		if (results[x][0] == -1):
			wins += 0
			errors += 1
			output_txt.write("--------------Machine player returned a null move------------\n")
		if (results[x][0] == -2):
			wins += 0
			cheating += 1
			output_txt.write("--------------accused of cheating------------\n")
		else:
			wins += results[x][0]
		output_txt.write((results[x][1]) + "\n\n\n" )
	output_txt.close()
	return wins,number_of_runs,cheating,errors

if __name__ == '__main__':
	start = time.time()
	wins = main()
	elapsed = time.time() - start
	print("Won " + str(wins[0]) + " games out of "+ str(wins[1]))
	print("Accused of cheating " + str(wins[2]) + " times.")
	print("Returned a null move " + str(wins[3]) + " times.")
	print(str(((wins[0]/wins[1])*100)) + "% win rate")
	print("total elapsed time: " + str("{0:.2f}".format(elapsed)) + " seconds")
	print("time per game: "+ str("{0:.2f}".format(elapsed/wins[1])) + " seconds")
