from typing import List
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document

ollama_host = ""
ollma_model = "orca-mini:3b"

embeddings = OllamaEmbeddings(model=ollma_model, base_url=ollama_host)

store = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store)
db = InMemoryVectorStore(embedding=cached_embedder)

qa_chain, rag_chain = None, None

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If relevent context is not present below, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
llm = Ollama(model=ollma_model, base_url=ollama_host)


def generate_embedding(path):
    global db
    textSplitter = CharacterTextSplitter(separator="\n", chunk_size=2000, chunk_overlap=200)
    with open(path) as f:
        dummy_text = [Document(page_content=f.read())]

    splites = textSplitter.split_documents(dummy_text)
    db.add_documents(documents=splites, embeddings=cached_embedder)


def generate_response(prompt_input):
    global db, qa_chain, rag_chain
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    qa_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
    )
    rag_chain = create_retrieval_chain(retriever=db.as_retriever(), combine_docs_chain=qa_chain)

    ai_response = ""
    for chunk in rag_chain.stream({"input": prompt_input}):
        if answer_chunk := chunk.get("answer"):
            ai_response += answer_chunk
    return ai_response
