from ..mindex_bengals import remove_bad_weeks
import pandas as pd


def test_remove_bad_weeks():
    d = {"Week": ["REG6", "REG7", "REG8", "REG9", "REG10", "REG11"]}

    df = remove_bad_weeks(pd.DataFrame(d))

    assert "REG10" not in df["Week"]
