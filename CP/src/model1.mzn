%% Dicosola Alessandro
%% model1.mzn - Simple model for the problem

include "globals.mzn";

% Constants
%% Total width
int: W;
set of int: WIDTH = 1..W;
%% Total height
int: H;
set of int: HEIGHT = 1..H;
%% Amount of presents
int: N;
set of int: Presents = 1..N;
%% Array of width of each present
array[Presents] of WIDTH: widths;
%% Array of heights of each present
array[Presents] of HEIGHT: heights;
%% Array of areas
array[Presents] of 1..W*H: areas = [ widths[i]*heights[i] | i in Presents ];
int: index_max = arg_max(areas);
%% Upper bound for width and height of each present
array[Presents] of 0..W-1: W_UB = [ W - widths[i]  | i in Presents ];
array[Presents] of 0..H-1: H_UB = [ H - heights[i] | i in Presents ];

% Set constants for testing
% N = 20;
% W = 40;
% H = 40;
% widths =  [3,3,3,3,3,3,3,3,3,3,3,4,4,4,5,5,5,5,5,22];
% heights = [3,4,5,6,7,8,9,10,12,16,40,4,14,22,3,4,8,12,13,40];
% N = 21;
% W = 27;
% H = 27;
% widths =  [3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4];
% heights = [3,4,5,6,7,8,9,10,11,12,19,20,21,3,4,6,7,8,14,19,20];
% N=29;
% W=39;
% H=39;
% widths = [3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,15];
% heights = [3,4,5,6,7,8,9,10,11,15,3,4,5,6,8,9,12,15,16,3,4,5,6,8,10,11,13,18,39];
% N=9;
% W=13;
% H=13;
% widths=[3,3,3,3,3,3,4,4,7];
% heights=[3,4,5,6,7,8,3,4,6];
% N=10;
% W=15;
% H=15;
% widths=[3,3,3,3,3,3,3,3,3,6];
% heights=[3,4,5,6,7,8,9,12,15,3];
% N=27;
% W=37;
% H=37;
% widths=[3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,12];
% heights=[3,4,5,6,7,8,9,11,12,13,14,17,18,21,3,4,5,6,10,22,24,3,4,6,10,14,37];
% N=7;
% W=11;
% H=11;
% widths = [3,3,3,3,5,5,8];
% heights= [3,4,5,6,3,4,4];

%Decision variable
%% Array of starting position X and Y to be found
array[Presents] of var 0..W-1: X;
array[Presents] of var 0..H-1: Y;

% Constraints
predicate largest_rect() = let {int: h = heights[index_max]; } in h==H;
constraint if largest_rect() then X[index_max] = W - widths[index_max] /\ Y[index_max]=0 endif;

%% Boundaries 
constraint forall(p in Presents where p!=index_max)(if largest_rect() then X[p] <= X[index_max] - widths[p] else X[p] <= W_UB[p] endif /\ Y[p] <= H_UB[p])::domain;

%% Symmetries breaking
%
%Flip rects over y 
constraint lex_lesseq(X,[-X[i]-widths[i]+W | i in Presents]);
%Flip rects over x
constraint lex_lesseq(Y,[-Y[i]-heights[i]+H | i in Presents]);
%Flip rects over origin
%It is contained in the ones before

function array[int] of var int: rotate90(var int:x,var int:y,int:cx,int:cy) = 
[-(y-cy)+cx , (x-cx)+cy ];
% function array[int] of var int: rotate180(var int:x,var int:y,int:cx,int:cy) = 
% [-(x-cx)+cx , -(y-cy)+cy ];
% function array[int] of var int: rotate270(var int:x,var int:y,int:cx,int:cy) = 
% [(y-cy)+cx , -(x-cx)+cy ];

constraint 
let {
int: cx = W div 2 + (if W mod 2 = 0 then 1 else -1 endif);
int: cy = H div 2 + (if H mod 2 = 0 then 1 else -1 endif);
array[int] of var int: seqX90 = [ rotate90(X[p],Y[p]+heights[p],cx,cy)[1] | p in Presents ];
array[int] of var int: seqY90 = [ rotate90(X[p],Y[p]+heights[p],cx,cy)[2] | p in Presents ];
} in lex_lesseq(X,seqX90) /\ lex_lesseq(Y,seqY90);


%% No overlapping between rectangles
constraint diffn(X,Y,widths,heights);
  
%% Implicit constraint
constraint cumulative(X,widths,heights,H) /\ cumulative(Y,heights,widths,W);

constraint forall(x in 0..W-1 where count(X,x)>0)(sum(p in Presents where X[p] <= x /\ X[p]+widths[p]>x)(heights[p])=H);
% Inserting the constraint below does not allow to have a gain in performance
% constraint forall(y in 0..H-1 where count(Y,y)>0)(sum(p in Presents where Y[p] <= y /\ Y[p]+heights[p]>y)(widths[p])=W);

% Use with Gecode solver
% ============================================================================================
% solve ::seq_search([int_search(X,smallest,indomain_min),int_search(Y,input_order,indomain)]) satisfy;
% ============================================================================================

% Use with Chuffed solver  
% ==========================================================================
include "chuffed.mzn";
solve ::seq_search([
          priority_search(areas,[int_search([X[p]],smallest,indomain_min) | p in Presents],largest,indomain_max),
          int_search(Y,largest,indomain_max)
          ]) satisfy; 
% ==========================================================================
 
output ["\(W) \(H)\n","\(N)\n"];
output ["\(widths[i]) \(heights[i]) \(X[i]) \(Y[i])\n" | i in 1..N];
% output [show(X) ++ "\n" ++ show(Y) ++ "\n" ++ show(widths) ++ "\n" ++ show(heights) ++ "\n" ++ show(areas) ++ "\n"];