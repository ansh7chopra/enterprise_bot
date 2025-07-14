# agents/meeting_agent.py
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
import os, dotenv; dotenv.load_dotenv()
from agents.meeting_scheduler_agent import meeting_tool
from utils.rag_search import enterprise_search_tool



def get_meeting_agent():
    llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-70b-8192",  # or mixtral
    temperature=0
)

    return initialize_agent(
        tools=[enterprise_search_tool],              
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
        handle_parsing_errors=True,
        verbose=True,
    )
