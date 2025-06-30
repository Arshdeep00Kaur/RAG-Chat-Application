# 📚 GenieDocs - RAG PDF Question Answering System

> **Chat with your PDFs using AI-powered question answering**

## 🌟 Overview

GenieDocs is a powerful Retrieval-Augmented Generation (RAG) system that transforms static PDF documents into interactive, conversational experiences. Upload any PDF, ask questions in natural language, and get intelligent answers with precise page references.

## ✨ Features

- 📄 **PDF Upload**: Drag and drop PDF files for instant processing
- 🔍 **Intelligent Search**: Vector-based semantic search through document content
- 🤖 **AI-Powered Answers**: GPT-4 powered responses with context awareness
- 📊 **Page References**: Get exact page numbers for further reading
- 🎨 **Beautiful Interface**: Clean, intuitive Streamlit web interface
- ⚡ **Real-time Processing**: Live feedback during document indexing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  PDF Processing │────│ Vector Database │
│    (app.py)     │    │  (indexing.py)  │    │    (Qdrant)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                        ┌─────────────────┐
                        │   Chat System   │
                        │   (chat.py)     │
                        │   OpenAI GPT-4  │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Arshdeep00Kaur/RAG-Chat-Application.git
   cd RAG-Chat-Application
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Start the vector database**
   ```bash
   docker-compose up -d
   ```

5. **Launch the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📖 Usage

### Step 1: Upload PDF
- Click "Browse files" or drag & drop your PDF
- Wait for upload confirmation

### Step 2: Process Document
- Click "📚 Prepare this PDF" button
- System will extract text and create vector embeddings
- Wait for "✅ PDF processed and indexed!" message

### Step 3: Ask Questions
- Type your question in the text input field
- Get AI-powered answers with page references
- Ask follow-up questions about the same document

### Example Questions:
- "What is the main topic of this document?"
- "Can you summarize the key findings?"
- "What conclusions are drawn in chapter 3?"
- "Explain the methodology used in this research"

## 🔧 Technical Details

### System Components

#### 📄 **Document Processing** (`indexing.py`)
- **Text Extraction**: PyPDFLoader for robust PDF parsing
- **Chunking**: 1000 characters with 300 character overlap
- **Embeddings**: OpenAI's text-embedding-3-large model
- **Storage**: Qdrant vector database for efficient similarity search

```python
def run_indexing(uploaded_pdf_path):
    loader = PyPDFLoader(file_path=uploaded_pdf_path)
    doc = loader.load()
    
    # Text chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=300
    )
    split_doc = text_splitter.split_documents(documents=doc)
    
    # Vector embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Vector storage
    vector_store = QdrantVectorStore.from_documents(
        documents=split_doc,
        url="http://localhost:6333",
        collection_name="Learning_vectors",
        embedding=embeddings,
        force_recreate=True
    )
```

#### 💬 **Chat System** (`chat.py`)
- **Vector Search**: Retrieves top-3 most relevant document chunks
- **Context Building**: Combines search results with metadata
- **AI Model**: GPT-4.1 for intelligent response generation
- **Output**: Formatted answers with page references

#### 🎨 **Frontend** (`app.py`)
- **Framework**: Streamlit for rapid web development
- **UI**: Custom beige theme with intuitive controls
- **Features**: File upload, processing status, Q&A interface

### Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Chunk Size | 1000 chars | Optimal balance of context vs. precision |
| Chunk Overlap | 300 chars | Maintains context across boundaries |
| Embedding Model | text-embedding-3-large | 3072-dimensional vectors |
| Search Results | k=3 | Number of relevant chunks retrieved |
| Vector DB | Qdrant | High-performance vector similarity search |

## 📁 Project Structure

```
RAG-Chat-Application/
├── app.py                 # Streamlit web interface
├── indexing.py            # PDF processing and vector storage
├── chat.py                # Question answering system
├── docker-compose.yml     # Qdrant database setup
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Dependencies

### Core Libraries
```
streamlit>=1.28.0          # Web framework
langchain-community>=0.0.10 # Document processing
langchain-openai>=0.0.5    # OpenAI integration
langchain-qdrant>=0.0.1    # Vector database
langchain-text-splitters>=0.0.1 # Text processing
openai>=1.3.0              # OpenAI API client
pypdf>=3.17.0              # PDF processing
python-dotenv>=1.0.0       # Environment management
qdrant-client>=1.6.0       # Vector database client
```

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here
```

**⚠️ Important**: 
- Never commit your `.env` file to version control
- Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- The `.env` file is already included in `.gitignore`

## 🐳 Docker Configuration

The `docker-compose.yml` sets up Qdrant vector database:

```yaml
services:
  vector-db:
    image: qdrant/qdrant
    ports:
      - 6333:6333  # Qdrant web interface and API
```

Access Qdrant dashboard at `http://localhost:6333/dashboard`

## 🚨 Troubleshooting

### Common Issues

**1. Connection Error to Qdrant**
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Start Qdrant if not running
docker-compose up -d
```

**2. OpenAI Authentication Error**
```bash
# Verify API key is loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key loaded:', bool(os.getenv('OPENAI_API_KEY')))"
```

**3. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**4. PDF Processing Errors**
- Ensure PDF is not password-protected
- Try with a different PDF file
- Check file size (very large files may timeout)

### Debug Commands

```bash
# Check Qdrant health
curl http://localhost:6333/health

# View Qdrant collections
curl http://localhost:6333/collections

# Check application logs
streamlit run app.py --logger.level debug
```

## 📊 Performance

### Processing Times
- **PDF Upload**: Instant
- **Document Indexing**: ~2-5 seconds per page
- **Question Answering**: ~2-3 seconds per query

### Resource Usage
- **Memory**: ~100MB base + document size
- **Storage**: ~1KB per text chunk in Qdrant
- **API Costs**: ~$0.01 per document + ~$0.001 per question

## 🔮 Future Enhancements

- [ ] **Multi-document support** - Handle multiple PDFs simultaneously
- [ ] **Conversation history** - Maintain chat context across sessions
- [ ] **Advanced filtering** - Search by document sections or metadata
- [ ] **Export functionality** - Save conversations and answers
- [ ] **Custom model support** - Use different embedding/chat models
- [ ] **Batch processing** - Process multiple documents at once

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for document processing and AI integration
- **Qdrant** for high-performance vector search
- **OpenAI** for powerful embeddings and language models
- **Streamlit** for rapid web application development

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Made with ❤️ by Arshdeep Kaur**

> Transform your PDFs into conversational knowledge bases with GenieDocs!
