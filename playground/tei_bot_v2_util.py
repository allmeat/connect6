import numpy as np
from operator import itemgetter
from itertools import groupby
from random import choice
from dataclasses import dataclass
from scipy.ndimage import convolve

from typing import List

a = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
)


@dataclass
class RowConnected:
    connected_size: int
    position: List[int]


def get_white(mat) -> np.array:
    mat = np.where(mat != 2, 0, mat)
    mat = np.where(mat == 2, 1, mat)
    return mat


def get_black(mat) -> np.array:
    return np.where(mat != 1, 0, mat)


def find_connected_under_k(vec, k):
    size = len(vec)
    cum_sum_vec = np.zeros(size, dtype="int32")
    for i in range(k, 0, -1):
        conv = np.concatenate((np.convolve(vec, np.ones(i, dtype="int32"), "valid") / i, np.zeros(i - 1)))
        conv = np.where(conv != 1, 0, conv).astype("int32")
        cum_sum_vec = cum_sum_vec + conv
    diff = np.diff(cum_sum_vec)
    diff = np.concatenate((cum_sum_vec[0:1], diff))
    diff = np.where(diff < 0, 0, diff)
    return diff


def find_connected_1d(vec):
    first_element_of_connected_n = []
    if np.sum(vec) == 0:
        return first_element_of_connected_n
    vec_copy = vec.copy()
    zz4 = find_connected_under_k(vec_copy, 6)

    for k in [6, 5, 4, 3, 2, 1]:
        n_connected_position = np.where(zz4 == k)[0]
        if len(n_connected_position) >= 0:
            connected = RowConnected(connected_size=k, position=list(n_connected_position))
            first_element_of_connected_n.append(connected)
    return first_element_of_connected_n


def find_connected_edge(dic: List[RowConnected]) -> List[RowConnected]:
    connected_edge = []
    for x in dic:
        edges = sum([[y - 1, y + x.connected_size] for y in x.position], [])
        edges_filtered_distinct = list(set([v1 for v1 in edges if 0 <= v1 <= 18]))
        edges_filtered_distinct = RowConnected(x.connected_size, edges_filtered_distinct)
        connected_edge.append(edges_filtered_distinct)
    return connected_edge


def diagonal_order(matrix, row, col):
    value = []
    coord = []
    for line in range(1, (row + col)):
        start_col = max(0, line - row)
        count = min(line, (col - start_col), row)
        jj = []
        kk = []
        for j in range(0, count):
            jj.append(matrix[min(row, line) - j - 1][start_col + j])
            kk.append([min(row, line) - j - 1, start_col + j])
        value.append(np.array(jj))
        coord.append(kk)
    value_coord = list(zip(value, coord))
    return value_coord


def find_connected_19x19(mat):
    mat_copy = mat.copy()
    mat_copy_flip = np.fliplr(mat.copy())
    position = []
    diagonal_0 = diagonal_order(mat_copy, 19, 19)
    diagonal_1 = diagonal_order(mat_copy_flip, 19, 19)

    for vec, i in diagonal_0:
        if len(vec) > 5:
            connected_diagonal_0 = find_connected_1d(vec)
            if len(connected_diagonal_0) > 0:
                find_diagonal_0_edge = find_connected_edge(connected_diagonal_0)
                find_diagonal_0_edge_2d = [[(y.connected_size, i[x][0], i[x][1]) for x in y.position if x < len(vec)]
                                           for y in find_diagonal_0_edge]
                position.extend(find_diagonal_0_edge_2d)

    for vec, i in diagonal_1:
        if len(vec) > 5:
            connected_diagonal_0 = find_connected_1d(vec)
            if len(connected_diagonal_0) > 0:
                find_diagonal_0_edge = find_connected_edge(connected_diagonal_0)
                find_diagonal_0_edge_2d = [
                    [(y.connected_size, i[x][0], 18 - i[x][1]) for x in y.position if x < len(vec)] for y in
                    find_diagonal_0_edge]
                position.extend(find_diagonal_0_edge_2d)

    for i in range(19):
        connected_row = find_connected_1d(mat_copy[i, :])
        if len(connected_row) > 0:
            find_row_edge = find_connected_edge(connected_row)
            find_row_edge_2d = [[(y.connected_size, i, x) for x in y.position] for y in find_row_edge]
            position.extend(find_row_edge_2d)
        connected_col = find_connected_1d(mat_copy[:, i])
        if len(connected_col) > 0:
            find_col_edge = find_connected_edge(connected_col)
            find_col_edge_2d = [[(y.connected_size, x, i) for x in y.position] for y in find_col_edge]
            position.extend(find_col_edge_2d)

    trimmed_positions = [(int(x[0:1]), int(x[1:3]), int(x[3:5])) for x in
                         set([str(z) + "%02d" % x + "%02d" % y for z, x, y in sum(position, [])])]

    trimmed_positions = [{"count": z, "pos": "%02d" % x + "%02d" % y} for z, x, y in trimmed_positions]
    trimmed_positions = sorted(trimmed_positions, key=itemgetter('pos'))

    max_connected_positions = []
    for g, data in groupby(trimmed_positions, key=itemgetter('pos')):
        max_cnt = max(data, key=itemgetter('count'))
        max_connected_positions.append((max_cnt["count"], max_cnt["pos"]))

    connected_positions_max_by_size = {}
    for i in [1, 2, 3, 4, 5, 6]:
        ll = list(filter(lambda x: x[0] == i, max_connected_positions))
        ll2 = list(map(lambda x: (int(x[1][0:2]), int(x[1][2:4])), ll))
        connected_positions_max_by_size[i] = ll2

    return connected_positions_max_by_size


