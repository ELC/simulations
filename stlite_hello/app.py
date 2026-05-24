import streamlit as st

from .charts import WaveChartParams, build_sine_wave_chart, wave_dataframe


def main() -> None:
    st.set_page_config(page_title="Stlite Hello World", layout="wide")
    st.title("Hello, Stlite!")
    st.caption("A static Streamlit app powered by @stlite/browser and Altair.")

    name = st.text_input("Your name", value="world")
    waves = st.slider("Wave cycles", min_value=1, max_value=10, value=3)
    amplitude = st.slider("Amplitude", min_value=0.1, max_value=2.0, value=1.0)

    st.write(f"Hello, **{name}**! Move the sliders to redraw the chart.")

    params = WaveChartParams(waves=waves, amplitude=amplitude)
    wave_data = wave_dataframe(params)
    chart = build_sine_wave_chart(wave_data, params=params)
    st.altair_chart(chart, width="stretch")


if __name__ == "__main__":
    main()
