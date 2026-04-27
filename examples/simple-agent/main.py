import os

from agentlens import AgentLens, trace_agent, trace_step

client = AgentLens(
    api_key=os.environ["AGENTLENS_API_KEY"],
    project_id=os.environ["AGENTLENS_PROJECT_ID"],
    endpoint=os.environ.get("AGENTLENS_ENDPOINT", "http://localhost:8000"),
).configure()


@trace_step(type="tool_call", name="search_documents")
def search_documents(query: str) -> dict[str, object]:
    return {"matches": ["document_1", "document_2"], "query": query}


@trace_agent(name="knowledge_assistant_agent")
def run_agent(message: str) -> dict[str, object]:
    result = search_documents(message)
    return {"message": "done", "result": result}


if __name__ == "__main__":
    print(run_agent("Find architecture notes for the payment retry workflow"))
