from typing import Annotated, Literal
from langgraph.types import Command
from pydantic import BaseModel
from ai.llms import get_groq_model
from langgraph.graph import StateGraph, START
from typing import TypedDict
from IPython.display import display, Image



class TitleSummaryResponse(BaseModel):
    title: Annotated[str, "A clear, concise title for the document"]
    summary: Annotated[str, "A short and accurate summary of the document"]

def title_summary_agent(state):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert technical writer. Your task is to generate a suitable title "
                "and a concise summary for the following technical document:\n\n"
                f"{state['document']}"
            )
        }
    ]

    response = get_groq_model().with_structured_output(TitleSummaryResponse).invoke(messages)

    return Command(
        goto="tag_category",
        update={
            "title": response.title,
            "summary": response.summary,
        }
    )


class TagCategoryResponse(BaseModel):
    tags: Annotated[list[str], "Relevant keywords for searchability and organization"]
    category: Annotated[str, "The category this document belongs to (e.g., frontend, backend, devops, ai, etc)"]

def tag_category_agent(state):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in technical content classification. Based on the following document title "
                f"and summary, generate a relevant category and useful tags:\n\n"
                f"Title: {state['title']}\n"
                f"Summary: {state['summary']}"
            )
        }
    ]

    response = get_groq_model().with_structured_output(TagCategoryResponse).invoke(messages)

    return Command(
        goto="__end__",
        update={
            "tags": response.tags,
            "category": response.category,
        }
    )


class GraphState(TypedDict):
    document: Annotated[str, "The document to be sorted"]
    tags: Annotated[list[str], "List of tags for the document"]
    category: Annotated[str, "Category of the documentation"]
    title: Annotated[str, "Title of the document"]
    summary: Annotated[str, "Summary of the document"]
    messages: Annotated[list[str], "List of user-facing messages"]

graph = StateGraph(GraphState)

# Add agent nodes
graph.add_node("title_summary", title_summary_agent)
graph.add_node("tag_category", tag_category_agent)

# Define the flow
graph.add_edge(START, "title_summary")
graph.add_edge("title_summary", "tag_category")
graph.add_edge("tag_category", "__end__")

# Compile the graph
agent = graph.compile()

# display(Image(app.get_graph().draw_mermaid_png()))



