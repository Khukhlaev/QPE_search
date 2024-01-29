import numpy as np


def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)


# Class for single curve generation
class LightCurveGenerator:
    def __init__(self, noise_std_coef: float, dt: float):
        # TODO: maybe need to add more params?
        self.noise_std_coef = noise_std_coef
        self.dt = dt

    def _generate_linear(self, width: float, height: float) -> np.ndarray:
        signal = np.zeros(int(width / self.dt))
        middle = signal.size // 2
        coef = height / middle

        signal[0:middle] = np.array([coef * i for i in range(middle)])
        signal[middle:] = np.array([coef * (signal.size - i) for i in range(middle, signal.size)])

        return signal

    def _generate_quadratic(self, width: float, height: float) -> np.ndarray:
        signal = np.zeros(int(width / self.dt))
        middle = signal.size // 2
        coef = height / middle ** 2

        signal[0:middle] = np.array([coef * i ** 2 for i in range(middle)])
        signal[middle:] = np.array([coef * (signal.size - i) ** 2 for i in range(middle, signal.size)])

        return signal

    def _generate_qpe(self, width: float, height: float, mode: str) -> np.ndarray:
        assert mode in ["linear", "quadratic"]

        if mode == "linear":
            return self._generate_linear(width, height)

        if mode == "quadratic":
            return self._generate_quadratic(width, height)

    def generate(self, noise_level: float, signal_time: float, params: dict) -> (np.ndarray, np.ndarray):
        times = np.arange(0, signal_time, self.dt)

        # Maybe Poisson noise is needed?
        noise = np.random.normal(noise_level, self.noise_std_coef * noise_level, len(times))
        noise = np.abs(noise)

        if len(params) == 0:  # There are no sources
            return noise, times

        signal = np.zeros_like(noise)

        for i in range(params["number QPEs"]):
            qpe_params = params[f"QPE {i + 1}"]

            width = qpe_params["width"]
            height = qpe_params["height"]
            start = int(qpe_params["start"] / self.dt)
            end = start + int(width / self.dt)

            # Mode is quadratic by default
            mode = "quadratic" if qpe_params.get("mode", None) is None else qpe_params.get("mode")

            signal[start:end] = self._generate_qpe(width, height, mode)

        return noise + signal, times


# Class for multiple curves generation
class CurvesGenerator:
    def __init__(self, noise_std_coef: float):
        self.num_qpe_weights = np.array([10, 4, 3, 2, 1])  # Weight 10 for 0 QPEs, 4 for 1 QPE, etc.
        self.dt = 500
        self.curve_gen = LightCurveGenerator(noise_std_coef, self.dt)

    def _generate_params(self) -> (dict, float, float):
        """
        Here some parameters can (and should!) be tweaked
        """

        noise_level = np.random.uniform(0.01, 0.2)
        signal_time = round_to_multiple(np.random.randint(40000, 100000), self.dt)

        number_QPEs = int(np.random.choice(np.arange(len(self.num_qpe_weights)),
                                           p=self.num_qpe_weights / np.sum(self.num_qpe_weights)))

        params = {"number QPEs": number_QPEs}

        starts = [round_to_multiple(signal_time * (i + 1) / (number_QPEs + 1), self.dt) for i in range(number_QPEs)]

        for i in range(number_QPEs):
            params[f"QPE {i + 1}"] = {"start": starts[i], "width": self.dt * np.random.randint(6, 12),
                                      "height": noise_level * np.random.uniform(2.5, 4),
                                      "mode": "quadratic"}

        return params, signal_time, noise_level

    def _generate_curve(self) -> (np.ndarray, np.ndarray, bool):
        params, signal_time, noise_level = self._generate_params()
        qpe_presence = True if params["number QPEs"] > 0 else False

        counts, times = self.curve_gen.generate(noise_level, signal_time, params)

        return counts, times, qpe_presence

    def generate_chunk(self, n: int):
        curves = [self._generate_curve() for _ in range(n)]

        return curves
