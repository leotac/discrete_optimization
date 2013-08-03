param N; # := 4;
param M;
set V default {}; #:= 0..N-1;
set E within {V,V} default {}; #:= {(0,1),(1,2),(1,3)};
set COLORS := 0..N;

var assignment{v in V, c in COLORS} binary;
var color{c in COLORS} binary;

minimize colors:
   sum{c in COLORS} color[c];

subject to priority{c in 0..N-1}:
   color[c]>=color[c+1];

subject to prior{v in V, c in COLORS : c>0}:
   assignment[v,c] <= sum{i in V : i<v}assignment[i,c-1];

subject to different_color{(i,j) in E, c in COLORS}:
   assignment[i,c] + assignment[j,c] <= 1;

subject to one_color{v in V}:
   sum{c in COLORS}assignment[v,c] >= 1;

#subject to color_use{c in COLORS}:
#   sum{v in V}assignment[v,c] <= N*color[c];

subject to color_use_single{v in V, c in COLORS}:
   assignment[v,c] <= color[c];
