#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 13:35
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : TS.py
# @Statement : Tabu Search for the traveling salesman problem (TSP)
# @Reference : Glover, Fred. Tabu Search-- Part I.[J]. ORSA Journal on Computing, 1989.
import math
import random
import matplotlib.pyplot as plt


def cal_dis(dis, path):
    # calculate the length of the path
    length = 0
    for i in range(len(path) - 1):
        length += dis[path[i]][path[i + 1]]
    length += dis[path[-1]][path[0]]
    return length


def swap(sol, i, j):
    """
    The swap action
    """
    new_sol = sol.copy()
    new_sol[i] = sol[j]
    new_sol[j] = sol[i]
    return new_sol


def reversion(sol, i, j):
    """
    The reversion action
    """
    new_sol = sol.copy()
    ind1 = min(i, j)
    ind2 = max(i, j)
    for i in range(ind1, ind2):
        new_sol[i] = sol[ind1 + ind2 - i]
    new_sol[ind2] = sol[ind1]
    return new_sol


def insertion(sol, i, j):
    """
    The insertion action
    """
    new_sol = []
    if i < j:
        new_sol.extend(sol[: i])
        new_sol.extend(sol[i + 1: j])
        new_sol.append(sol[i])
        new_sol.extend(sol[j:])
    else:
        new_sol.extend(sol[: j])
        new_sol.append(sol[i])
        new_sol.extend(sol[j: i])
        new_sol.extend(sol[i + 1:])
    return new_sol


def act(sol, action):
    """
    Do the action
    """
    if action[0] == 1:  # swap
        new_sol = swap(sol, action[1], action[2])
    elif action[0] == 2:  # reversion
        new_sol = reversion(sol, action[1], action[2])
    else:  # insertion
        new_sol = insertion(sol, action[1], action[2])
    return new_sol


def main(x, y, iter):
    """
    The main function for the TS
    :param x: the x coordinates of cities
    :param y: the y coordinates of cities
    :param iter: the maximum number of iterations
    :return:
    """
    # Step 1. Initialization
    city_num = len(x)  # the number of cities
    dis = [[0 for _ in range(city_num)] for _ in range(city_num)]  # distance matrix
    for i in range(city_num - 1):
        for j in range(i + 1, city_num):
            temp_dis = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
            dis[i][j] = temp_dis
            dis[j][i] = temp_dis
    city_list = [i for i in range(city_num)]
    random.shuffle(city_list)
    iter_best = []  # the best-so-far length of each iteration
    con_iter = 0
    sol = city_list
    gbest_path = city_list.copy()  # the best-so-far path
    gbest = cal_dis(dis, gbest_path)  # the best-so-far length
    action_list = []
    for i in range(city_num - 1):  # swap
        for j in range(i + 1, city_num):
            action_list.append([1, i, j])
    for i in range(city_num - 1):  # reversion
        for j in range(i + 1, city_num):
            if j - i > 2:
                action_list.append([2, i, j])
    for i in range(city_num):  # insertion
        for j in range(city_num):
            if abs(i - j) > 1:
                action_list.append([3, i, j])
    na = len(action_list)  # the number of actions
    TC = [0 for _ in range(na)]  # tabu counter
    TL = round(0.5 * na)  # tabu length

    # Step 2. The main loop
    for t in range(iter):

        new_best_sol = []
        new_best_length = 1e6
        new_best_ind = 0
        # Step 2.1. Apply actions
        for i in range(na):
            if TC[i] == 0:
                new_sol = act(sol, action_list[i])
                new_length = cal_dis(dis, new_sol)
                if new_length <= new_best_length:
                    new_best_length = new_length
                    new_best_sol = new_sol
                    new_best_ind = i
        sol = new_best_sol
        sol_length = new_best_length

        # Step 2.2. Update tabu list
        for i in range(na):
            if i == new_best_ind:
                TC[i] = TL
            else:
                TC[i] = max(0, TC[i] - 1)

        # Step 2.3. Update the global best
        if sol_length < gbest:
            gbest = sol_length
            gbest_path = sol.copy()
            con_iter = t + 1
        iter_best.append(gbest)

        # Step 2.4. Plot the temporary result
        plt.figure()
        plt.scatter(x, y, color='black')
        for i in range(len(gbest_path) - 1):
            temp_x = [x[gbest_path[i]], x[gbest_path[i + 1]]]
            temp_y = [y[gbest_path[i]], y[gbest_path[i + 1]]]
            plt.plot(temp_x, temp_y, color='blue')
        temp_x = [x[gbest_path[-1]], x[gbest_path[0]]]
        temp_y = [y[gbest_path[-1]], y[gbest_path[0]]]
        plt.plot(temp_x, temp_y, color='blue')
        title = 'The ' + str(t + 1) + '-th iteration'
        plt.title(title)
        plt.xlabel('x coordination')
        plt.ylabel('y coordination')
        # plt.savefig(title + '.png')
        plt.show()

    # Step 3. Sort the results
    temp_x = [i for i in range(iter)]
    plt.figure()
    plt.plot(temp_x, iter_best, linewidth=2, color='blue')
    plt.xlabel('Iteration number')
    plt.ylabel('Global optimal value')
    plt.title('Convergence curve')
    plt.ticklabel_format(style='sci', scilimits=(0, 0))
    # plt.savefig('result.png')
    plt.show()
    return {'best length': gbest, 'best path': gbest_path, 'convergence iteration': con_iter}


if __name__ == '__main__':
    min_coord = 0
    max_coord = 10
    city_num = 30
    iter = 50
    x = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    y = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    print(main(x, y, iter))
    