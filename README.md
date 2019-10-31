# Artificial Ecosystem
“Artificial Ecosystem” is a complex self-running virtual 2D ecosystem where user can interact with the environment ( spawning food and killing animals by creating wetlands) and can explore the ecosystem. Each species move around as a group as a whole and have their unique prey. They reproduce after certain age and die at certain age. 
Virus appears at certain point when the whole population exceeds certain level. This emergency situation let the ecosystem to run and balance itself endlessly, adding complexity to the ecosystem. 

[![Watch the video](https://i.imgur.com/jT4xh2D.jpg)](https://vimeo.com/333818929)
click to view the video

### How to run the projec
Run "__init__.py" file 

### Libraries
tkinter, random, math, numpy, PIL, shapely

### Shortcut
N/A

### Competitive Analysis
1. Past 15-112 Project [“Evolve”](https://www.youtube.com/watch?v=14zm7Z8k3lo) byy Mina Nowroozi 
2. Interactive video game [“Spore”](https://www.youtube.com/watch?v=bTC8QPjI3YI) by EA 
3. Interactive Art Installation [“Archipelago”](https://vimeo.com/120987833) by Artificial Nature 

### Optimized collision detection - Grid System
In order to deal with collision detection, I came with Grid System. The whole screen runs with grid system which has several grids. Each grid holds “food” and “species”, as what each grid contains are updated as these objects move. Each species will collision detection with only the food and other species that are in the same grid. Following image is a visualization of grid system and how each food and species belong to each grid.
![Artificial Ecosystem1](https://i.imgur.com/rh4Qirt.png)



### Virus : controlling over-population and leg
Virus appears at certain point when the whole population exceeds certain level. All the species freezes while all the viruses are gone. Virus has target prey to eat the most populated species. Once that mission is accomplished, it turns into least-populated species. This emergency situation let the ecosystem to run and balance itself endlessly, adding complexity to the ecosystem.
![Articial Ecosystem2](https://i.imgur.com/GiVRNLE.png)
