from mcp.server.fastmcp import FastMCP
from helper import create_s3_bucket, delete_s3_bucket

# Initialize FastMCP server
mcp = FastMCP("aws")

@mcp.tool()
async def initiate_s3_bucket_creation():
    """
    Initiates the creation of an S3 bucket.
    """
    print("Creating S3 bucket...")
    result = create_s3_bucket()
    return result

@mcp.tool()
async def initiate_s3_bucket_deletion():
    """
    Initiates the deletion of an S3 bucket.
    """
    print("Deleting S3 bucket...")
    result = delete_s3_bucket()
    return result

if __name__ == "__main__":
    print("Starting FastMCP server for S3...")
    mcp.run(transport='stdio')
    print("FastMCP server is running.")
