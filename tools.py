# tools.py

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

search_runnable = TavilySearch(max_results = 5)
tools = [search_runnable]