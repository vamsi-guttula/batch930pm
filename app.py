import validators
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
##
st.set_page_config(page_title="Summarize Text from Website")
st.title("Summarize using Langchain")
user_key = st.sidebar.text_input(label="Provide the api key",type='password')
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0,api_key=user_key)
prompt_temp="""
Provide the summary of the following content 5 lines and Print line by line with bullets:
content:{text}
"""
####
prompt =PromptTemplate(template=prompt_temp,input_variables=["text"])

user_url = st.text_input("URL")

if st.button("click to summarize:"):
    if not user_url.strip():
        st.error("URL cannot be empty")
    elif not validators.url(user_url):
        st.error("provide the URL in the correct format")
    else:
        try:
            with st.spinner(text="In Progress"):
                loader =UnstructuredURLLoader(urls=[user_url],ssl_verify=False,
                                              header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
                data=loader.load()

                chain = load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output = chain.run(data)

                st.success(output)

        except Exception as e:
            st.exception(f'Exception:{e}')


            
