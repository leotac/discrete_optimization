import numpy as np

def approximate(capacity, values, weights, factor):

   capacity = capacity/factor
   weights =  np.ceil(np.array(weights, dtype=float)/factor)
   return dp(capacity, values, weights)


def dp(capacity, values, weights):

   items = len(values)
   m = np.zeros((items, capacity+1), dtype=int)
   #taken = np.zeros((items, capacity+1), dtype=int)
   taken = {}

   print "Table size:", items*(capacity)

   chunk = items*capacity / 20 

   # m[i,w] - max value using up to item 'i' and not exceeding capacity 'c'
   
   # max value not exceeding capacity 0 is 0
   for i in xrange(items):
      m[i,0] = 0

   for c in xrange(1,capacity+1):
      for i in xrange(items):
         percent = 100.0*(items*(c-1) + i)/(items*capacity)
         #print percent
         if (items*(c-1)+i) % chunk == 0:
            print percent
      
         # if weight of item i is greater than current capacity c, 
         # the value cannot improve 
         if weights[i] > c:
            if i>=1:
               m[i,c] = m[i-1,c]
            else:
               m[i,c] = 0
         # if weight of item i fits current capacity c, 
         # try to improve
         else:
            if i >= 1:
               m[i,c] = max( m[i-1,c], m[i-1, c-weights[i]] + values[i] )
               if m[i,c] != m[i-1,c]:
                  taken[i,c] = 1
            else:
               m[i,c] = values[i]
               taken[i,c] = 1

   opt = m[items-1, capacity]
   take = np.zeros(items, dtype=int)
   i,c = items-1,capacity
   while i>=0 and c>=0:
      if taken.get((i,c)) == 1:
         take[i] = 1
         i,c = i-1, c-weights[i]
      else:
         i,c = i-1, c
   #print "Optimal solution:", take
   #print "Optimum:", opt
   return opt, list(take)


def inline_dp(capacity, values, weights):

   items = len(values)
   m = np.zeros((capacity+1), dtype=int)
   #taken = np.zeros((items, capacity+1), dtype=int)
   taken = {}

   print "Table size:", items*(capacity)

   chunk = items*capacity / 20 

   # m[i,w] - max value using up to item 'i' and not exceeding capacity 'c'
   
   # max value not exceeding capacity 0 is 0

   for c in xrange(1,capacity+1):
      m[c]=0

   for c in xrange(1,capacity+1):
      for i in xrange(items):
         percent = 100.0*(items*(c-1) + i)/(items*capacity)
         #print percent
         if (items*(c-1)+i) % chunk == 0:
            print percent
      
         # if weight of item i is greater than current capacity c, 
         # the value cannot improve 
         if weights[i] > c:
            if i==0:
               m[c] = 0
            #else:
            #   m[i,c] = m[i-1,c]
         # if weight of item i fits current capacity c, 
         # try to improve
         else:
            if i >= 1:
               if (m[c-weights[i]] + values[i]) > m[c]:
                  m[c] = m[c-weights[i]] + values[i]
                  taken[i,c] = 1
            else:
               m[c] = values[i]
               taken[i,c] = 1

   opt = m[capacity]
   take = np.zeros(items, dtype=int)
   i,c = items-1,capacity
   while i>=0 and c>=0:
      if taken.get((i,c)) == 1:
         take[i] = 1
         i,c = i-1, c-weights[i]
      else:
         i,c = i-1, c
   #print "Optimal solution:", take
   #print "Optimum:", opt
   return opt, list(take)
