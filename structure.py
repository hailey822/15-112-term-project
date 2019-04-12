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
# Algorithmic plan for populating the field with monsters
#########################################################
#
# First: generate a set of monsters with varying attack levels
# 	- number of monsters should be determined by field size
# 	- level should be determined by hero level at beginning: half should be at
#     hero level, 1/4 one level above, 1/4 two levels above, and 1 five levels above
#	- distinguish monsters based on fill color?
#
# Second: determine where monsters should be placed on the field
#	- use random library to randomly place them
#	- but weight the placement so that easier monsters mostly appear closer to the hero
#	- non-randomly place the boss monster at the end
#
# Third: don't start monster movement until the gameplay starts
#	- have a class method to pause/unpause all monsters? or put a block in timerFired?
#########################################################
