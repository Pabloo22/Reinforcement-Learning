# The racetrack game
Consider driving a race car
around a turn like those shown in Figure 5.11 (a grid of squares). You want to go as fast as
possible, but not so fast as to run off the track. In our simplified racetrack,
the car is at one of a discrete set of grid positions, the cells in the diagram. The
velocity is also discrete, a number of grid cells moved horizontally and vertically
per time step. The actions are increments to the velocity components. Each
may be changed by +1, −1, or 0 in one step, for a total of nine actions.

Both velocity components are restricted to be nonnegative and less than 5,
and they cannot both be zero. Each episode begins in one of the randomly
selected start states and ends when the car crosses the finish line. The rewards
are −1 for each step that stays on the track, and −5 if the agent tries to drive
off the track. Actually leaving the track is not allowed, but the position is
always advanced by at least one cell along either the horizontal or vertical
axes. With these restrictions and considering only right turns, such as shown
in the figure, all episodes are guaranteed to terminate, yet the optimal policy
is unlikely to be excluded. To make the task more challenging, we assume that
on half of the time steps the position is displaced forward or to the right by
one additional cell beyond that specified by the velocity. Apply a Monte Carlo
control method to this task to compute the optimal policy from each starting
state. Exhibit several trajectories following the optimal policy.

(This game is the Exercise 5.9 from the Sutton and Barto book: 
https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)
