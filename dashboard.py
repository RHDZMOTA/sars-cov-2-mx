import datetime as dt

import pandas as pd


import altair as alt
import streamlit as st

from sars_cov_2_mx.dataset import get_latest_snapshot
from sars_cov_2_mx.settings import get_logger

logger = get_logger(name=__name__)


@st.cache
def get_latest_reliable_date() -> str:
    return (dt.datetime.utcnow() - dt.timedelta(days=7)) \
        .strftime("%Y-%m-%d")


@st.cache
def get_raw_data() -> pd.DataFrame:
    return get_latest_snapshot()


@st.cache
def get_data() -> pd.DataFrame:
    df_raw = get_raw_data()
    df_parsed = df_raw.query("""nombre == '"JALISCO"'""").melt(["cve_ent", "poblacion", "nombre"])[
        ["variable", "value"]]
    latest_reliable_date = get_latest_reliable_date()
    return (
        df_parsed
        # Fix data types
        .assign(
            value=lambda df: df.value.astype(int),
            variable=lambda df: pd.to_datetime(df.variable, dayfirst=True)
        )
        .sort_values("variable", ascending=True)
        # Filter relevant time period
        .query(f"'2021-01-01' < variable <= {repr(latest_reliable_date)}")
        # Add weeks segments
        .apply(
            lambda row: pd.Series(
                {
                    "week": "-".join(str(elm) for elm in row["variable"].isocalendar()[:-1]),
                    **row.to_dict()
                }
            ),
            axis=1
        )
        # Rolling average
        .assign(
            ma_short=lambda df:
                df.value.rolling(7, min_periods=7).mean(),
            ma_long=lambda df:
                df.value.rolling(21, min_periods=21).mean(),
        )
    )


def get_chart(df: pd.DataFrame):
    # Chart source
    source = (
        df
            .dropna()
            .rename(
            columns={
                "variable": "date",
                "value": "current_cases"
            }
        )
            .drop(columns=["week"])
            .melt(["date"])
    )
    # Chart Axis
    x_axis = alt.X("date", title="Date")
    y_axis = alt.Y("value", title="Number of Cases", scale=alt.Scale(zero=False))
    # Line Chart
    return alt.Chart(source).mark_line()\
        .encode(x_axis, y_axis, color="variable")\
        .properties(title="Jalisco MX")


def main():
    df = get_data()
    line_chart = get_chart(df=df)
    st.title("Sars-Cov-2: New Cases")
    st.altair_chart(line_chart, use_container_width=True)


if __name__ == "__main__":
    main()
