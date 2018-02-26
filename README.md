# dendryt

## Description
Cell migration simulator written overnight.

A cell is a pixel on a canvas. Each iteration, it can go North, South, East or West. If the persistance index is high, chances are it will continue in the same direction.

The score is calculated as the number of pixels visited after a maximum number of moves. Each persistance index is tested several time to make a mean.

## Results

Persistance of 1:

![pers1](https://i.imgur.com/s0eoSYe.png)

Persistance of 81:

![pers81](https://i.imgur.com/Hjgktlp.png)

All the means plotted:

![all](https://i.imgur.com/maUiqKN.png)
