"""
OpenAI API Service.
Handles all interactions with OpenAI Assistant API.
"""
import os
import time
from openai import OpenAI
import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Global assistant ID storage (in production, use database)
assistant_id = None
vector_store_id = None


def load_vector_store_id():
    """Load vector store ID from file if it exists."""
    global vector_store_id
    if os.path.exists('.vector_store_id'):
        with open('.vector_store_id', 'r') as f:
            vector_store_id = f.read().strip()
            print(f"Loaded vector store: {vector_store_id}")
    return vector_store_id


def get_or_create_assistant():
    """
    Get existing assistant or create a new one.

    Returns:
        str: Assistant ID
    """
    global assistant_id

    if assistant_id:
        return assistant_id

    # Load vector store ID
    vs_id = load_vector_store_id()

    # Try to find existing assistant
    assistants = client.beta.assistants.list()
    for asst in assistants.data:
        if asst.name == config.ASSISTANT_NAME:
            assistant_id = asst.id

            # Update assistant with latest instructions and vector store
            update_params = {
                "instructions": config.ASSISTANT_INSTRUCTIONS
            }
            if vs_id:
                update_params["tool_resources"] = {
                    "file_search": {
                        "vector_store_ids": [vs_id]
                    }
                }

            try:
                # Also update tools to include code_interpreter for image support
                update_params["tools"] = [{"type": "file_search"}, {"type": "code_interpreter"}]
                client.beta.assistants.update(
                    assistant_id=assistant_id,
                    **update_params
                )
                print(f"Updated assistant with latest instructions and tools")
                if vs_id:
                    print(f"Updated assistant with vector store: {vs_id}")
            except Exception as e:
                print(f"Could not update assistant: {e}")

            return assistant_id

    # Create new assistant with vector store
    tool_resources = {}
    if vs_id:
        tool_resources = {
            "file_search": {
                "vector_store_ids": [vs_id]
            }
        }

    assistant = client.beta.assistants.create(
        name=config.ASSISTANT_NAME,
        instructions=config.ASSISTANT_INSTRUCTIONS,
        model="gpt-4o",
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],  # Added code_interpreter for image support
        tool_resources=tool_resources if tool_resources else None
    )
    assistant_id = assistant.id
    print(f"Created new assistant: {assistant_id}")
    return assistant_id


def create_thread(knowledge_file_ids=None):
    """
    Create a new conversation thread.

    Args:
        knowledge_file_ids: List of file IDs to attach to thread (optional)

    Returns:
        str: Thread ID
    """
    if knowledge_file_ids:
        # Create thread with knowledge base files attached
        attachments = [
            {"file_id": fid, "tools": [{"type": "file_search"}]}
            for fid in knowledge_file_ids
        ]

        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": "Initialize knowledge base",
                "attachments": attachments
            }]
        )
    else:
        thread = client.beta.threads.create()

    return thread.id


def send_message_to_thread(thread_id, message_content, file_id=None, use_file_search=True):
    """
    Send a message to a thread and get response.

    Args:
        thread_id: Thread ID
        message_content: Text content of the message
        file_id: Optional file ID to attach
        use_file_search: Whether to use file_search tool (True for documents, False for images)

    Returns:
        str: Assistant's response text
    """
    # Add message to thread
    message_params = {
        "thread_id": thread_id,
        "role": "user"
    }

    if file_id:
        # For images (use_file_search=False), use attachments with code_interpreter
        # For documents (use_file_search=True), use attachments with file_search tool
        if use_file_search:
            # Documents: use attachments with file_search
            message_params["content"] = message_content
            message_params["attachments"] = [{
                "file_id": file_id,
                "tools": [{"type": "file_search"}]
            }]
        else:
            # Images: use attachments with code_interpreter for vision
            message_params["content"] = message_content
            message_params["attachments"] = [{
                "file_id": file_id,
                "tools": [{"type": "code_interpreter"}]
            }]
    else:
        # Text only message
        message_params["content"] = message_content

    client.beta.threads.messages.create(**message_params)

    # Get or create assistant
    asst_id = get_or_create_assistant()

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=asst_id
    )

    # Wait for completion
    if not wait_for_run_completion(thread_id, run.id):
        raise Exception('Assistant response timed out')

    # Get the latest message
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        order="desc",
        limit=1
    )

    if messages.data:
        assistant_message = messages.data[0]
        return assistant_message.content[0].text.value
    else:
        raise Exception('No response from assistant')


def upload_file_to_openai(filepath, purpose='assistants'):
    """
    Upload a file to OpenAI.

    Args:
        filepath: Path to the file
        purpose: Purpose of the file - 'vision' for images, 'assistants' for documents

    Returns:
        str: File ID from OpenAI
    """
    with open(filepath, 'rb') as f:
        uploaded_file = client.files.create(
            file=f,
            purpose=purpose
        )
    return uploaded_file.id


def wait_for_run_completion(thread_id, run_id, timeout=600):
    """
    Wait for the assistant run to complete.

    Args:
        thread_id: Thread ID
        run_id: Run ID
        timeout: Maximum time to wait in seconds (default: 600 seconds = 10 minutes)

    Returns:
        bool: True if completed, False if timed out or failed
    """
    start_time = time.time()
    print(f"[DEBUG] Starting to wait for run {run_id} completion...")

    while time.time() - start_time < timeout:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        elapsed = time.time() - start_time
        print(f"[DEBUG] Run status: {run.status} (elapsed: {elapsed:.1f}s)")

        if run.status == 'completed':
            print(f"[DEBUG] Run completed successfully after {elapsed:.1f}s")
            return True
        elif run.status in ['failed', 'cancelled', 'expired']:
            print(f"[DEBUG] Run failed with status: {run.status}")
            if hasattr(run, 'last_error') and run.last_error:
                print(f"[DEBUG] Error details: {run.last_error}")
            return False

        time.sleep(0.5)

    print(f"[DEBUG] Run timed out after {timeout}s")
    return False
