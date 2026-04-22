# College Admission Assistant 🎓

This project is a fully-featured Gen AI application integrating **Streamlit (UI)**, **n8n (Orchestration)**, **MCP (Model Context Protocol)**, and **RAG (Vector DB)** to create a ChatGPT-like College Admission Assistant.

## Project Structure
- `ui/app.py`: The Streamlit chat interface.
- `mcp_server/server.py`: A Python MCP server providing admission-related tools.
- `data_prep/build_vector_db.py`: A script to initialize a local RAG database using ChromaDB.
- `n8n_workflows/workflow.json`: A sample n8n workflow for orchestration.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed. Open a terminal in this directory and run:
```bash
pip install -r requirements.txt
```

### 2. Prepare the Vector Database (RAG)
We are using **Chroma Cloud** to host our vector database. Run the script to process the CSV data and upload it to your Chroma Cloud cluster:
```bash
python data_prep/build_vector_db.py
```
*This will upload the embeddings to your cloud database so the n8n workflow can query it from anywhere.*

### 3. Start the MCP Server
In a new terminal window, start the MCP server:
```bash
python mcp_server/server.py
```
*This runs locally over standard I/O, which your MCP client (like Claude Desktop or n8n with MCP support) can connect to.*

### 4. Setup n8n
1. Start your n8n instance.
2. Import the `n8n_workflows/workflow.json` file.
3. In the workflow, attach your LLM provider credentials (e.g., OpenAI, Gemini).
4. Connect the **Vector Store** and **MCP Tool** nodes to the AI Agent (you can add these via the n8n UI).
5. Ensure the Webhook URL in n8n matches the one in `ui/app.py`.
6. **Activate** the workflow.

### 5. Run the UI
Finally, start the Streamlit UI in a new terminal window:
```bash
streamlit run ui/app.py
```

This will open the web interface in your browser (usually `http://localhost:8501`). You can now chat with the assistant!