def choose_connected_position(dic, n_connected):
    put_array = np.zeros(19 * 19, dtype="int64").reshape((19, 19))
    xx1 = dic[n_connected]
    xx2 = (
        np.array(list(map(lambda x: x[0], xx1)), dtype="int64"), np.array(list(map(lambda x: x[1], xx1)), dtype="int64")
    )
    put_array[xx2] = 1

    return put_array


def neighbor_sum(mat):
    s = 2
    kernel = np.ones(s * s, dtype="int32").reshape((s, s))
    c = convolve(mat, kernel, mode='constant')
    c = c / (s * s)
    return c


def suggest_position_by_connected_element(mat, turn):
    black = get_black(mat)
    white = get_white(mat)
    all_stone = black + white

    if turn == "w":
        enemy = find_connected_19x19(black)
        me = find_connected_19x19(white)
    else:
        me = find_connected_19x19(black)
        enemy = find_connected_19x19(white)

    final_positions = np.zeros(19 * 19, dtype="int64").reshape((19, 19))
    for i in [5, 4, 3, 2, 1]:
        if i > 1:
            if len(enemy[i]) > 0:
                find_connected = choose_connected_position(enemy, i)
                available_positions = find_connected - all_stone
                available_positions = np.where(available_positions < 0, 0, available_positions)

                density = neighbor_sum(black) - neighbor_sum(white)
                positions_with_density = available_positions + density
                positions_maximizing_density = np.max(positions_with_density)
                if positions_maximizing_density > 1:
                    available_positions = np.where(positions_with_density != positions_maximizing_density, 0,
                                                   positions_with_density)

                if np.sum(available_positions) > 0:
                    final_positions = available_positions
                    break
            elif len(me[i]) > 0:
                find_connected = choose_connected_position(me, i)
                available_positions = find_connected - all_stone
                available_positions = np.where(available_positions < 0, 0, available_positions)

                density = neighbor_sum(white) - neighbor_sum(black)
                positions_with_density = available_positions + density
                positions_maximizing_density = np.max(positions_with_density)
                if positions_maximizing_density > 1:
                    available_positions = np.where(positions_with_density != positions_maximizing_density, 0,
                                                   positions_with_density)

                if np.sum(available_positions) > 0:
                    final_positions = available_positions
                    break
        else:
            if len(me[i]) > 0:
                find_connected = choose_connected_position(me, i)
                available_positions = find_connected - all_stone
                available_positions = np.where(available_positions < 0, 0, available_positions)

                density = neighbor_sum(black) - neighbor_sum(white)
                positions_with_density = available_positions + density
                positions_maximizing_density = np.max(positions_with_density)
                if positions_maximizing_density > 1:
                    available_positions = np.where(positions_with_density != positions_maximizing_density, 0,
                                                   positions_with_density)

                if np.sum(available_positions) > 0:
                    final_positions = available_positions
                    break

            elif len(enemy[i]) > 0:
                find_connected = choose_connected_position(enemy, i)
                available_positions = find_connected - all_stone
                available_positions = np.where(available_positions < 0, 0, available_positions)

                density = neighbor_sum(white) - neighbor_sum(black)
                positions_with_density = available_positions + density
                positions_maximizing_density = np.max(positions_with_density)
                if positions_maximizing_density > 1:
                    available_positions = np.where(positions_with_density != positions_maximizing_density, 0,
                                                   positions_with_density)

                if np.sum(available_positions) > 0:
                    final_positions = available_positions
                    break

    if np.sum(final_positions) == 0:
        zero_positions = np.where(all_stone == 0)
        zero_positions = list(zip(zero_positions[0], zero_positions[1]))
        selected_zero_position = choice(zero_positions)
        zero_mat = np.zeros(19 * 19, dtype="int64").reshape((19, 19))
        selected_zero_position = (np.array(selected_zero_position[0]), np.array(selected_zero_position[1]))
        zero_mat[selected_zero_position] = 1
        final_positions = zero_mat
        print("random")
    return final_positions

