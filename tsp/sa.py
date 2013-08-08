from gurobipy import *
import random
import math
import os
import string




def swap(solution, cost, index1, index2):
   index1, index2 = min(index1,index2), max(index1,index2)
   assert index1 <= index2
   n= len(solution)
   if index1 == index2 or index1==index2+1 or index2==index1+1:
      return None, 0
   i,j = solution[index1], solution[index1+1]
   k,l = solution[index2], solution[(index2+1)%n]
   delta = cost[(i,k)] + cost[(j,l)] - (cost[(i,j)] + cost[(k,l)])
   # take vector from index+1 to index2 and reverse it!
   solution = solution[:index1+1] + solution[index2:index1:-1] + solution[index2+1:]
   return solution, delta

def swap_3(solution, cost, index1, index2):
   n = len(solution)
   if index1 == index2 or index1==(index2+1)%n or index2==(index1+1)%n: # \
         #or index1<1 or index1+1>len(solution)-2 \
         #or index2<0 or index2>len(solution)-2:
      return None, 0
   i,j = solution[index1], solution[(index1+1)%n]
   l,k = solution[index2], solution[(index2+1)%n]
   delta = cost[i,k] + cost[l,j] + cost[solution[(index1-1)%n],solution[(index1+2)%n]] - (cost[l,k] + cost[solution[(index1-1)%n],i]+ cost[j,solution[(index1+2)%n]])
   print (i,k), (l,j), (solution[(index1-1)%n],solution[(index1+2)%n])
   print (l,k), (solution[(index1-1)%n],i), (j,solution[(index1+2)%n])
   if index1 < index2:
      solution = solution[:index1] + solution[index1+2:index2+1] + [j,i] + solution[index2+1:]
   if index2 < index1:
      solution = solution[:(index2+1)] + [j,i] + solution[(index2+1):index1] + solution[(index1+2):]
   return solution, delta

def swap_p(solution, cost, index1, index2, p):
   index1, index2 = min(index1,index2), max(index1,index2)
   n = len(solution)
   if index1 == index2 or index2 <= index1+p or index1==(index2+1)%n or index1<1: # \
         #or index1<1 or index1+1>len(solution)-2 \
         #or index2<0 or index2>len(solution)-2:
      return None, 0
   i,j = solution[index1], solution[(index1+p)%n]
   l,k = solution[index2], solution[(index2+1)%n]
   delta = cost[i,k] + cost[l,j] + cost[solution[(index1-1)%n],solution[(index1+p+1)%n]] - (cost[l,k] + cost[solution[(index1-1)%n],i]+ cost[j,solution[(index1+p+1)%n]])
   #print "Old:",(l,k), (solution[(index1-1)%n],i), (j,solution[(index1+p+1)%n])
   #print "New:",(i,k), (l,j), (solution[(index1-1)%n],solution[(index1+p+1)%n])
   if index1 < index2:
      solution = solution[:index1] + solution[index1+p+1:index2+1] + solution[index1+p:index1-1:-1] + solution[index2+1:]
   return solution, delta

def sa(nodes, arcs, cost, points, tour=None):
   random.seed(2)
   if tour is None:
      cur_tour = nodes[:]
   else:
      cur_tour = tour[:]
   best_tour = cur_tour[:]
   n = len(cur_tour)
   best_val = sum([cost[(cur_tour[i],cur_tour[(i+1)%n])] for i in xrange(n)])
   cur_val = best_val
   alpha = 0.999
   temperature = 20*cur_val
   best_it=0
   reheat_it=0
   last_improvement=0
   print "SA start:",best_val, best_tour
   
   import matplotlib.pyplot as plt
   #plt.figure(figsize=(8,8)
   plt.ion()
   import networkx as nx
   def display_sol(sss):
      G=nx.Graph()
      for v in range(n):
         G.add_node(v)
      for i,v in enumerate(sss):
         G.add_edge(sss[i],sss[(i+1)%n])
      plt.clf()
      nx.draw(G,points,node_size=5,with_labels=False)
      plt.draw()
   
   for i in xrange(2000):
      delta = best_val
      tour = None
      for t in xrange(1000): 
         if random.random() < 0.5:
            newtour, newdelta = swap(cur_tour, cost, random.randint(0,n-1), random.randint(0,n-1))
         else:
            newtour, newdelta = swap_p(cur_tour, cost, random.randint(1,n-1), random.randint(1,n-1), random.randint(1,n-3))
         if newdelta < delta and newtour is not None:
            tour = newtour[:]
            delta = newdelta

      if tour is None:
         continue
      if delta < 0.0 or random.random() < math.exp(-delta/temperature):
         cur_tour = tour[:]
         cur_val += delta
         last_improvement = i
         if cur_val < best_val:
            best_val = cur_val
            best_tour = cur_tour[:]
            display_sol(best_tour)
            best_it = i
            print "new best", best_val, i
      temperature *= alpha
      if last_improvement - i > 50000:
         print "last"
      if i - reheat_it > 1000 and i - best_it > 1000:
         print "reheat"
         reheat_it = i
         temperature = 2*cur_val
      if i - best_it > 1000:
         print "restart"
         best_it = i
         cur_tour = best_tour[:]
         cur_val = sum([cost[(cur_tour[i],cur_tour[(i+1)%n])] for i in xrange(n)])
         temperature = 2*cur_val

   print "SA end",best_val, best_tour
   return best_tour 

if __name__ == '__main__':
	main()
