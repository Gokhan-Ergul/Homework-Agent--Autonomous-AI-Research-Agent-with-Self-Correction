from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from langchain_core.messages import ToolMessage

from langgraph.prebuilt import ToolNode

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')
llm_with_tools = llm.bind_tools(tools)


tool_node = ToolNode(tools)

from workflow import HomeworkState
def Researcher_agent(state: HomeworkState) -> HomeworkState:
    """This search agent node recieves the topic and decides to search it on web."""

    print("--- RESEARCHER_agent WORKING ---")
    
    message = state['messages']

    response = llm_with_tools.invoke(message)
    #this will contain AIMessage about tool_call not answer of the llm query.

    #after tool run, the response will turn back to reasearcher node by "Conditional edge (we will set it later.)"
    # messages will be like this:
    #HumanMessage (.........)
    #AIMessage (..........)
    #ToolMessage (...........)
    #the second time llm ask itself:Are these search results sufficient? Or do I need more information?
    #Senerio A: This results enough.
    #Senerio B: These are not enough I want to use the tool again. AIMessage(tool_calls=[...New_query...])
    print("--- REASEARCHER FINISHED DRAFT ---")
    return {'messages':[response]}

def compile_research_node(state: HomeworkState) -> HomeworkState:
    """Runs after the search cycle completes.
    Finds all ToolMessages in the 'messages' list, collects their contents, and writes them to
    the 'researcher_result' key. """

    print("--- compile_research_node WORKING ---")

    
    compaile_results = []
    messages = state['messages']
    for m in messages:
        if isinstance(m, ToolMessage):
            # The content returned by TavilySearch may already be a list,
            # so it might be safer to use 'extend'.
            # OR 'append' if you assume the content is a string.
            if isinstance(m.content,str):
                compaile_results.append(m.content)

            elif isinstance(m.content, list):
                compaile_results.extend(m.content)
    print("--- COMPAILE FINISHED DRAFT ---")

    return {'researcher_result': compaile_results}

from langchain.schema.messages import SystemMessage, HumanMessage
def writer_agent(state: HomeworkState) -> HomeworkState: #google use docstring like this:
    """
Runs the Writer Agent to synthesize an academic draft in Markdown.

This node retrieves sources from the 'researcher_result' key in the state, 
prompts the LLM to write a formal draft based on those sources, and
formats the output as Markdown.

Args:
    state (Homework_state): The current state of the graph. Must 
                            contain 'researcher_result'.

Returns:
    dict: A dictionary with the key 'writer_result' containing the
          newly generated Markdown draft.
"""
    print("--- writer_agent WORKING ---")
    
    research_results = state['researcher_result'] # if you give this to llm directly it may not understand so we will give it more readable shape.
    sources_text = "\n\n---\n\n".join(research_results)
    
    does_need_to_rewrite = state.get('does_need_to_rewrite')
    
    if not does_need_to_rewrite or does_need_to_rewrite == None:        
        system_prompt = """
        You are an expert academic writer. 
        Your task is to synthesize information from various sources into a coherent, 
        well-structured academic paper.
        You must only use the information provided in the sources.
        You must format your entire output in Markdown.
        """
        
        user_prompt = f"""
        Here are the research sources:
        
        <SOURCES>
        {sources_text}
        </SOURCES>
        
        Please write an academic draft in Markdown based *only* on these sources.
        """
    
        #in here we don't use llm_with_tools because only reaseacher can use it.
         # If you use a chat model then you have to use : SystemMessage or HumanMessage. On Reasearch part we will give the input with using HumanMessages.
        #SystemMessage: Tells LLM who you are.
        #HumanMessage : Tells the request to LLM.

    else:
        writer_result = state['writer_result']
        mistakes = state['mistakes']
        
        system_prompt = """
        You are an expert academic editor. 
        Your task is to rewrite an academic paper to fix specific mistakes.
        You must use the <SOURCES> as the single source of truth.
        The new paper MUST be in Markdown.
        
        """
        user_prompt = f"""
        Here are the original research sources:
        
        <SOURCES>
        {sources_text}
        </SOURCES>
        
        Here is the flawed academic paper:
        <PAPER>
        {writer_result}
        </PAPER>

        Here are the mistakes you MUST fix:
        <MISTAKES>
        {mistakes}
        </MISTAKES>
        
        Please rewrite the entire paper in Markdown, ensuring all mistakes are 
        corrected and the content strictly follows the sources.
        """

    messages_for_llm = [
        SystemMessage(content = system_prompt),
        HumanMessage(content = user_prompt)
    ]
    
    response = llm.invoke(messages_for_llm)
        
    markdown_draft = response.content
        
    print("--- WRITER FINISHED DRAFT ---")
        
    return {"writer_result" : markdown_draft}

