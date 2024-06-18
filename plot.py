import matplotlib.pyplot as plt
import numpy as np

time = [0.5, 0.7, 0.8, 1, 1.2, 1.5]
left_distance = [7.5, 21.2, 28, 33.5, 34.5, 48]
left_angle = [5, 11, 13, 16, 19, 30]
right_distance = [6.5, 22.4, 27, 32.5, 39, 42.5]
right_angle = [5, 10, 15, 18, 28, 30]
forward_distance = [8.5, 28.5, 30.7, 35, 50.5, 53] 
forward_angle = [0, 0, -1, 0, -2, 2]



def angle_dist_to_xy(theta, L):
    x= L * np.cos(np.deg2rad(theta))
    y = L * np.sin(np.deg2rad(theta))
    return x, y

def xy_to_angle(x, y):
    try: 
        return np.rad2deg(np.arctan(y / x))
    except:
        return 0

def calc_route_back(start_x, start_y, start_robot_angle):
    
    time_list = []
    direction_list = []

    angle_to_goal = xy_to_angle(start_x, start_y)
    print(angle_to_goal)
    x = start_x
    y = start_y
    if start_robot_angle >= angle_to_goal:
        direction = 'L'
        dist_arr = left_distance
        angle_arr = left_angle
    else: 
        direction = 'R'
        dist_arr = right_distance
        angle_arr = right_angle
    while np.abs(angle_to_goal) >= 5:
        for idx, angle in reversed(list(enumerate(angle_arr))):
            if angle <= angle_to_goal:
                time_list.append(time[idx])
                direction_list.append(direction)
                angle_to_goal -= angle
                dist = dist_arr[idx]
                x_, y_ = angle_dist_to_xy(angle, dist)
                x += x_
                y += y_

                break
            
    to_travel_dist = np.sqrt((x**2) + (y**2))
    while to_travel_dist >= 8.5:
        for idx, dist in reversed(list(enumerate(forward_distance))):
            if dist <= to_travel_dist:
                time_list.append(time[idx])
                direction_list.append('F')
                to_travel_dist -= dist
                break
    return time_list, direction_list

if __name__ == "__main__": 
    start_x = -20
    start_y = 200
    start_robot_angle = -30

    time_list, direction_list = calc_route_back(start_x, start_y, start_robot_angle)
    print(time_list)
    print(direction_list)

    x_list = [start_x]
    y_list = [start_y]
    x = start_x
    y = start_y

    for idx, t in enumerate(time_list):
        if direction_list[idx] == 'R':
            dist_arr = right_distance
            angle_arr = right_angle
        elif direction_list[idx] == 'L':
            dist_arr = left_distance
            angle_arr = left_angle
        elif direction_list[idx] == 'F':
            dist_arr = forward_distance
            angle_arr = forward_angle
        
        curr_idx = time.index(t)
        dist = dist_arr[curr_idx]
        angle = angle_arr[curr_idx]


        x_, y_ = angle_dist_to_xy(angle, dist)
        x += x_
        y += y_
        x_list.append(x)
        y_list.append(y)
    
    fig, ax = plt.subplots()
    ax.plot(x_list, y_list)
    # ax.set_aspect('equal')
    ax.axhline(y=0, color='black')
    ax.axvline(x=0, color='black')
    plt.show()