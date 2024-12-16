import json
from typing import Any
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Initalize server instance
GMAIL_API_BASE = "https://www.googleapis.com/gmail/v1"
USER_AGENT = "mail-app/1.0"

server = Server("mail")

# Defining list of tools
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
   """List available tools. Each tool specifies its arguments using JSON Schema validation. """
   
   return [
        types.Tool(
            name="get-emails",
            description="Get emails for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "maxResults": {
                        "type": "integer",
                        "description": "Number of emails to retrieve (e.g., 5, 10, 20)",
                    },
                },
                "required": ["maxResults"],
            },
        ),
    ]
   
# Helper functions for querying and formatting the data from the GMAIL API
async def query_gmail(service, max_result: int) -> list[dict] | None:
    """
    Query Gmail API to fetch the first X emails.
    Args:
        service: Authorized Gmail API service instance.
        max_results: Number of emails to fetch.
    Returns:
        List of email metadata or None in case of failure.
    """
    try:
        # Fetch email list
        response = service.users().messages().list(
            userId="me", maxResults=max_result
            ).execute()
        # Return list of message metadata
        return response.get("messages", [])
    except Exception as e:
        print(f"Falied to fetch emails: {e}")
        return None

def format_email(service, email_metadata: dict) -> str:
    """
    Format email metadata to include only the subject and sender.
    Args:
        service: Authorized Gmail API service instance.
        email_metadata: Metadata for a single email (e.g., ID).
    Returns:
        A formatted string containing the subject and sender.
    """
    try:
        # Fetch the email in 'full' format
        message = service.users().messages().get(
            userId="me", id=email_metadata["id"], format="full"
        ).execute()

        # Extract headers
        headers = message.get("payload", {}).get("headers", [])

        # Case-insensitive extraction for Subject and From
        subject = next(
            (header["value"] for header in headers if header["name"].lower() == "subject"), "No Subject"
        )
        sender = next(
            (header["value"] for header in headers if header["name"].lower() == "from"), "Unknown Sender"
        )

        return f"Subject: {subject}\nSender: {sender}\n"

    except Exception as e:
        print(f"Failed to fetch or format email: {e}")
        return "Failed to fetch or format this email."

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """
    Handle tool execution requests for fetching emails.
    """
    # Validate there are enough arguments
    if not arguments:
        raise ValueError("Missing arguments")
    if name == "get-emails":
        max_results = arguments.get("maxResults")
        if not max_results or not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("The 'maxResults' parameter must be a positive integer.")
        
        # Get Gmail API server
        from mail.auth import get_gmail_service
        service = get_gmail_service()
        
        # Query Gmail API for the first 'maxResults' emails
        email_metadata_list = await query_gmail(service, max_results)
        if not email_metadata_list:
            return [
                types.TextContent(
                    type="text",
                    text="No emails found or failed to fetch."
                ) 
            ]
        # Format the mails and prepare results 
        formatted_emails = []
        for email_metadata in email_metadata_list:
            formatted_email = format_email(service, email_metadata)
            formatted_emails.append(
                types.TextContent(type="text", text=formatted_email)
            )
        
        return formatted_emails
    
    # Handle unknown tool names
    raise ValueError(f"Tool '{name}' is not supported.")

async def main():
    """
    Run the server using stdin/stdout streams.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mail",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# Entry point for running the server
if __name__ == "__main__":
    asyncio.run(main())
    