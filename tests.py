from end_to_end import end_to_end


def main():
    # Set parameters
    release_number = 500
    number_infected_before_release = 200
    stop_inflow_at_intervention = True

    print('Running simulation ...')
    t, S, I, R, D = end_to_end(release_number, number_infected_before_release, stop_inflow_at_intervention)
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
