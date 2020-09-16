
## N Queen's Problem using Genetic Algorithm

import random
import numpy as np

'''
Define function to generate random population for NxN chess board
For each combination, an array of length N is defined.
(position of element, value of element) = position of queen on board (row,column)
eg for a random chromosome {2,5,6,1,3,4,8,7}
= position of queen for 1st column is in 2nd row, 2nd column is 5th row and so on...
using such a denotation,
we eliminate the possibility of having more than one queens placed in a single column
'''
def Initialize_Population(size,N):
    
    population = []
    for i in range(size):
        for j in range(N):
            population.append(random.randrange(0,N))

    population = np.array(population)
    pop = np.split(population,size)
    return pop

'''
This function determines total possible clashes for a NxN chess board and N queens
As one column will have at the max one queen, so only row or diagonal clashes are possible
max clashes will occur when all queens are in the same row or same diagonal
'''
def total_possible_clashes(a):
    a = a-1
    tot = 0
    while (a != 0):
        tot = tot + a
        a = a-1
    return tot

'''
find row clashes and diagonal clashes
total clashes = row clashes + diagonal clashes
determine fitness = (max possible clashes - total clashes for a certain combination)
So Goal is to maximize fitness (or minimize the number of clashes)
take care, not to consider any clash twice
(clash btwn queen 1 and 3 is same as clash between queen 3 and 1)
'''
def fitness(population,N):
    tot_clashes = total_possible_clashes(N)
    #print('Total possible clashes = ',tot_clashes)
    fits = []
    for i in range(len(population)):
        row_clashes = 0
        diag_clashes = 0
        for j in range(N):
            for k in range(j+1,N):
                if (population[i][j] == population[i][k]):
                    row_clashes = row_clashes + 1
                dx = abs(j-k)
                dy = abs(population[i][j] - population[i][k])
                if (dx == dy):
                    diag_clashes = diag_clashes + 1
        #print('Total row clashes = ',row_clashes)
        #print('Total diagonal clashes = ',diag_clashes)
        clashes = row_clashes + diag_clashes
        f = tot_clashes - clashes
        #print('Fitness = ',f,'\n')
        fits.append(f)
    return fits

'''
Define function to calculate probability
It is calculated as (fitness of a chromosome)/(total fitness sum of whole population)
'''
def probability(f):
    total = sum(f)
    f_update = []
    for i in f:
        f_update.append(i/total)
    return (f_update)

'''
Define function to calculate cumulative probabilities
'''
def cumulative_prob(f):
    cp = []
    for i in range(len(f)):
        cp.append(sum(f[:i+1]))
    return (cp)

'''
Define a function for selection of parents for mating
Selection is done according to roulette wheel selesction 
'''
def selection(population,cp):
    new_population = []
    for i in range(len(population)):
        a = random.random()
        #print(a)
        for j in cp:
            if (a <= j):
                x = cp.index(j)
                break
        new_population.append(population[x])
    return (new_population)

'''
Define a function to perform crossover between 2 chromosomes
Here we perform single-point crossover
'''
def crossover(population,N):
    offspring = []
    i = 0
    while (i != len(population)):
        a = random.randrange(0,N)
        #print(a)
        offspring.append(np.concatenate((population[i][:a],population[i+1][a:])))
        offspring.append(np.concatenate((population[i+1][:a],population[i][a:])))
        i = i+2
    return(offspring)

'''
Define a function to perform mutation
If a randomly generated number is greater than 0.95, only then mutation is performed
'''
def mutation(population,N):
    for i in range(len(population)):
        a = random.random()
        if (a > 0.95):
            c = random.randrange(0,N)
            population[i][c] = random.randrange(0,N)
    return (population)

'''
We define a terminating condition
If the fitness of any chromosome in a population is equal to
total possible clashes (ie for that combinitation, there are no clashes occuring)
then it is the soultion, else we continue with the crossover and mutation
'''
def terminate_condition(f,N):
    desired_fitness = total_possible_clashes(N)
    x = []
    for i in f:
        if (i == desired_fitness):
            x.append(f.index(i))
    return (x)
            
init_pop = 500
N = 8
iterations = 10
'''
1.Random population is generated for given size,
2.corresponding fitness for each chromosome is calculated
3.probabilities of fitness are used for parent selection
4.ternimating condition is checked, if it doesn't match,
5.then cossover and mutation is performed to give new set of offsprings
6.and this is continued till we get a solution.
All the above points are repeated for given number of iterations
and solution corresponding to each iteration is printed
'''
for k in range(iterations):
    x = Initialize_Population(init_pop,N)
    #print('Initial population is = ',x,'\n')
    fit = fitness(x,N)
    #print('Fitness of initial population is = ',fit,'\n')

    a = terminate_condition(fit,N)
    #print(a)
    while (len(a) == 0):
        p = probability(fit)
        #print('Percentage fitness = ',p,'\n')
        cum_p = cumulative_prob(p)
        #print('Cumulative fitness = ',cum_p,'\n')
        x = selection(x,cum_p)
        #print('\nNew population = ',x,'\n')
        x = crossover(x,N)
        #print('\nNew offsprings after crossover = ',x,'\n')
        x = mutation(x,N)
        #print('Offspring after mutation = ',x,'\n')
        fit = fitness(x,N)
        #print('Fitness = ',fit,'\n')
        a = terminate_condition(fit,N)
        #print(a)
    if (len(a) != 0):
        solution = []
        for i in a:
            solution.append(x[i])

    print(solution)

