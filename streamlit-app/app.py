import streamlit as st
import pandas as pd
import numpy
from elasticsearch import Elasticsearch
import json
 
 
# Set up the application

st.set_page_config(
    page_title="DKP Big Data Demo",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Set up our es instance:
es = Elasticsearch(["https://elastic-es-default:9200"], basic_auth=('elastic', 'elastic'), verify_certs=False)

def count_records():
    try:
        count = "{:,}".format(es.count(index="newsitems")['count'])
    except:
        count = 0
    return count

def aggregate_countries():
    query = {"size":0,"aggs":{"countries":{"terms":{"field":"sourcecountry.keyword","size":25}}}}
    aggregate = es.search(body=query, index="newsitems")['aggregations']['countries']['buckets']
    df = pd.DataFrame.from_dict(aggregate)
    df = df.rename(columns={"key": "Country", "doc_count": "Number of Articles"})
    for row in df.index:
        if len(df.loc[row, "Country"]) < 2 or df.loc[row, "Country"] == "United States":
            df.drop(row, inplace=True)
    return df


# Page layout
col1, col2, col3 = st.columns([1,8, 1])
with col1:
    st.text("")
    st.text("")
    st.image("https://docs.d2iq.com/~assets-5a76a465-a273-4642-8096-e925db8ea38d/image/D2IQ_Logotype_Color_Positive.png", width=100)
    
with col2:
    st.title('Tech News Data Analyser')
    st.text(f"There are currently {count_records()} articles in the search engine.")

st.markdown("""---""")    
try:    
    st.bar_chart(data=aggregate_countries(), x="Country", y="Number of Articles", height=400, use_container_width=False, width=800)
except:
    st.text("There is no data in Elastic yet. Add some data")

st.markdown("""---""")

col1, col2 = st.columns([1, 1])

with st.sidebar:
    with st.form("search"):
        st.write("Search News Articles")
        search_term = st.text_input("Search Term")
        submitted = st.form_submit_button("Submit")