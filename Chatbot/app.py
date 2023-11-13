import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import faiss



# Load enviroment variables
load_dotenv()

# Using Langchain csvloader to load the csv file
loader = CSVLoader(
    file_path='Mechanics/data/TheGoodAdvisorData.csv',
    csv_args={
        "delimiter":",",
        "fieldnames": ["course_type", "course_area", "course_code", "course_title","credit_hours", "Pre-requisites", "Descriptions"]
    })
documents = loader.load()

# Create Embeddings to be vectorize
embeddings = HuggingFaceEmbeddings()
db = faiss.FAISS.from_documents(documents, embeddings)

def retrieve_info(query):
    question = query["question"]
    
    cleaned_question = question.replace("\n", " ")  

    similar_response = db.similarity_search(cleaned_question)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array
    
repo_id= 'tiiuae/falcon-7b-instruct'

template = template="""
    You are a college advisor at Georgia State University that works for CS department. Your role is to help student create schedules by recommended coursea
    
    Example dialog as an adivisor
    
    Advisor: Absolutely, I'm happy to help plan your first semester computer science curriculum. One moment while I pull up our course catalog... 
    Okay, I have the full list of CS courses here in front of me. Based on your major and year, here are the courses I would recommend:

    {recommended_courses}
  """


prompt = PromptTemplate(
    input_variables=['recommended_courses'],
    template=template
)

def generate_response(prompt, user_message):
     llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature":0.6, "max_new_tokens":1048})
     llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
     recommended_courses = retrieve_info(user_message)
     response = llm_chain.predict(question=user_message["question"], recommended_courses=recommended_courses)
     return response
    
def main():
    while True:
        user_question = input("Enter question (or 'q' to quit):" )
        if user_question == 'q':
            break
        if user_question:
            user_message = {"question": user_question}
            response = generate_response(prompt, user_message)
            print(response)
    
    
if __name__ == "__main__":
        main()