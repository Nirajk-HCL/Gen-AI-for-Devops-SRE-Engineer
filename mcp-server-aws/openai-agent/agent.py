import asyncio
import os
import shutil
from apply_env import apply_env


from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio

async def run(mcp_server: MCPServer,user_input: str):
    agent = Agent(
        name="Assistant",
        instructions="Use the mcp server and its tools to instanciate an AWS EC2 instance.",
        mcp_servers=[mcp_server],
    )

    message = user_input
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    

    
   

async def main(query:str):  

    root_dir = os.path.dirname(os.getcwd())
    async with MCPServerStdio(
        name="AWS ec2 agent",        
        params={
            "command": "uv",
            "args": [
                "--directory", 
                root_dir,
                "run",
                "aws.py",],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP aws Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server,user_input=query)


if __name__ == "__main__":
    apply_env()
    # Let's make sure the user has npx installed
    if not shutil.which("uv"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    while True:
        user_input = input("Enter your command (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        else:
            asyncio.run(main(user_input))