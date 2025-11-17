import streamlit as st
import pandas as pd
from src.data_validation import DataValidator

st.title("Data Integration & Analytics Hub (DIAH)")

uploaded_file = st.file_uploader("Upload data for validation", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    validator = DataValidator(df)
    results = validator.run_all_validations(numeric_cols=["amount"])

    st.subheader("Validation Results")
    st.write(results)

    if any([results["null_values"], results["duplicates"], results["negative_values"]]):
        st.error("Validation failed. Please fix the data issues before loading.")
    else:
        st.success("All validation checks passed!")
