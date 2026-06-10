## Overview

# task 1
Used BFS for finding the shortest path between two links. In order to keep track of the path I stored the path using a list and added new link each time. I used a helper function where it converts list of IDs to titles to return the shortest path with titles.

# task 2
Used the page rank algorithm we went over in class. In order to make it O(N+E), instead of distributing .15 of rank to each node every time, I accumulated all the ranks to be distributed to all nodes and processed it all at once. This avoided to be O(N^2)
Question: what is a fair threshold to check if the sum of all the ranks are held constant?
