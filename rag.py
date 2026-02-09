import numpy as np
import faiss
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key="csk-vvtfvve63m5f4h4ekmtwrm2my3d2xjwf6de2nwtwckfe6thr"
)

def load_documents_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
   
    documents = [doc.strip() for doc in text.split("\n\n") if doc.strip()]
    return documents

documents = load_documents_from_txt("data.txt")
np.random.seed(42)
doc_embeddings = np.random.rand(len(documents), 512).astype("float32")


index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings)

def rag_answer(query, top_k=2):
   
    np.random.seed(hash(query) % 2**32) 
    query_embedding = np.random.rand(1, 512).astype("float32")
    
    
    distances, indices = index.search(query_embedding, top_k)
    retrieved_docs = [documents[i] for i in indices[0]]
    
    context = "\n".join(retrieved_docs)
   
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful AI."},
            {
                "role": "user",
                "content": f"Answer the question based on the following text:\n\n{context}\n\nQuestion: {query}"
            }
        ],
        model="gpt-oss-120b",
        max_completion_tokens=200,
        temperature=0.7,
        top_p=1
    )
    
    return completion.choices[0].message.content

query = "what u know about v link ?"
answer = rag_answer(query)
print("Answer:", answer)
