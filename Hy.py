# coding:utf-8
# @author: Jeremy Tsui
# @date  : 2019-05-08 10:05
# @file  : maze-generator-binary-tree.py
# @IDE   : PyCharm
# @brief : This script generate a maze by binary tree algorithm in Minecraft.

import random
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.block as block
# import ministackstuff as ms

name = "Hy"
# Makes the boundary walls, entrance and exit points of the maze.
def Maze_Init(mc, mc_x, mc_y, mc_z, width, height, length, material):
    # Create an area filled with material.
    maze = np.full((length, width), 0, dtype="uint8")
    # Base
    mc.setBlocks(mc_x, mc_y - 1, mc_z, mc_x + width - 1, mc_y + height - 2, mc_z + length - 1, material)
    mc.setBlocks(mc_x, mc_y, mc_z, mc_x + width - 1, mc_y + height + 4, mc_z + length - 1, 0)
    #
    mc.setBlocks(mc_x, mc_y, mc_z, mc_x + width - 1, mc_y + height - 1, mc_z + length - 1, material)
    # Entrance and exit.
    maze[0, 1] = 1
    mc.setBlocks(mc_x + 1, mc_y, mc_z, mc_x + 1, mc_y + height - 1, mc_z, block.AIR)
    maze[length - 1, width - 2] = 1
    mc.setBlocks(mc_x + width - 2, mc_y, mc_z + length - 1, mc_x + width - 2, mc_y + height - 1, mc_z + length - 1,
                 block.AIR)
    return maze


# The binary tree algorithm. Randomly craves horizontally or vertically.
def Maze_CravePassage(mc, maze, mc_x, mc_y, mc_z, height):
    # Loop through every second cell.
    for z in range(1, maze.shape[0] - 1, 2):
        for x in range(1, maze.shape[1] - 1, 2):
            # Decide which orientation we shall crave.
            # Normally we choose randomly, except at the end sides.
            if (((maze.shape[1] - 2) == x) and ((maze.shape[0] - 2) == z)):
                orientation = "none"
            elif ((maze.shape[1] - 2) == x):
                orientation = "vertical"
            elif ((maze.shape[0] - 2) == z):
                orientation = "horizontal"
            else:
                orientation = random.choice(["horizontal", "vertical"])

            # Crave horizontally or vertically 2 cells.
            if ("horizontal" == orientation):
                maze[z, x:x + 3] = 1
                mc.setBlocks(mc_x + x, mc_y, mc_z + z, mc_x + x + 2, mc_y + height - 1, mc_z + z, block.AIR)
            elif ("vertical" == orientation):
                maze[z:z + 3, x] = 1
                mc.setBlocks(mc_x + x, mc_y, mc_z + z, mc_x + x, mc_y + height - 1, mc_z + z + 2, block.AIR)
            else:
                return


# Main function.
def main(width, height, length, material):
    mc = minecraft.Minecraft.create()  # address='192.168.0.109'

    # Make sure, that width and length are odd numbers.
    if ((not (width % 2)) or (not (length % 2))):
        print("Width and length must be odd numbers!")
        return

    # Get position of the player. Shift it a little, so the entrance is going to be in front of the player.
    player_name = mc.getPlayerEntityId(name)
    mc_x, mc_y, mc_z = mc.entity.getPos(player_name)
    mc_x -= 1
    mc_z += 2

    # Init and do the algorithm.
    maze = Maze_Init(mc, mc_x, mc_y, mc_z, width, height, length, material)
    Maze_CravePassage(mc, maze, mc_x, mc_y, mc_z, height)
    # mc.postToChat("Maze generation done[binary tree algorithm]!")


block_id = block.ICE
# p = 'JeremyTsui'
# m = ms.Ministack()  # 47.105.46.254 address='192.168.0.109'
main(25, 5, 25, block_id)
