# oracle_simulator

# Goal
Before a supervisor can work at a construction site, they are to be trained in how to coordinate with a bulldozer operator to clear the site in preparation for building. The training consists of interactive sessions with a simulator. This repo contains site clearing simulator written in Python

# Installation
Clone the repo and install Python3

git clone https://github.com/shahramatuber/oracle_simulator.git

Instructions on how to install python 3 can be found [here](https://realpython.com/installing-python/)

# Running Unit Tests
If you would like to run all the test at once, run the following command from repository root diretory:
`py.test`

If you want to run tests of a specific file, run the command above and specidy the file path. For example:
`py.test ./test/expense.py`

# Design 
This project consists of 3 main classes:

1- SiteMap class which is defined in `./core/site_map.py` and represents the site that will be cleared. It will be initialized by a given filepath which represents a grid of plain land, rock, removable tree, and protected tree.

2- Expense class which is defined in `./core/expense.py` and represents the costs associated with a simulation.

3- Bulldozer class which is defined in `./core/bulldozer.py` and represents a bulldozer. An object of SiteMap and Expense classes is created as member variables of Bulldozer objects. At each step, the bulldozer receives a command, updates its location, clears the land if possible, and updates the cost of operation in its expense member variable. It also keeps track of all the commands it has received since the beginning of simulation.

There is a driver program in `./simulator.py`, which instanciates a bulldozer, and sends commands to the bulldozer until user quits, or the bulldozer hits a protected tree, or the bulldozer goes out of the site map. Any of those terminating actions will end the simulation and will generate a report of all the commands and per-item and total cost of the executed commands. 

After each command, the updated site plan is printed out on the screen so the the user knows what the result of the previous action on the site map was.

# Usage
Run the following command from the repository root directory:

`python3 simulator.py <path-to-the-sitemap-file>`
  
  
There is a test file included in this repo that you can use:

`python3 simulator.py ./test/fixtures/sample1.txt`

# Example
`python3 simulator.py ./test/fixtures/sample1.txt`

Welcome to the Aconex site clearing simulator. This is a map of the site:

  -----------------------------------------------------------------  
  
o	o	t	o	o	o	o	o	o	o

o	o	o	o	o	o	o	T	o	o

r	r	r	o	o	o	o	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o

  -----------------------------------------------------------------  
  

The bulldozer is currently located at the Northern edge of the site, immediately to the West of the site, and facing East.

`(l)eft, (r)ight, (a)dvance <n>, (q)uit: a 4`

  -----------------------------------------------------------------  
  
*	*	*	*	o	o	o	o	o	o

o	o	o	o	o	o	o	T	o	o

r	r	r	o	o	o	o	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o

  -----------------------------------------------------------------  
  
`(l)eft, (r)ight, (a)dvance <n>, (q)uit: r`

  -----------------------------------------------------------------  
  
*	*	*	*	o	o	o	o	o	o

o	o	o	o	o	o	o	T	o	o

r	r	r	o	o	o	o	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o

  -----------------------------------------------------------------  
  
`(l)eft, (r)ight, (a)dvance <n>, (q)uit: a 2`

  -----------------------------------------------------------------  
  
*	*	*	*	o	o	o	o	o	o

o	o	o	*	o	o	o	T	o	o

r	r	r	*	o	o	o	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o

  -----------------------------------------------------------------  
  
`(l)eft, (r)ight, (a)dvance <n>, (q)uit: l`

  -----------------------------------------------------------------  
  
*	*	*	*	o	o	o	o	o	o

o	o	o	*	o	o	o	T	o	o

r	r	r	*	o	o	o	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o

  -----------------------------------------------------------------  
  
`(l)eft, (r)ight, (a)dvance <n>, (q)uit: a 7`

Simulation ended by attempting to move to a protected tree!

The final status of the site is shown below: 


  -----------------------------------------------------------------  
  
*	*	*	*	o	o	o	o	o	o

o	o	o	*	o	o	o	T	o	o

r	r	r	*	*	*	*	T	o	o

r	r	r	r	o	o	o	o	o	o

r	r	r	r	r	t	o	o	o	o


  -----------------------------------------------------------------  


These are the commands you issued:


Advance 4, Turn right, Advance 2, Turn left, Advance 7


The costs for this land clearing operation were:

Item                                       Quantity                 Cost

communication overhead                            5                    5

fuel usage                                       10                   10

uncleared squares                                39                  117

destruction of protected tree                     1                   10

paint damage to bulldozer                         1                    2

-----------------------------                                           

Total                                                                144


Thank you for using the Aconex site clearing simulator.
