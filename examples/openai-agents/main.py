import os

from agents import Agent, Runner, function_tool

from agentlens import AgentLens, install_openai_agents_tracing


client = AgentLens(
    api_key=os.environ["AGENTLENS_API_KEY"],
    project_id=os.environ["AGENTLENS_PROJECT_ID"],
    endpoint=os.environ.get("AGENTLENS_ENDPOINT", "http://localhost:8000"),
).configure()

install_openai_agents_tracing(client)


@function_tool
def lookup_policy(topic: str) -> str:
    return f"Policy summary for {topic}: approve standard password reset requests."


agent = Agent(
    name="Support Assistant",
    instructions="Answer support questions using the available tool when relevant.",
    tools=[lookup_policy],
)


if __name__ == "__main__":
    result = Runner.run_sync(agent, "What is the password reset policy?")
    print(result.final_output)
