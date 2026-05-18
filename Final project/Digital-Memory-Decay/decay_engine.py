from corruption_model import corruption_factor


def simulate_decay(
    initial_files,
    decay_rate,
    years
):

    retention = []

    for year in range(years + 1):

        corruption = corruption_factor()

        remaining = initial_files * (
            (1 - (decay_rate + corruption)) ** year
        )

        retention.append(remaining)

    return retention