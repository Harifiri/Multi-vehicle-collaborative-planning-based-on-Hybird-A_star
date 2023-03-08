import numpy as np
from model import *

class Map(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.map = np.zeros((int(2*Bound/Tile_size), int(2*Bound/Tile_size)), dtype=int)

        self.setBlock_obstacle(Block1)
        self.setBlock_obstacle(Block2)
        self.setBlock_obstacle(Block3)
        self.setBlock_obstacle(Block4)
        self.setBlock_obstacle(Block5)

    # def get_neighbers(self, state):
    #     # 获取8邻域
    #     state_list = []
    #     for i in [-1, 0, 1]:
    #         for j in [-1, 0, 1]:
    #             if i == 0 and j == 0:
    #                 continue
    #             if state.x + i < 0 or state.x + i >= self.row:
    #                 continue
    #             if state.y + j < 0 or state.y + j >= self.col:
    #                 continue
    #             state_list.append(self.map[state.x + i][state.y + j])
    #     return state_list

    def setBlock_obstacle(self, rec):
        p1, p2, p3, p4 = Rec2Pol(rec)

        x_min = int((min(p1[0], p2[0], p3[0], p4[0]) + Bound)/Tile_size)
        y_min = int((-max(p1[1], p2[1], p3[1], p4[1]) + Bound)/Tile_size)
        x_max = int((max(p1[0], p2[0], p3[0], p4[0]) + Bound)/Tile_size)
        y_max = int((-min(p1[1], p2[1], p3[1], p4[1]) + Bound)/Tile_size)

        print(x_min,y_min,x_max,y_max)
        for i in range(x_min,x_max,1):
            for j in range(y_min,y_max,1):
                self.map[i][j] = 1

    def setCar_obstacle(self, pol):
        p = np.array(pol)
        p = (p + Bound)*10/Tile_size

        p1, p2, p3, p4 = p

        x_min = int(min(p1[0], p2[0], p3[0], p4[0]))
        y_min = int(min(p1[1], p2[1], p3[1], p4[1]))
        x_max = int(max(p1[0], p2[0], p3[0], p4[0]))
        y_max = int(max(p1[1], p2[1], p3[1], p4[1]))

        for i in range(x_min,x_max,1):
            for j in range(y_min,y_max,1):
                if IsPointInRec((i,j), p):
                    self.map[i][j].set_state(1)