from openai import OpenAI
from langchain_openai import ChatOpenAI

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from langchain_text_splitters import CharacterTextSplitter
from langchain.docstore.document import Document
import json
from typing import Dict, Any
import os

os.environ["OPENAI_API_KEY"] = ""

llm = ChatOpenAI(temperature = 0.7, model_name = "gpt-3.5-turbo-1106")
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])

def _summarize(x: str) -> str:
    x = ' '.join(x.split())
    x = x.replace("\n", "")
    chunks, chunk_size = len(x), 12000
    chunks = [ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    doc = Document(page_content = chunks[0])

    prompt_template = """Write a detailed summary of the following in one block of text.:
    "{text}"
    DETAILED SUMMARY (ONE BLOCK OF TEXT):"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    return stuff_chain.invoke([doc])["output_text"]

def _subtopics(content: str) -> Dict[str, Any]:
    prompt = f"""
    Given the following article summary, provide a comprehensive and detailed output.
    1. If the topic is technical (math, physics, computer science), provide an example problem AND solution.
    2. If the topic is non-technical (humanities, earth science, biology), provide a brief case study.

    Output any math in Latex and use $ as the delimeter.

    Here's the summary:
    {content}
    """

    try:
        response = client.chat.completions.create(model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            n=1,
            temperature=0.7
        )

        content = response.choices[0].message.content
        return content 

    except Exception as e:
        print(f"Error in summarizing content: {e}")
        return "OpenAI error"

def summarize_content(content: str) -> str:
    a = _summarize(content)
    b = _subtopics(content)
    return a + "\n\n\n" + b

def summarize_and_format(content: str) -> str:
    summary_json = summarize_content(content)
    #return format_summary(summary_json)
    return summary_json
