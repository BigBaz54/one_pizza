# one_pizza

Here is the [link](https://codingcompetitions.withgoogle.com/hashcode/round/00000000008f5ca9/00000000008f6f33) to the problem. It comes from the Google Hash Code 2022.

The data I used is in the *data* folder and the solutions are written in subfolders of the *solutions* folder wich will be created when you run the code.

I used several approaches to solve it, to experiment with different algorithms and to compare the results.

## Different approaches

Here is a summary of the different approaches I used to solve the problem.
- [**explicit search**](#explicit-search)
- [**genetic**](#genetic)
- [**simulated annealing**](#simulated-annealing)
- [**tabu search**](#tabu-search)
- [**greedy algorithm**](#greedy-algorithm)

For each approach, you need to provide the path to the data file corresponding to the problem you want to solve.

For genetic, simulated annealing and tabu search, the results are written in a file during the execution of the algorithm and can be visualized with the *plot_results* function.


### Explicit search

This is the most basic approach. It consists in trying all the possible combinations of pizzas to find the best one. It is very slow and can only be used for small instances of the problem.

### Genetic

This approach is based on the genetic algorithm. It consists in creating a population of solutions and then to evolve it to find the best solution. The evolution is done by selecting the best solutions, crossing them and mutating them to generate the next generation.

The selection is done either by selecting the top 50% of the population or by tournament which ensures that the best recipe is selected but adds randomness and variety to the population.

The crossover is done by creating a pivot point in the middle of the list of ingredients and then swapping the recipes before and after the pivot. 

The mutation is done by randomly toggling the presence of an ingredient in a recipe.

You can modify the size of the population and the mutation rate and choose between the different selection methods.
The algorithm stops after a given number of generations or if the best solution has reached the objective score given by the user.

image here




|                 | **T = 100** | **T = 50** | **T = 20** | **T = 10** | **T = 5** | **T = 2** | **T = 1** |
|:---------------:|:-----------:|:----------:|:----------:|:----------:|:---------:|:---------:|:---------:|
| **Rate = 0.99** | 1610        | 1617       | 1657       | 1646       | 1691      | 1675      | 1657      |
| **Rate = 0.95** | 1658        | 1671       | 1648       | 1675       | 1673      | 1649      | 1655      |
| **Rate = 0.90** | 1664        | 1672       | 1677       | 1653       | 1671      | 1676      | 1656      |
| **Rate = 0.80** | 1664        | 1656       | 1669       | 1698       | 1669      | 1654      | 1668      |
