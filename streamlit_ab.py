import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###


@st.cache_data
def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###


st.write("Age-specific cancer mortality rates")

# min_year = df['Year'].min().astype(int)
# max_year = df['Year'].max().astype(int)
#int()
year = 2012

select_year = st.slider("Year", min_value= 1994, max_value= 2020, value=year, step=1)

subset = df[df["Year"] == select_year]

### P2.2 ###
# replace with st.radio
sex = "M"

select_gender = st.radio ('Sex', ('M', 'F'))
subset = subset[subset["Sex"] == select_gender]

### P2.3 ###

# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]

select_country = st.multiselect('Countries', options=countries, default=countries)

subset = subset[subset["Country"].isin(select_country)]


### P2.4 ###
# replace with st.selectbox

cancer = "Malignant neoplasm of stomach"
in_stomach = df['Cancer'].unique().tolist().index(cancer)
#in_stomach = [pd.unique(df['Cancer'])== cancer]

dd_selectbox_cancer = st.selectbox(
    'Cancer', df['Cancer'].unique(), index=in_stomach)

subset = subset[subset["Cancer"] == dd_selectbox_cancer]


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age:O", sort=ages),
    y=alt.Y("Country:N"),
    color=alt.Color("Rate:Q", title="Mortality rate per 100k", scale=alt.Scale(type='log', domain=(0.01, 1000), clamp=True)),
    tooltip=["Rate:Q"],
).properties(
    title=f"{dd_selectbox_cancer} mortality rates for {'males' if select_gender == 'M' else 'females'} in {select_year}",
)
### P2.5 ###


st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")

