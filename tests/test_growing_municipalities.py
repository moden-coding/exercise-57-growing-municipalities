#!/usr/bin/env python3

import contextlib
import io
import unittest
from unittest.mock import patch

import pandas as pd

from src.growing_municipalities import growing_municipalities, main


class TestGrowingMunicipalities(unittest.TestCase):

    def setUp(self):
        self.df = pd.read_csv("src/municipal.tsv", index_col=0, sep="\t")
        self.df = self.df["Akaa":"Äänekoski"]
        self.c = "Population change from the previous year, %"

    def test_all(self):
        result = growing_municipalities(self.df)
        self.assertAlmostEqual(
            result,
            0.228296,
            places=4,
            msg="growing_municipalities(df) on the full data set should be "
            "about 0.228296 (22.8%% of municipalities grew). Got %r." % (
                result,
            ),
        )

    def test_growing(self):
        m = self.df[self.c] > 0.0
        result = growing_municipalities(self.df[m])
        self.assertAlmostEqual(
            result,
            1.0,
            places=4,
            msg="growing_municipalities(df) restricted to only municipalities "
            "with positive population change should be 1.0: every row in "
            "that subset is growing. Got %r." % (result,),
        )

    def test_not_growing(self):
        m = self.df[self.c] <= 0.0
        result = growing_municipalities(self.df[m])
        self.assertAlmostEqual(
            result,
            0.0,
            places=4,
            msg="growing_municipalities(df) restricted to only municipalities "
            "with zero or negative population change should be 0.0: none of "
            "those rows are growing. Got %r." % (result,),
        )

    def test_call(self):
        with patch(
            "src.growing_municipalities.growing_municipalities",
            wraps=growing_municipalities,
        ) as pgm:
            main()
            pgm.assert_called()

    def test_output(self):
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            main()
        out = buf.getvalue().strip()
        pattern = r"Proportion of growing municipalities: \d+\.\d%"
        self.assertRegex(
            out,
            pattern,
            msg="main() should print something matching "
            "'Proportion of growing municipalities: <number>%%' with one "
            "decimal place. Printed: %r." % (out,),
        )


if __name__ == "__main__":
    unittest.main()
