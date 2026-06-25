#!/usr/bin/env python3

from common import format_tour, read_input

import solver_opt

CHALLENGES = 8

def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = solver_opt.solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')
        print(f'input {i} done')


if __name__ == '__main__':
    generate_sample_output()