def controller_agent(state: HomeworkState) ->HomeworkState:
    """This agent controls the rewrite text and source text to detect if there is any hallucination on rewrited text writer_result
    
    Args:
    state (Homework_state): The current state of the graph. Must 
                            contain 'researcher_result' and 'writer_result '.

    
    Returns:
    bool: A boolean with the key 'does_need_to_rewrite' it will say if there is hallucination or not.                    
    """
    print('---CONTROLLER IS RUNNING---')
    researcher_result = state['researcher_result']
    writer_result = state['writer_result']
    
    research_results = state['researcher_result'] # if you give this to llm directly it may not understand so we will give it more readable shape.
    sources_text = "\n\n---\n\n".join(research_results)
    
    system_prompt = """You are an expert fact-checker and editor. Your task is to compare an academic paper
    against its original sources. You must identify *any* statements in the paper that
    are NOT supported by the sources (hallucinations) or contradict the sources.

    If the paper is perfect and has NO hallucinations, you must respond with 
    the single word: NONE
    
    If you find any hallucinations or unsupported claims, you MUST return a 
    list of the specific mistakes."""
    

    user_prompt = f"""
        Here are the research sources:
        
        <SOURCES>
        {sources_text}
        </SOURCES>
        Here are the rewrited academic paper:
        Here is the academic paper to check:
        <PAPER>
        {writer_result}
        </PAPER>
        
        Remember: Respond with ONLY the word "NONE" if there are no errors. Otherwise, list the errors.
        """
    messages_for_llm = [
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt)
        ]
    
    response = llm.invoke(messages_for_llm)
    response_content = response.content.strip()
    
    if response_content == "NONE":
        print('---THERE IS NO ERROR.')
        print('---CONTROLLER IS FINISHED---')
        return {'does_need_to_rewrite':False, 'mistakes': ""}
        
    else:
        print('---CONTROLLER FIND SOME ERROR:---')
        print('---CONTROLLER IS FINISHED---')
        
        return {'does_need_to_rewrite':True, 'mistakes': response_content}

import pypandoc
def formatter(state: HomeworkState) -> HomeworkState:
    """This is a formatter node. It creates a Word file from text written in Markdown format."""
    
    print('---FORMATTER NODE IS RUNNING ---')

    outputfile = 'student_number_homeworkname.docx'
    
    writer_result = state['writer_result']
    
    try:
        pypandoc.convert_text(
            writer_result,
            'docx',
            format = 'md', #markdown
            outputfile= outputfile
        )
        print(f"The {outputfile} saved succesfully!.")
        return {"document_path": outputfile}
        
    except Exception as e:
        print("---THERE IS SOMETHING WRONG THE WORD FILE COUND'T CREATE!---")
        print(e)
        return {"document_path": None}

def should_contunie(state: HomeworkState) -> str:
    """The researcher decides the flow after the agent."""
    last_message = state['messages'][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return 'tool_call'

    else:
        return 'compile'

def decide_to_rewrite(state: HomeworkState) -> str:
    """Reads the Auditor's decision and directs the flow."""

    
    if state.get('does_need_to_rewrite') == True:
        return 'rewrite'
    else:
        return 'format'

