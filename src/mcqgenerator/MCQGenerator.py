from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
import os
import json
from dotenv import load_dotenv
import PyPDF2

#load environment variables from the .env file
load_dotenv()
#access the environment variables just like you would with os.environ
Key=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key= Key, model_name="gpt-3.5-turbo", temperature=0)

#with open("C:\\Users\\HP\\mcqgen1\\Response.json", "r") as f:
 #  RESPONSE_JSON = json.load(f)

#print(RESPONSE_JSON)

TEMPLATE = """
Text:{text}
You are expert reader . Given the above text, it is your job to \ 
provide the answer to {subject}. Make sure to provide the question and relevant answer in table format.
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "subject"],
    template=TEMPLATE)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz")

TEMPLATE2 = """
Given a {subject}.\
you need to evaluate the answer in quiz and respond accordingly.\
Answer:
{quiz}
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review")

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "subject"],
    output_variables=["quiz"],
    
)