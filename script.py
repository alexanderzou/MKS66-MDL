import mdl
from display import *
from matrix import *
from draw import *
import math

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # print(symbols)
    # print(stack)
    # for command in commands:
        # print(command)
        
    points = []
    clear_screen(screen)
    clear_zbuffer(zbuffer)
    
    for command in commands:
        op = command['op']
        if op == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        elif op == 'pop':
            stack.pop()
        elif op == 'move':
            tmp = make_translate(command['args'][0], command['args'][1], command['args'][2])
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
        elif op == 'scale':
            tmp = make_scale(command['args'][0], command['args'][1], command['args'][2])
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
        elif op == 'rotate':
            theta = command['args'][1] * (math.pi / 180)
            if command['args'][0] == 'x':
                tmp = make_rotX(theta)
            elif command['args'][0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            #print(tmp)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
        elif op == 'sphere':
            if command['constants'] == None:
                ref = '.white'
            else:
                ref = command['constants']
            val = command['args']
            add_sphere(points, val[0], val[1], val[2], val[3], step_3d)
            matrix_mult( stack[-1], points )
            draw_polygons(points, screen, zbuffer, view, ambient, light, symbols, ref)
            points = []
        elif op == 'torus':
            if command['constants'] == None:
                ref = '.white'
            else:
                ref = command['constants']
            val = command['args']
            add_torus(points, val[0], val[1], val[2], val[3], val[4], step_3d)
            matrix_mult( stack[-1], points )
            draw_polygons(points, screen, zbuffer, view, ambient, light, symbols, ref)
            points = []
        elif op == 'box':
            if command['constants'] == None:
                ref = '.white'
            else:
                ref = command['constants']
            val = command['args']
            add_box(points, val[0], val[1], val[2], val[3], val[4], val[5])
            matrix_mult( stack[-1], points )
            draw_polygons(points, screen, zbuffer, view, ambient, light, symbols, ref)
            points = []
        elif op == 'line':
            val = command['args']
            add_edge(points, val[0], val[1], val[2], val[3], val[4], val[5])
            matrix_mult( stack[-1], points )
            draw_lines(points, screen, zbuffer, color)
            points = []
        elif op == 'save':
            #print(command['args'][0]+'.png')
            save_extension(screen, command['args'][0]+'.png')
        elif op == 'display':
            display(screen)