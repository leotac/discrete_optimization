#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from subprocess import Popen

def scip(points):
    data = open("tsp.tsp","w")
    data.write("NAME : tsp\n")
    data.write("TYPE : TSP\n")
    data.write("DIMENSION : "+str(len(points))+"\n")
    data.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
    data.write("DISPLAY_DATA_TYPE : TWOD_DISPLAY\n")
    data.write("DISPLAY_DATA_SECTION\n")

    for i,p in enumerate(points):
       data.write(str(i+1)+" "+str(p[0])+" "+str(p[1])+"\n")
    data.write("EOF\n")
    data.close()

    process = Popen(['/opt/scipoptsuite/scip-3.0.1/examples/TSP/bin/sciptsp', '-c', 'read tsp.tsp', '-c', 'set limits time 120','-c', 'optimize', '-c', 'write solution tsp.sol','-c','quit'])
    process.wait()
    
    solution =  open("tsp.sol","r")
    optimal = 1 if solution.readline().split()[2]=="optimal" else 0
    opt_value = solution.readline().split()[2]
    edges = {} 
    for line in solution:
       name = line.split()[0]
       name = name.split("_")[2]
       i,j = name.split("-")
       edges.setdefault(int(i)-1,[]).append(int(j)-1)
       edges.setdefault(int(j)-1,[]).append(int(i)-1)
    
    node = 0
    tour = [0]
    next_node = edges[node][0]
    edges[node].remove(next_node)
    edges[next_node].remove(node)
    tour.append(next_node)
    node = next_node
    while node != 0:
       next_node = edges[node][0]
       edges[node].remove(next_node)
       edges[next_node].remove(node)
       tour.append(next_node)
       node = next_node

    print optimal, opt_value, tour
    return optimal, opt_value, tour
   

#    sol = csol_solution.readline()
#    csol_solution.close()
#
#    out_solution = open("coloring.out","w")
#    out_solution.write(opt + "\n")
#    out_solution.write(sol)
#    out_solution.close()


def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    nodeCount = int(lines[0])

    points = []
    pointsX = []
    pointsY = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))
        pointsX.append(float(parts[0]))
        pointsY.append(float(parts[1]))

    #from pylab import plot, ion, show, scatter
    #ion()
    #scatter(pointsX,pointsY)

    #print points
    arcs = []
    cost = {}
    for i,a in enumerate(points):
       for j,b in enumerate(points):
          if i != j:
             arcs.append((i,j))
             cost[(i,j)] = length(a,b)
    #print arcs
 
    #optimal, opt_value, tour = scip(points)
    import tsp
    # build a trivial solution
    #solution = range(0, nodeCount)
    #solution = tsp.tsp2(range(0,nodeCount), arcs, cost)
    #solution = tsp.tsp(range(0,nodeCount), arcs, cost)
    #solution = tsp.christo(range(0,nodeCount), arcs, cost)
    solution = tsp.doubletree(range(0,nodeCount), arcs, cost)
    #solution = tour[:-1]

    import sa
    #sa.sa(range(0,nodeCount),arcs,cost,solution)
    solution = sa.sa(range(0,nodeCount),arcs,cost,points,solution)
    optimal = 0

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    opt_value = obj

    # prepare the solution in the specified output format
    outputData = str(opt_value) + ' ' + str(optimal) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

