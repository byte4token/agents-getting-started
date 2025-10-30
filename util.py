# Import packages
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables from .env file

def get_project_client():
    # Use the connection string to connect to your Foundry project
    project_connection_string = os.getenv("AIPROJECT_CONNECTION_STRING")
    try:
        project = AIProjectClient(
            endpoint=project_connection_string,
            credential=DefaultAzureCredential()
        )

        return project
    except Exception as e:
        print(f"Failed to connect to project: {e}")
        raise

def sendMessage(project, agentId, msg):
    # Create a thread
    thread = project.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg,  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agentId)
    print(f"Run finished with status: {run.status}")

    messages = project.agents.messages.list(thread_id=thread.id, order="asc")
    for msg in messages:
        role = msg.role
        content = msg.content[0].text.value
        print(f"{role.capitalize()}: {content}")

