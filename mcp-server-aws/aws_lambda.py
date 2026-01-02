from mcp.server.fastmcp import FastMCP
from helper import create_lambda_function, delete_lambda_function

mcp = FastMCP("aws")

@mcp.tool()
async def create_lambda():
    """Creates an AWS Lambda function."""
    return create_lambda_function()

@mcp.tool()
async def delete_lambda():
    """Deletes an AWS Lambda function."""
    return delete_lambda_function()

if __name__ == "__main__":
    print("Starting FastMCP server for Lambda...")
    mcp.run(transport='stdio')
