import json
import requests
import collections
import sys
import time
from pandas import DataFrame
from enum import Enum

"""Get Game Data From Server"""

url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
uid = {'uid' : 704931660}

session = requests.post(url + '/session', data = uid)
session_data = session.json()
TOKEN = session_data['token']
"""print(TOKEN)"""

"""Depth First Search"""

def df_search(curr_position):
	for action in ['UP', 'LEFT', 'DOWN', 'RIGHT']:

		x_pos = curr_position[0]
		y_pos = curr_position[1]

		if(action == 'UP'):
			if(y_pos - 1 < 0):
				continue
			probe_loc = maze[y_pos-1][x_pos]
			new_position = [x_pos, y_pos-1]

		elif(action == 'DOWN'):
			if(y_pos + 1 >= y_dim):
				continue 
			probe_loc = maze[y_pos+1][x_pos]
			new_position = [x_pos, y_pos+1]

		elif(action == 'LEFT'):
			if(x_pos - 1 < 0):
				continue
			probe_loc = maze[y_pos][x_pos-1]
			new_position = [x_pos-1, y_pos]

		elif(action == 'RIGHT'):
			if(x_pos + 1 >= x_dim):
				continue
			probe_loc = maze[y_pos][x_pos+1]
			new_position = [x_pos+1, y_pos]

		if(probe_loc != '?'):
			continue
		"""print(curr_position)"""
		move = {'action' : action}
		response = requests.post(url + '/game?token=' + TOKEN, data=move)
		time.sleep(0.010)
		data = response.json()
		result = data['result']

		if(result == 'SUCCESS'):
			"""print("MOVE " + action)"""
			"""print(new_position)"""
			maze[new_position[1]][new_position[0]] = ' '
			if(df_search(new_position)):
				return True

			else:
				if(action == 'UP'):
					move = {'action' : 'DOWN'}
					"""print("BACKTRACK DOWN")"""

				elif(action == 'DOWN'):
					move = {'action' : 'UP'}
					"""print("BACKTRACK UP")"""

				elif(action == 'LEFT'):
					move = {'action' : 'RIGHT'}
					"""print("BACKTRACK RIGHT")"""

				elif(action == 'RIGHT'):
					move = {'action' : 'LEFT'}
					"""print("BACKTRACK LEFT")"""

			response = requests.post(url + '/game?token=' + TOKEN, data=move)
			time.sleep(0.010)

		elif(result == 'WALL'):
			maze[new_position[1]][new_position[0]] = 'W'
			"""print("WALL " + action)"""
			

		elif(result == 'END'):
			maze[new_position[1]][new_position[0]] = 'E'
			print(DataFrame(maze))
			return True

	return False

"""Game"""

while(True):

	x_dim = None
	y_dim = None
	x_start = None
	y_start = None

	game = requests.get(url + '/game?token=' + TOKEN)
	game_data = game.json()

	status = game_data['status']

	if(status == 'FINISHED'):
		break

	dimension = game_data['maze_size']
	position = game_data['current_location']

	(x_dim, y_dim) = dimension
	(x_start, y_start) = position

	print(status)
	print(position)
	print(dimension)

	maze = [['?' for _ in range(x_dim) ] for _ in range(y_dim)]
	maze[y_start][x_start] = 'S'

	if(df_search(position)):
		print('Level %d Complete!' % (game_data['levels_completed']))

