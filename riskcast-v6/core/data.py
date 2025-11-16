import streamlit as st
import pandas as pd
import os

class DataService:
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_historical_data() -> pd.DataFrame:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "historical_climate.csv")
        return pd.read_csv(data_path)

    @staticmethod
    @st.cache_data
    def get_company_data() -> pd.DataFrame:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "company_data.csv")
        return pd.read_csv(data_path).set_index("Company")