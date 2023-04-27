# one_pizza

Here is the [link](https://codingcompetitions.withgoogle.com/hashcode/round/00000000008f5ca9/00000000008f6f33) to the problem. It comes from the Google Hash Code 2022.

The data I used is in the *data* folder and the solutions are written in subfolders of the *solutions* folder wich will be created when you run the code.

I used several approaches to solve it, to experiment with different algorithms and to compare the results. All the results given are for the *data/d_difficile.txt* file.

## The scoring function

The scoring function is the same for all the approaches. It is the number of clients satistified by the recipe as described in the problem statement.

It is very long to compute for large instances of the problem since you need to go through the whole recipe for each client to ensure that it contains all their liked ingredients and none of their disliked ingredients.

## Different approaches

Here is a summary of the different approaches I used to solve the problem.
  - [Explicit search](#explicit-search)
  - [Genetic](#genetic)
  - [Simulated annealing](#simulated-annealing)
  - [Tabu search](#tabu-search)
  - [Greedy algorithm](#greedy-algorithm)

For each approach, you need to provide the path to the data file corresponding to the problem you want to solve.

For genetic, simulated annealing and tabu search, the results are written in a file during the execution of the algorithm and can be visualized with the *plot_results* function. You can start these algorithms with a given solution to continue the search from this solution otherwise a random solution is generated.


### Explicit search

This is the most basic approach. It consists in trying all the possible combinations of pizzas to find the best one. It is very slow and can only be used for small instances of the problem.

### Genetic

This approach is based on the genetic algorithm. It consists in creating a population of solutions and then to evolve it to find the best solution. The evolution is done by selecting the best solutions, crossing them and mutating them to generate the next generation.

The selection is done either by selecting the top 50% of the population or by tournament which ensures that the best recipe is selected but adds randomness and variety to the population.

The crossover is done by creating a pivot point in the middle of the list of ingredients and then swapping the recipes before and after the pivot. 

The mutation is done by randomly toggling the presence of an ingredient in a recipe.

You can modify the size of the population and the mutation rate and choose between the different selection methods.
The algorithm stops after a given number of generations or if the best solution has reached the objective score given by the user.

Here are the results I got for different values of the mutation rate. The population size is 100 and the number of generations is 300. The selection method is elitism which means that the top 50% of the population is selected.

| **Mutation rate** | **Score** |
|:-----------------:|:---------:|
| 0.05              | 1552      |
| 0.01              | 1663      |
| 0.001             | 1749      |
| 0.0005            | 1730      |

A mutation rate around 0.001 seems to be the best choice for this instance of the problem. It has 600 ingredients so such mutation rates correspond to less than 1 ingredient being mutated on average. It allows the algorithm to explore the search space without making too many changes at once.

The plots below show the evolution of the best solution for both selection methods for a mutation rate of 0.001 and 1000 generations. Both gave a best score of around 1730 and seem to have a similar evolution.

<img src="https://user-images.githubusercontent.com/96493391/234731423-78a76a27-d36d-492f-9d32-b094224ab127.png" width="750" height="200">

### Simulated annealing

This approach is based on the simulated annealing algorithm. It consists in creating a solution and then to modify it to find the best solution. The modification is done by randomly adding or removing an ingredient from a recipe.

It starts with a given temperature and then decreases it at each iteration at a given rate. The temperature is used to decide whether to keep the new solution or not. The higher the temperature, the more likely it is to keep a solution that is worse than the current one. This allows the algorithm to escape local minima.

You can modify the initial temperature, the temperature decrease rate. The algorithm stops after a given number of iterations or if the best solution has reached the objective score given by the user.

Here are the results I got for different values of the temperature and the temperature decrease rate. The number of iterations is 1000.

|                 | **T = 100** | **T = 50** | **T = 20** | **T = 10** | **T = 5** | **T = 2** | **T = 1** |
|:---------------:|:-----------:|:----------:|:----------:|:----------:|:---------:|:---------:|:---------:|
| **Rate = 0.99** | 1610        | 1617       | 1657       | 1646       | 1691      | 1675      | 1657      |
| **Rate = 0.95** | 1658        | 1671       | 1648       | 1675       | 1673      | 1649      | 1655      |
| **Rate = 0.90** | 1664        | 1672       | 1677       | 1653       | 1671      | 1676      | 1656      |
| **Rate = 0.80** | 1664        | 1656       | 1669       | 1698       | 1669      | 1654      | 1668      |

We can see that a temperatures of 10 to 20 with high decrease rate or a temperature of 5 to 10 with a low decrease rate give the best results.

As shown in the plots below, a decrease rate of 0.99 with too high temperatures is suboptimal because worse solutions are kept too often and the best solution stagnates for a while.

<img src="https://user-images.githubusercontent.com/96493391/234730967-ac48e4ed-27bf-4fd6-8438-6e9d330c23f6.png" width="660" height="550">

### Tabu search

This approach is based on the tabu search algorithm. It consists in creating a solution and then going through its neighborhood to find the best solution. The neighborhood is created by toggling the presence of an ingredient in a recipe.

It keeps a list of the last solutions and prevents the algorithm from going back to these solutions. This allows the algorithm to escape local minima.

You can modify the size of the tabu list. The algorithm stops after a given number of iterations or if the best solution has reached the objective score given by the user.

I didn't find any heuristic to select only few neighbors to explore that would give better results than exploring all the neighbors. Since the neighborhood is very large, it is very slow to compute the score of all the neighbors at each iteration. 

It reached a score of 1769 in 200 iterations which took several hours.

Maybe only allowing to toggle the most promising ingredients would help reducing the size of the neighborhood. I might try to implement this in the future.

### Greedy algorithm

This approach is based on the greedy algorithm.

It consists it iteratingly adding to the recipe the ingredient that will increase the score the most. It stops when the score cannot be increased anymore.

It is very slow too since it needs to compute the score of all the possible ingredients to add to the recipe at each iteration.

This approach reaches a score of 1764.
