import pandas as pd
from typing import List


def neyman_alloc(
    sample_size: int,
    strata_name: List[str],
    strata_ac: List[float],
    strata_std: List[float],
) -> dict[str, int]:
    """
    Implements Neyman allocation for stratified random sampling.
    """
    # Calculate the proportion of the strata
    strata_prop = [ac / sum(strata_ac) for ac in strata_ac]
    # Calculate the variance of the sample
    sample_var = sum([var * prop for var, prop in zip(strata_std, strata_prop)])
    # Calculate the optimal allocation
    alloc = {
        strata: round(prop * sample_size * std / sample_var)
        for strata, prop, std in zip(strata_name, strata_prop, strata_std)
    }
    # Return the optimal allocation
    return alloc


import unittest


class TestNeymanAlloc(unittest.TestCase):
    def test_neyman_alloc(self):
        sample_size = 150
        strata_name = ["1", "2", "3", "4", "5"]
        strata_ac = [15, 45, 110, 60, 70.0]
        strata_std = [20, 70, 35, 45, 25.0]
        alloc = neyman_alloc(sample_size, strata_name, strata_ac, strata_std)
        self.assertEqual(alloc["1"], 4)
        self.assertEqual(alloc["2"], 40)
        self.assertEqual(alloc["3"], 49)
        self.assertEqual(alloc["4"], 35)
        self.assertEqual(alloc["5"], 22)


if __name__ == "__main__":
    unittest.main()
