from end_to_end import end_to_end


def main():
    # Set parameters
    birth_number = 100
    release_number = 500
    number_infected_before_release = 200

    print('Running simulation ...')
    t, S, I, R, D = end_to_end(birth_number, release_number, number_infected_before_release, rho=0.0003,
                               death_rate=0.012, tau=0.03, gamma=1.0, max_time=10, N=3000, p=0.02,
                               percent_infected=0.0035, percent_recovered=0.0015)
    print('Simulation complete.')

    print('Commencing tests ...')
    test_death_rate_is_strictly_increasing(D)
    print('Testing completed.')

    print('Program ending.')


def test_death_rate_is_strictly_increasing(D):
    print('test_death_rate_is_strictly_increasing:', end=' ')
    for i in range(len(D) - 1):
        if D[i] > D[i + 1]:
            print('Failed')
            return
    print('Passed')


if __name__ == "__main__":
    main()
