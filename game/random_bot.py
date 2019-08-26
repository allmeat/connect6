import random


def find_empty_spot(coord_info):
	x_candidate = []
	y_candidate = []
	for i in coord_info.x_axis:
		if i == 0:
			x_candidate.append(i)
	for j in coord_info.y_axis:
		if j == 0:
			y_candidate.append(j)
	final_x = random.choice(x_candidate)
	final_y = random.choice(y_candidate)
	return final_x, final_y
