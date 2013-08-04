#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE

def cplex(nodeCount, edgeCount, edges):
    data = open("coloring.dat","w")
    data.write("data;\n")
    data.write("param N := " + str(nodeCount) + ";\n")
    data.write("param M := " + str(edgeCount) + ";\n")

    data.write("set E :=\n")
    for e in edges:
       data.write("("+str(e[0])+","+str(e[1])+")\n")
    data.write(";\n")
    data.close()

    process = Popen(['ampl', 'coloring.run'])
    #(stdout, stderr) = process.communicate()
    process.wait()
    return 


def scip(nodeCount, edgeCount, edges):
    data = open("coloring.col","w")
    data.write("p edge " + str(nodeCount) + " " + str(edgeCount) + "\n")

    for e in edges:
       data.write("e "+str(e[0]+1)+" "+str(e[1]+1)+"\n")
    data.write("\n")
    data.close()

    #process = Popen(['/opt/scipoptsuite/scip-3.0.1/examples/Coloring/bin/coloring', '-f', 'coloring.col'])
    process = Popen(['/opt/scipoptsuite/scip-3.0.1/examples/Coloring/bin/coloring', '-c', 'read coloring.col', '-c', 'set limits time 20','-c', 'optimize', '-c','write problem coloring.csol','-c','quit'])
    #(stdout, stderr) = process.communicate()
    process.wait()
    
    csol_solution =  open("coloring.csol","r")
    opt = csol_solution.readline().split()[1]
    sol = csol_solution.readline()
    csol_solution.close()

    out_solution = open("coloring.out","w")
    out_solution.write(opt + "\n")
    out_solution.write(sol)
    out_solution.close()

    return 


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
   
    #cplex(nodeCount, edgeCount, edges)
    scip(nodeCount, edgeCount, edges)

    output = open("coloring.out","r")
    opt = output.readline()
    opt = opt.strip()
    solution = output.read()
    # prepare the solution in the specified output format
    outputData = opt + ' ' + str(1) + '\n'
    outputData += solution
    #outputData += ' '.join(map(str, solution))

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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'



