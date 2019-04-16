# object World
#   attribute Species[]
#   attribute Foods[]
#
# object DNA
#   attribute genes
#
# object Species
#   attribute DNA
#   attribute location
#   attributes predators[]
#   attributes prey[]
#   attribute age
#   function move
#   function eat
#   function attack
#   functino reproduce
# 
# object A inherits from Species....
# object B inherits from Species....
# object C inherits from Species....
# ..... so on..... depending n design...... 
#
# object Food 
#   attribute location
#   attribute energy
#   attribute life


#########################################################
# Algorithmic plan for Flock Behavior
#########################################################
#
# First : Generate a set of animals
# 	- differnt list of species

# Second : Make basic steering force template
#	- steering force : desired velocity - current velocity
#   - apply force
#
# Third : Make three different steering forces 
#	- avoidance : try not to bump into each other (with same species) 
#   - align : head in same direction as neighbor
#   - cohesion : staying in the gorup 
#   - seek : seek for food and prey 

#########################################################
