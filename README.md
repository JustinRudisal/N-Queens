
# N-Queens Problem Solver

This project is an implementation of a genetic algorithm to solve the N-Queens problem. The algorithm efficiently finds solutions for large values of N (e.g., N=32) in just a few seconds.

## Features

- **Genetic Algorithm:** Utilizes a genetic algorithm to evolve solutions over generations.
- **Multithreading:** Optional multithreading to speed up fitness calculations.
- **Fitness Caching:** Caches fitness values to avoid recalculating known chromosomes' fitness.
- **Escape Mechanism:** Implements an escape mechanism to avoid local minima.
- **Adjustable Parameters:** Allows customization of population size, mutation probability, and other parameters.

## Requirements

- Python 3.6+
- `concurrent.futures` (included in Python 3.6+)

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JustinRudisal/nqueens-solver.git
   cd nqueens-solver
   ```

2. **Run the script:**

   ```bash
   python nqueens_solver.py
   ```

3. **Enter the number of queens:**

   When prompted, enter the number of queens (e.g., 32):

   ```
   Enter Number of Queens: 32
   ```

4. **View the output:**

   The script will display the runtime, number of generations, and a visual representation of one of the solutions.

## Code Overview

- **random_chromosome:** Generates a random chromosome (board configuration).
- **calculate_fitnesses:** Calculates fitness values for a list of chromosomes.
- **fitness:** Calculates the fitness of a single chromosome.
- **probability:** Calculates the selection probability of a chromosome.
- **random_pick:** Selects a chromosome based on its selection probability.
- **reproduce:** Performs crossover between two chromosomes.
- **mutate:** Mutates a chromosome to introduce diversity.
- **calculate_parameters:** Adjusts mutation probability and escape parameters.
- **genetic_queen:** Executes the genetic algorithm to evolve the population towards a solution.
- **print_board:** Prints the chessboard with queens placed.

## Customization

You can customize various parameters in the script to suit your needs:

- **POPULATION_AMOUNT:** Number of chromosomes in the population.
- **MULTITHREADING:** Set to `True` to enable multithreading.
- **BASE_MUTATION_PROBABILITY:** Base probability of mutation.
- **MAX_MUTATION_PROBABILITY:** Maximum probability of mutation.
- **AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING:** Number of chromosomes to randomize when escaping local minima.
- **ESCAPE_EVERY_X_GENERATIONS:** Frequency of escape attempts.
- **PRINT_CHROMOSOMES, PRINT_GENERATIONS, PRINT_ESCAPE_INDICATOR:** Debugging flags to print additional information.

## Example

Here is an example of running the script for N=8:

```plaintext
Enter Number of Queens: 8

---------------------------------------------
Maximum fitness = 28

Solved in Generation 40!
One of the solutions:
Chromosome = [1, 5, 8, 6, 3, 7, 2, 4],  Fitness = 28

x x x x Q x x x
Q x x x x x x x
x x x x x Q x x
x x x Q x x x x
x Q x x x x x x
x x x x x x Q x
x x Q x x x x x
x x x x x x x Q

Total runtime: 0.65 seconds

---------------------------------
Average Runtime over 5 runs: 0.65 seconds
```

## Acknowledgments

- This project was created as part of an artificial intelligence class at Florida Atlantic University.
