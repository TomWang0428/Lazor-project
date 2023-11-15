# Lazor Project
This algorithm starts with a '.bff' file containing the basic settings of the lazor game, and can perform the following tasks:
<br> Identify whether the game has a solution.
<br> If there's a solution, the algorithm would generate a key for current game setting.
<br> Output the solution.
<br> 
<br> Input Requirements：
<br> To run this algorithm, the input should be:
<br> - a '.bff' file, containing the grid setting, block to put on the grid (type and quantity), lazor start point and direction, and target point to be intersected.
<br> - the organizatino of the input '.bff' file should obey the '.bff' tempelate.
<br> 
<br> Output:
<br> - an image showing the solution, in which white and grey square represents no block to put in the position. Green square means the positions of block A, black, black square means the positions of block B, and blue square means the positions of block C.
<br> 
<br> How to use:
<br> 1. when you have game setting file: open main file, input the filepath of game setting file, and see the solution (both printed as text output and saved as a image file).
<br> 2. when you don't have game setting file: open '.bff' tempelate file, change the parameters as your case, and open main file as step 1.
