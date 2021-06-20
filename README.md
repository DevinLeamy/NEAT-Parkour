# NEAT-Parkour
Using the NEAT genetic algorithm to solve a reinforcement learning problem. In other words, teaching an AI parkour!

## Overview of NEAT
NEAT (Neural Evolution of Augmenting Typologies) is a genetic algorithm that, since 2002, has become a hallmark algorithm of reinforcement learning. Unlike backpropagation-based RL algorithms that rely on gradient descent, NEAT learns models by augmenting the weights and typologies (nodes and edges) of networks, starting from the most basic of networks - one edge connecting one input to one output. It's really amazing! ([Stanley, 2002](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf))

## This Adventure
In NEAT-Parkour, I use my implementation of NEAT to train AIs to play a parkour-platformer (built in pygame) at a superhuman level. The initial population is `1000` agents. In each generation, agents play in batches of `150`. Moderate scores `(75 - 200)` can be achieved in fewer than `20` generations (≈ 1 hr). High scores `(200 - 250)` can expect at least `20` generations (≈ 2 hr). The best score achieved `359` required 43 generations (≈ 5 hr).

## Genome display 
In the top right, you'll see the genome of current best agent. Input nodes are blue. Output nodes are red. Hidden nodes are grey. Active edges are green, inactive 
edges are red. The width of edges increases with the magnitude of their weight.

## Highlights
The highlights of each generation (the best agents of each generation) are shown when training is complete and the population size becomes 0. To skip to the highlights press `h`, ending the training.

![NEAT](https://user-images.githubusercontent.com/45083086/122660182-81bfb680-d13c-11eb-8cb1-159b71578594.png)

[Early training](https://user-images.githubusercontent.com/45083086/122660420-9ef58480-d13e-11eb-94f2-599c3a072873.mov)

[Later training](https://user-images.githubusercontent.com/45083086/122678262-46a49e00-d1a3-11eb-8fb9-fb6cfe130a23.mov)


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
