# NEAT-Parkour
Using the NEAT genetic algorithm to solve a reinforcement learning problem. In other words, teaching an AI parkour!

## Overview of NEAT
NEAT (Neural Evolution of Augmenting Typologies) is a genetic algorithm that, since 2002, has become a hallmark algorithm of reinforcement learning. Unlike backpropagation-based RL algorithms that rely on gradient descent, NEAT learns models by augmenting the weights and typologies (nodes and edges) of networks, starting from the most basic of networks - one edge connecting one input to one output. It's really amazing! ([Stanley, 2002](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf))

## This Adventure
In NEAT-Parkour, I use my implementation of NEAT to train AIs to play a parkour-platformer at a superhuman level. The initial population is `1000` agents. In each generation, agents play in batches of `150`. Moderate scores, `50 - 100`, can be achieved in fewer than `20` generations (10 - 20min). To achieve high scores, `130 - 200`, the population requires at least `40` generations (roughly 2 hours - the games get longer as the population gets better). 

## Genome display 
In the top right, you'll see the genome of current best agent. Input nodes are blue. Output nodes are red. Hidden nodes are grey. Active edges are green, inactive edges are red.

![NEAT2](https://user-images.githubusercontent.com/45083086/122322701-20e97180-cee3-11eb-95e4-bbfa3b44f246.png)
 
