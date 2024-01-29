import numpy as np

from detection import check_curve
from curve_generation import CurvesGenerator


def test_detection(n: int, max_val: float, prominence: float):
    gen = CurvesGenerator(0.3)

    test_samples = gen.generate_chunk(n)

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for sample in test_samples:
        predict = check_curve(sample[0], sample[1], np.zeros_like(sample[0]), max_val, prominence)

        if predict:
            if sample[2]:
                true_positive += 1
            else:
                false_positive += 1

        else:
            if sample[2]:
                false_negative += 1
            else:
                true_negative += 1

    assert (true_positive + true_negative + false_positive + false_negative) == n

    return true_positive, true_negative, false_positive, false_negative
