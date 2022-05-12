from vectortools import *
render_vector = Vector(0, 800)
render_metric = Tensor(1, 0, 0, -1)
origin_vector = Vector(1000/2, 800/2)
import pygame as pg
def rendering_vector(vector):
    return render_vector + render_metric.dot(vector + origin_vector)

class QuadNode:
    def __init__(self):
        self.m = 0
        self.pos = Vector(0, 0)
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def __str__(self):
        return 'QuadNode(' + str(self.m) + ', ' + str(self.pos) + ')'

    def insert(self, dir, node):
        if dir == 'nw':
            self.nw = node
        elif dir == 'ne':
            self.ne = node
        elif dir == 'sw':
            self.sw = node
        elif dir == 'se':
            self.se = node

def draw_box(min_x, min_y, length, screen):
    P_list = []
    for pos in [Vector(min_x, min_y), Vector(min_x, min_y+length), Vector(min_x+length, min_y+length), Vector(min_x+length, min_y)]:
        P = rendering_vector(pos)
        P_list.append([P.x, P.y])
    pg.draw.aalines(screen, pg.Color('red'), True, P_list, True)

def is_in_box(min_x, min_y, length, pos):
    if min_x < pos.x and pos.x < (min_x + length) and min_y < pos.y and pos.y < (min_y + length):
        return True
    else:
        return False

def make_quad_tree(min_x, min_y, length, atoms, node, screen):
    draw_box(min_x, min_y, length, screen)
    m = 0
    pos = Vector(0, 0)
    nw_atoms = []
    ne_atoms = []
    sw_atoms = []
    se_atoms = []
    for atom in atoms:
        m += atom.element.mass
        pos += atom.element.mass * atom.pos
        if is_in_box(min_x, min_y + length/2, length/2, atom.pos):
            nw_atoms.append(atom)
        elif is_in_box(min_x +length/2, min_y + length/2, length/2, atom.pos):
            ne_atoms.append(atom)
        elif is_in_box(min_x, min_y, length/2, atom.pos):
            sw_atoms.append(atom)
        elif is_in_box(min_x + length/2, min_y, length/2, atom.pos):
            se_atoms.append(atom)

    if not len(atoms) == 1:
        if not len(nw_atoms) == 0:
            node.nw = QuadNode()
            make_quad_tree(min_x, min_y + length/2, length/2, nw_atoms, node.nw, screen)

        if not len(ne_atoms) == 0:
            node.ne = QuadNode()
            make_quad_tree(min_x +length/2, min_y + length/2, length/2, ne_atoms, node.ne, screen)
        if not len(sw_atoms) == 0:
            node.sw = QuadNode()
            make_quad_tree(min_x, min_y, length/2, sw_atoms, node.sw, screen)
        if not len(se_atoms) == 0:
            node.se = QuadNode()
            make_quad_tree(min_x + length/2, min_y, length/2, se_atoms, node.se, screen)
    pos = pos/m
    node.m = m
    node.pos = pos

def print_quad_tree(tree, rank):
    if not tree == None:
        print('\t'*rank + str(tree))
        rank += 1
        print_quad_tree(tree.nw, rank)
        print_quad_tree(tree.ne, rank)
        print_quad_tree(tree.sw, rank)
        print_quad_tree(tree.se, rank)
