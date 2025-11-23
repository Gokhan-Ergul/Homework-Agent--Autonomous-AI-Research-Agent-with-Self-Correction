from langgraph.graph import StateGraph, END, START
from typing import TypedDict,List,Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from tools import tools

class HomeworkState(TypedDict):
    does_need_to_rewrite : bool
    researcher_result : List[str]
    writer_result : str
    mistakes : str
    messages : Annotated[Sequence[BaseMessage],add_messages]
    document_path: str
    rewriter_counter: int

from nodes import Researcher_agent, compile_research_node, writer_agent, controller_agent, formatter, update_counter_node, tool_node,should_contunie,decide_to_rewrite


workflow = StateGraph(HomeworkState)



workflow.add_node('researcher', Researcher_agent)
workflow.add_node('compile_research',compile_research_node)
workflow.add_node('run_tools', tool_node)
workflow.add_node('writer', writer_agent)
workflow.add_node("update_counter", update_counter_node)
workflow.add_node('controller',controller_agent)
workflow.add_node('formatter',formatter)

workflow.add_edge(START,'researcher')

workflow.add_conditional_edges(
    'researcher',
    should_contunie,
    {
        'tool_call':'run_tools',
        'compile':'compile_research'
    },
)
workflow.add_edge('run_tools', 'researcher')
workflow.add_edge('compile_research','writer')
workflow.add_edge('writer','update_counter')
workflow.add_edge('update_counter', 'controller')


workflow.add_conditional_edges('controller',
                              decide_to_rewrite,
                              {
                                  "rewrite":"writer",
                                  'format':'formatter'
                              },
                              )

workflow.add_edge('formatter', END)
app = workflow.compile()