"""
Upload Knowledge Base Files to OpenAI Vector Store
This script uploads your shop's knowledge base files so the AI can answer customer questions
"""

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import time

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
VECTOR_STORE_NAME = os.getenv('VECTOR_STORE_NAME', '<PUT_YOUR_VECTOR_STORE_NAME_HERE>')  # <-- put your vector store name here
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'Clothing Shop Assistant')
KNOWLEDGE_BASE_DIR = 'knowledge_base'

def get_or_create_vector_store():
    """Get existing vector store or create a new one"""
    print(f"\n🔍 Looking for existing vector store: '{VECTOR_STORE_NAME}'...")

    # Check if vector store already exists
    vector_stores = client.beta.vector_stores.list()
    for vs in vector_stores.data:
        if vs.name == VECTOR_STORE_NAME:
            print(f"✅ Found existing vector store: {vs.id}")
            return vs.id

    # Create new vector store
    print(f"📦 Creating new vector store: '{VECTOR_STORE_NAME}'...")
    vector_store = client.beta.vector_stores.create(
        name=VECTOR_STORE_NAME
    )
    print(f"✅ Vector store created: {vector_store.id}")
    return vector_store.id

def upload_files_to_vector_store(vector_store_id):
    """Upload all files from knowledge_base directory"""
    print(f"\n📁 Scanning knowledge base directory: {KNOWLEDGE_BASE_DIR}/")

    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"❌ Error: Directory '{KNOWLEDGE_BASE_DIR}' not found!")
        return []

    files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.endswith(('.txt', '.pdf', '.docx', '.md'))]

    if not files:
        print(f"⚠️  No files found in {KNOWLEDGE_BASE_DIR}/")
        return []

    print(f"📄 Found {len(files)} files to upload:")
    for f in files:
        print(f"   - {f}")

    file_ids = []

    for filename in files:
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        print(f"\n⬆️  Uploading: {filename}...")

        try:
            with open(filepath, 'rb') as file:
                uploaded_file = client.files.create(
                    file=file,
                    purpose='assistants'
                )
                file_ids.append(uploaded_file.id)
                print(f"   ✅ Uploaded successfully: {uploaded_file.id}")
        except Exception as e:
            print(f"   ❌ Error uploading {filename}: {e}")

    # Add files to vector store
    if file_ids:
        print(f"\n🔗 Attaching {len(file_ids)} files to vector store...")
        try:
            client.beta.vector_stores.file_batches.create(
                vector_store_id=vector_store_id,
                file_ids=file_ids
            )
            print(f"   ✅ Files attached to vector store!")

            # Wait for processing
            print(f"   ⏳ Processing files (this may take a moment)...")
            time.sleep(3)

        except Exception as e:
            print(f"   ❌ Error attaching files: {e}")

    return file_ids

def update_assistant_with_vector_store(vector_store_id):
    """Update assistant to use the vector store"""
    print(f"\n🤖 Updating assistant: '{ASSISTANT_NAME}'...")

    # Find the assistant
    assistants = client.beta.assistants.list()
    assistant_id = None

    for asst in assistants.data:
        if asst.name == ASSISTANT_NAME:
            assistant_id = asst.id
            break

    if not assistant_id:
        print(f"⚠️  Assistant '{ASSISTANT_NAME}' not found. It will be created on first use.")
        return

    # Update assistant with vector store
    try:
        client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            }
        )
        print(f"✅ Assistant updated with knowledge base!")
        print(f"   Assistant ID: {assistant_id}")
        print(f"   Vector Store ID: {vector_store_id}")
    except Exception as e:
        print(f"❌ Error updating assistant: {e}")

def main():
    print("=" * 60)
    print("📚 KNOWLEDGE BASE UPLOAD TOOL")
    print("=" * 60)

    try:
        # Step 1: Create or get vector store
        vector_store_id = get_or_create_vector_store()

        # Step 2: Upload files
        file_ids = upload_files_to_vector_store(vector_store_id)

        if not file_ids:
            print("\n⚠️  No files were uploaded. Please add files to the knowledge_base/ folder.")
            return

        # Step 3: Update assistant
        update_assistant_with_vector_store(vector_store_id)

        # Save vector store ID for future use
        with open('.vector_store_id', 'w') as f:
            f.write(vector_store_id)

        print("\n" + "=" * 60)
        print("✅ KNOWLEDGE BASE UPLOAD COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   - Vector Store: {VECTOR_STORE_NAME}")
        print(f"   - Files Uploaded: {len(file_ids)}")
        print(f"   - Vector Store ID: {vector_store_id}")
        print(f"\n💡 Your assistant can now answer questions based on these files!")
        print(f"   Restart your Flask server to apply changes.\n")

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
