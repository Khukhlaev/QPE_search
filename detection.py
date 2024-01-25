import numpy as np
import scipy.signal

# Very early draft of detection algorithm


def check_max_val(counts: np.ndarray, n: float = 2.5) -> bool:
    # TODO: maybe add something about errors? For. ex (counts[argmax(counts)] + err[argmax(counts)]) / ...
    return np.max(counts) / np.mean(counts) > n


def find_top_points(counts: np.ndarray, n: float = 2.5) -> np.ndarray:
    # TODO: do something with distance between peaks, they should be quite far away from each other
    # TODO: think about widths also! check how scipy computes it
    return scipy.signal.find_peaks(counts, prominence=np.mean(counts) * n)[0]


def calculate_widths(counts: np.ndarray, peaks: np.ndarray) -> np.ndarray:
    return scipy.signal.peak_widths(counts, peaks, rel_height=0.9)[0]


def check_curve(counts: np.ndarray, dt: np.ndarray, errors: np.ndarray) -> bool:
    """
    Function to check if curve could correspond to QPE candidate in 3 steps:
    1. Check that max value of timeseries is >n times greater than the background (default n = 3)
    2. Find all peak points
    3. Calculate durations of all eruptions and compare them to existing limits (strange criteria maybe?)

    :return: True if source is QPE candidate, False otherwise
    """

    assert counts.shape[0] == dt.shape[0]
    assert dt.shape[0] == errors.shape[0]

    if not check_max_val(counts):
        return False

    peaks = find_top_points(counts)

    if not peaks.size:
        return False

    widths = calculate_widths(counts, peaks)

    widths_t = widths * (dt[1] - dt[0])

    # if np.min(widths_t) > 50000. or np.max(widths_t) < 1000.:
    #     return False

    return True


def main():
    pass


if __name__ == "__main__":
    main()
