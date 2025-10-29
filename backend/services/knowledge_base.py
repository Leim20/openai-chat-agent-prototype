"""
Knowledge Base Management Service.
Handles loading and uploading knowledge base files to OpenAI.
"""
import os
from openai import OpenAI
import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Cache uploaded file IDs
_knowledge_file_ids = None


def load_knowledge_base_files(knowledge_dir='knowledge_base'):
    """
    Upload all files from knowledge_base directory and return file IDs.

    Args:
        knowledge_dir: Directory containing knowledge base files

    Returns:
        list: List of OpenAI file IDs
    """
    file_ids = []

    if not os.path.exists(knowledge_dir):
        print(f"Knowledge base directory '{knowledge_dir}' not found")
        return file_ids

    supported_extensions = ('.pdf', '.txt', '.docx', '.md', '.csv', '.json')

    for filename in os.listdir(knowledge_dir):
        if filename.endswith(supported_extensions):
            filepath = os.path.join(knowledge_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    uploaded_file = client.files.create(
                        file=f,
                        purpose='assistants'
                    )
                    file_ids.append(uploaded_file.id)
                    print(f"Uploaded knowledge file: {filename} -> {uploaded_file.id}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")

    return file_ids


def get_knowledge_file_ids(knowledge_dir='knowledge_base'):
    """
    Get or upload knowledge base files (with caching).

    Args:
        knowledge_dir: Directory containing knowledge base files

    Returns:
        list: List of OpenAI file IDs
    """
    global _knowledge_file_ids

    if _knowledge_file_ids is None:
        _knowledge_file_ids = load_knowledge_base_files(knowledge_dir)
        if _knowledge_file_ids:
            print(f"Loaded {len(_knowledge_file_ids)} knowledge base files")

    return _knowledge_file_ids


def reset_knowledge_cache():
    """Reset the knowledge file IDs cache (useful for reloading files)."""
    global _knowledge_file_ids
    _knowledge_file_ids = None
