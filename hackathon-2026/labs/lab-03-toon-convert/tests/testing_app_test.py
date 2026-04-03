import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import requests
import os
import plotly.express as px

st.set_page_config(
    page_title="AI Dataset Analyzer",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
#till here

st.set_page_config(page_title="Dataset Analyzer", layout="wide")

st.title("Dataset Quality Analyzer")

# ------------------ AI FUNCTION (OPENROUTER) ------------------

def get_ai_suggestions(missing, duplicates, score):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "API key not found. Please set OPENROUTER_API_KEY."

    prompt = f"""
    You are a data scientist.

    Analyze the dataset issues:
    - Missing values: {missing}
    - Duplicate rows: {duplicates}
    - Data quality score: {score}

    Explain problems clearly and suggest improvements in simple terms.
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",   # REQUIRED sometimes
            "X-Title": "Dataset Analyzer Project"      # REQUIRED sometimes
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"
# ------------------ FILE UPLOAD ------------------

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:

    # ----------- SMART FILE LOADING -----------

    try:
        uploaded_file.seek(0)
        sample = uploaded_file.read(1024).decode("utf-8")

        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter

        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, delimiter=delimiter)

        st.success("Dataset loaded successfully!")

    except Exception:
        st.error("⚠️ Error loading dataset. Attempting to fix...")

        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, on_bad_lines='skip')

        st.warning("⚠️ Some rows were skipped due to formatting issues.")

    # ----------- PREVIEW -----------

    st.subheader("Dataset Preview")
    st.write(df.head())

    # ----------- DATA QUALITY -----------

    st.subheader("Data Quality Analysis")

    missing = df.isnull().sum()
    duplicate_rows = df.duplicated().sum()

    st.write("### Missing Values")
    st.write(missing)

    st.write("### Duplicate Rows")
    st.write(duplicate_rows)

    st.write("### Statistical Summary")
    st.write(df.describe())
#edited
#	col1, col2, col3 = st.columns(3)

 #   col1.metric("Missing Values", int(missing_cells))
  #  col2.metric("Duplicate Rows", int(duplicate_rows))
   # col3.metric("Quality Score", f"{score:.2f}")
#till here
    # ----------- VISUALIZATION -----------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Missing Values Analysis")

        missing = df.isnull().sum()
        missing = missing[missing > 0]  # only columns with missing values

        if not missing.empty:

            fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={'x': 'Columns', 'y': 'Number of Missing Values'},
            title="Missing Values per Column",
            height=350
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.success("No missing values found in dataset")
    with col2:
        st.subheader("Data Distribution")

        numeric_cols = df.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:

            selected_col = st.selectbox("Select column for distribution", numeric_cols)

            fig = px.histogram(
            df,
            x=selected_col,
            nbins=30,
            title=f"Distribution of {selected_col}",
            labels={selected_col: "Values"},
            height=350
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns available for distribution")
	    
	# ----------- SCORE -----------

    total_cells = df.size
    missing_cells = df.isnull().sum().sum()

    score = 100 - ((missing_cells / total_cells) * 50 + (duplicate_rows / len(df)) * 50)

    st.subheader("Data Quality Score")
    st.write(f"{score:.2f} / 100")

   
    # ----------- AI INSIGHTS -----------

    st.subheader("🤖 AI Insights")

    with st.spinner("Analyzing with AI..."):
        ai_output = get_ai_suggestions(missing_cells, duplicate_rows, score)

    st.write(ai_output)

    # ----------- AUTO CLEAN -----------
    st.subheader("Auto Clean Dataset")

    if st.button("Clean Dataset"):

        cleaned_df = df.copy()

        cleaned_df.replace(["", "NA", "null"], pd.NA, inplace=True)

        for col in cleaned_df.columns:

            converted_col = pd.to_numeric(cleaned_df[col], errors='coerce')

            if converted_col.notna().sum() > 0.5 * len(cleaned_df):
                cleaned_df[col] = converted_col
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
            else:
                if not cleaned_df[col].mode().empty:
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                else:
                    cleaned_df[col].fillna("Unknown", inplace=True)

        cleaned_df.drop_duplicates(inplace=True)

        st.success("Dataset cleaned successfully!")

        st.write(cleaned_df.head())

        # ✅ KEEP DOWNLOAD HERE (IMPORTANT)
        csv_file = cleaned_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Cleaned Dataset",
            data=csv_file,
            file_name='cleaned_dataset.csv',
            mime='text/csv',
        )

    # ----------- CLASS IMBALANCE -----------

    st.subheader("Class Imbalance Check")

    for col in df.columns:
        if df[col].nunique() < 10:
            st.write(f"Column: {col}")
            st.write(df[col].value_counts())
    
#-----------bias detection code-------------

    st.subheader("Bias Detection")

    bias_report = []   # ✅ DEFINE HERE
    bias_found = False

    for col in df.columns:

        if df[col].nunique() < 10:

            value_counts = df[col].value_counts(normalize=True)

            max_ratio = value_counts.max()
            min_ratio = value_counts.min()

            imbalance_ratio = max_ratio / min_ratio if min_ratio > 0 else float('inf')

            if imbalance_ratio > 1.5:

                bias_found = True

                st.write(f"### Column: {col}")

                fig = px.bar(
                    x=value_counts.index.astype(str),
                    y=value_counts.values,
                    labels={'x': col, 'y': 'Proportion'},
                    title=f"Distribution of {col}",
                    height=350
                )

                st.plotly_chart(fig, use_container_width=True)

            # ✅ ADD TO REPORT
                bias_report.append(f"{col} is imbalanced (ratio: {imbalance_ratio:.2f})")

                if imbalance_ratio > 3:
                    st.error(f"⚠️ High bias detected in {col}")
                else:
                    st.warning(f"⚠️ Moderate imbalance in {col}")

        # AFTER LOOP
        if not bias_found:
            st.success("No significant bias detected")
#---------AI bias explanation-------------

    st.subheader("🤖 AI Bias Insights")

    if bias_report:

        bias_prompt = f"""
        The dataset has the following bias issues:
        {bias_report}

        Explain:
        - Why this is a problem
        - How it affects machine learning models
        - How to fix it
        """

        with st.spinner("Analyzing bias with AI..."):
            bias_ai = get_ai_suggestions(len(bias_report), 0, score)

        st.write(bias_ai)

    else:
        st.write("No major bias detected in dataset.")
