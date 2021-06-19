# NEAT-Parkour
Using the NEAT genetic algorithm to solve a reinforcement learning problem. In other words, teaching an AI parkour!

## Overview of NEAT
NEAT (Neural Evolution of Augmenting Typologies) is a genetic algorithm that, since 2002, has become a hallmark algorithm of reinforcement learning. Unlike backpropagation-based RL algorithms that rely on gradient descent, NEAT learns models by augmenting the weights and typologies (nodes and edges) of networks, starting from the most basic of networks - one edge connecting one input to one output. It's really amazing! ([Stanley, 2002](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf))

## This Adventure
In NEAT-Parkour, I use my implementation of NEAT to train AIs to play a parkour-platformer at a superhuman level. The initial population is `1000` agents. In each generation, agents play in batches of `150`. Moderate scores, `75 - 200`, can be achieved in fewer than `20` generations (< 1 hr). To achieve high scores, `200 - 250`, the population requires at least `20` generations (≈ 2 hr). The best score achieved `359` required 34 generations (> 4 hr).

## Genome display 
In the top right, you'll see the genome of current best agent. Input nodes are blue. Output nodes are red. Hidden nodes are grey. Active edges are green, inactive 
edges are red. The width of edges increases with the magnitude of their weight.

### Inputs (6)
1. Head height
2. Distance to the next head-height block
3. Distance to the next (head-height - 1) block
4. Type of next head-height block
5. Type of next (head-height - 1) block
6. Game speed

### Outputs (4)
1. Run
2. Jump
3. Slide
4. Attack

![NEAT2](https://user-images.githubusercontent.com/45083086/122322701-20e97180-cee3-11eb-95e4-bbfa3b44f246.png)
 
