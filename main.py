from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.mongodb import MongodbLoader
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = ""
def chatbotdb(query, server, db, collection ):
    loader = MongodbLoader(
        connection_string=server,
        db_name=db,
        collection_name=collection,
    )
    docs = loader.load()

    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(docs, embedding=embeddings)
    vectors.save_local("faiss_index")

    vectors = FAISS.load_local("faiss_index", embeddings)
    retriever = vectors.as_retriever(search_type="similarity", search_kwargs={"k":2})
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    query = f"###Prompt {query}"
    try:
        llm_response = qa(query)
        return llm_response["result"]
    except Exception as err:
        return 'Exception occurred. Please try again', str(err)
