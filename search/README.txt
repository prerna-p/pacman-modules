Q6.
The logic for the heuristic is similar to that of building a minimum spanning tree where the nodes are the
corners of the maze. 
(1) compute the cost from current state to all the corners
(2) find and store the minimum cost from previous step
(3) set the next state to the corner corresponding to the minimum cost  
 repeat 
note : value in step (2) is incrementally updated in each iteration.
the cost of the minimum spanning tree by definition would have the least cost for a round trip on the maze that
reaches every corner.
Cost is calculated via manhattan distance, so it is an optimistic estimate compared to actual cost it would take
from current position to the food. Therefore the heuristic is admissible and consistent

Q7.
The food that is farthest from its current position is the distance pacman has to atleast travel. Therefore the 
heuristic is calculated by finding the straight line distance to the food that is farthest from pacman's current
position. 
This is an unestimation of the actual distance to the farthest food as walls and other obstacles have
not been considered therefore the heuristic is admissible and consistent.