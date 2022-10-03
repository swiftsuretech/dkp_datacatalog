from cgi import test
import streamlit as st
import pandas as pd
import numpy
from elasticsearch import Elasticsearch
import json
from datetime import datetime
from IPython.core.display import HTML, Image

# Set envt to test or demo
envt = ""
if envt == "test":
    endpoint = "https://a06df877875674d6c8518d5cfe46cbcb-231150320.us-west-2.elb.amazonaws.com:443/elastic/"
else:
    endpoint = "https://elastic-es-default:9200"
pd.set_option('display.max_columns', None)
search_query = None
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
es = Elasticsearch([endpoint], basic_auth=('elastic', 'elastic'), verify_certs=False)

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

def latest_articles(query):
    if query:
        latest = es.search(index="newsitems", size=10, sort="seendate:desc", query=query)['hits']['hits']
    else:
        latest = es.search(index="newsitems", size=10, sort="seendate:desc")['hits']['hits']
    stripped = []
    for news in latest:
        stripped.append((news['_source']['sourcecountry'], datetime.strptime(news['_source']['seendate'], '%Y%m%dT%H%M%SZ').strftime('%d %b %Y'), news['_source']['title'], \
            news['_source']['url'], news['_source']['socialimage']))
    stripped = pd.DataFrame.from_dict(stripped)
    stripped.columns = ['Source Country', 'Publish Date', 'Title of Article', 'Link', 'image']
    stripped['image'] = '<img src="' + stripped['image'] + '" onerror="this.onerror=null;this.src=\'https://upload.wikimedia.org/wikipedia/commons/b/b2/High-contrast-image-missing.svg\';" height=70 />'
    stripped['Link'] = '<a href="' + stripped['Link'] + '">Link</a>'
    return stripped



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
#try:    
data = aggregate_countries()
st.bar_chart(data, x="Country", y="Number of Articles", height=400, use_container_width=False, width=800)
#except:
#    st.text("There is no data in Elastic yet. Add some data")

st.markdown("""---""")

with st.sidebar:
    with st.form("search"):
        st.write("Search News Articles")
        search_term = st.text_input("Search Term")
        submitted = st.form_submit_button("Submit")
        if submitted:
            search_query = {"match": {"title": {"query": search_term}}}

html = latest_articles(search_query).to_html(render_links=True, escape=False, index=False)
st.markdown(html, unsafe_allow_html=True)
