#!/usr/bin/env python3
"""
Guía de Mejoras Específicas para LOCAL-RAG-JJ
Genera código de ejemplo y estructura recomendada
"""

import os
from pathlib import Path

def create_improved_structure():
    """Crea la estructura de directorios recomendada"""
    
    structure = {
        "src": {
            "api": ["__init__.py", "main.py", "routes.py", "dependencies.py"],
            "services": ["__init__.py", "rag_service.py", "document_service.py", "llm_service.py"],
            "repositories": ["__init__.py", "document_repository.py", "vector_repository.py"],
            "models": ["__init__.py", "document.py", "chat.py", "config.py"],
            "factories": ["__init__.py", "llm_factory.py"],
            "exceptions": ["__init__.py", "rag_exceptions.py"],
            "config": ["__init__.py", "settings.py"]
        },
        "tests": {
            "unit": ["__init__.py", "test_rag_service.py", "test_document_service.py"],
            "integration": ["__init__.py", "test_api.py", "test_rag_flow.py"],
            "fixtures": ["sample_documents.py"]
        },
        "docs": {
            "api": ["openapi.yaml"],
            "architecture": ["README.md", "patterns.md"],
            "deployment": ["docker.md", "kubernetes.md"]
        },
        "scripts": ["setup.py", "migrate.py", "deploy.sh"],
        "config": ["docker-compose.yml", "nginx.conf"]
    }
    
    return structure

def generate_improved_code_examples():
    """Genera ejemplos de código mejorado"""
    
    examples = {}
    
    # 1. Modelo de configuración
    examples["src/models/config.py"] = '''
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "ollama"
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Database Configuration
    db_dir: str = "./db"
    docs_dir: str = "./documents"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_tokens: int = 4000
    temperature: float = 0.6
    
    class Config:
        env_file = ".env"

settings = Settings()
'''
    
    # 2. Factory Pattern para LLMs
    examples["src/factories/llm_factory.py"] = '''
from abc import ABC, abstractmethod
from typing import Tuple, Any
from src.models.config import settings

class BaseLLMProvider(ABC):
    @abstractmethod
    def get_llm_and_embedding(self) -> Tuple[Any, Any]:
        pass

class OpenAIProvider(BaseLLMProvider):
    def get_llm_and_embedding(self):
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=settings.temperature,
            api_key=settings.openai_api_key
        )
        embedding = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key
        )
        return llm, embedding

class OllamaProvider(BaseLLMProvider):
    def get_llm_and_embedding(self):
        from langchain_ollama import OllamaLLM
        from langchain_community.embeddings import OllamaEmbeddings
        llm = OllamaLLM(model="llama3.2")
        embedding = OllamaEmbeddings(model="llama3.2")
        return llm, embedding

class LLMFactory:
    _providers = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        # Añadir más proveedores aquí
    }
    
    @classmethod
    def create_provider(cls, provider_name: str) -> BaseLLMProvider:
        if provider_name not in cls._providers:
            raise ValueError(f"Provider {provider_name} not supported")
        return cls._providers[provider_name]()
    
    @classmethod
    def get_llm_and_embedding(cls, provider_name: str = None):
        provider_name = provider_name or settings.llm_provider
        provider = cls.create_provider(provider_name)
        return provider.get_llm_and_embedding()
'''
    
    # 3. Repository Pattern
    examples["src/repositories/document_repository.py"] = '''
from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
from src.models.document import Document
from src.exceptions.rag_exceptions import DocumentNotFoundError, DocumentProcessingError

class DocumentRepositoryInterface(ABC):
    @abstractmethod
    def save_document(self, document: Document) -> str:
        pass
    
    @abstractmethod
    def get_document(self, document_id: str) -> Optional[Document]:
        pass
    
    @abstractmethod
    def list_documents(self) -> List[Document]:
        pass
    
    @abstractmethod
    def delete_document(self, document_id: str) -> bool:
        pass

class FileSystemDocumentRepository(DocumentRepositoryInterface):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def save_document(self, document: Document) -> str:
        try:
            file_path = self.base_path / document.filename
            with open(file_path, 'wb') as f:
                f.write(document.content)
            return str(file_path)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to save document: {str(e)}")
    
    def get_document(self, document_id: str) -> Optional[Document]:
        try:
            file_path = self.base_path / document_id
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            return Document(
                filename=document_id,
                content=content,
                size=len(content)
            )
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get document: {str(e)}")
    
    def list_documents(self) -> List[Document]:
        documents = []
        for file_path in self.base_path.glob("*.pdf"):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                documents.append(Document(
                    filename=file_path.name,
                    content=content,
                    size=len(content)
                ))
            except Exception:
                continue  # Skip corrupted files
        return documents
    
    def delete_document(self, document_id: str) -> bool:
        try:
            file_path = self.base_path / document_id
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete document: {str(e)}")
'''
    
    # 4. Service Layer
    examples["src/services/rag_service.py"] = '''
from typing import Dict, Any
import logging
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_retrieval_chain

from src.factories.llm_factory import LLMFactory
from src.repositories.document_repository import DocumentRepositoryInterface
from src.services.document_service import DocumentService
from src.exceptions.rag_exceptions import RAGProcessingError, LLMConnectionError
from src.models.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(
        self, 
        document_repository: DocumentRepositoryInterface,
        document_service: DocumentService
    ):
        self.document_repository = document_repository
        self.document_service = document_service
        self.llm, self.embedding = LLMFactory.get_llm_and_embedding()
        self.session_store: Dict[str, ChatMessageHistory] = {}
    
    def process_document(self, filename: str) -> bool:
        """Procesa un documento y lo añade a la base vectorial"""
        try:
            # Obtener documento del repositorio
            document = self.document_repository.get_document(filename)
            if not document:
                raise RAGProcessingError(f"Document {filename} not found")
            
            # Procesar documento
            docs = self.document_service.load_and_split_document(
                f"{settings.docs_dir}/{filename}"
            )
            
            # Crear/actualizar base vectorial
            db = Chroma.from_documents(
                persist_directory=settings.db_dir,
                documents=docs,
                embedding=self.embedding
            )
            
            logger.info(f"Document {filename} processed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")
            raise RAGProcessingError(f"Failed to process document: {str(e)}")
    
    def query(self, user_input: str, session_id: str = "default") -> str:
        """Procesa una consulta usando RAG"""
        try:
            if not self.llm or not self.embedding:
                return self._demo_response(user_input)
            
            # Obtener retriever
            db = Chroma(
                persist_directory=settings.db_dir, 
                embedding_function=self.embedding
            )
            retriever = db.as_retriever()
            
            # Crear cadena RAG con historial
            history_aware_retriever = self.document_service.build_history_aware_retriever(
                self.llm, retriever
            )
            qa_chain = self.document_service.build_qa_chain(self.llm)
            rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)
            
            # Configurar historial de conversación
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
            )
            
            # Procesar consulta
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            
            return response["answer"]
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise RAGProcessingError(f"Failed to process query: {str(e)}")
    
    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Obtiene o crea el historial de una sesión"""
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
        return self.session_store[session_id]
    
    def _demo_response(self, user_input: str) -> str:
        """Respuesta demo cuando no hay LLM configurado"""
        return f"Demo mode: Your question was '{user_input}'. Configure a real LLM for AI responses."
    
    def clear_session(self, session_id: str) -> bool:
        """Limpia el historial de una sesión"""
        if session_id in self.session_store:
            del self.session_store[session_id]
            return True
        return False
'''
    
    # 5. Excepciones personalizadas
    examples["src/exceptions/rag_exceptions.py"] = '''
class RAGException(Exception):
    """Base exception for RAG-related errors"""
    pass

class DocumentProcessingError(RAGException):
    """Raised when document processing fails"""
    pass

class DocumentNotFoundError(RAGException):
    """Raised when a document is not found"""
    pass

class LLMConnectionError(RAGException):
    """Raised when LLM connection fails"""
    pass

class RAGProcessingError(RAGException):
    """Raised when RAG processing fails"""
    pass

class InvalidConfigurationError(RAGException):
    """Raised when configuration is invalid"""
    pass
'''
    
    # 6. API mejorada con manejo de errores
    examples["src/api/main.py"] = '''
import logging
from fastapi import FastAPI, File, UploadFile, Request, WebSocket, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.services.rag_service import RAGService
from src.services.document_service import DocumentService
from src.repositories.document_repository import FileSystemDocumentRepository
from src.exceptions.rag_exceptions import RAGException, DocumentProcessingError
from src.models.config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar FastAPI
app = FastAPI(
    title="LOCAL-RAG-JJ API",
    description="RAG Chatbot API with multiple LLM providers",
    version="2.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates y archivos estáticos
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Dependency injection
def get_document_repository():
    return FileSystemDocumentRepository(settings.docs_dir)

def get_document_service():
    return DocumentService()

def get_rag_service(
    doc_repo: FileSystemDocumentRepository = Depends(get_document_repository),
    doc_service: DocumentService = Depends(get_document_service)
):
    return RAGService(doc_repo, doc_service)

# Exception handlers
@app.exception_handler(RAGException)
async def rag_exception_handler(request: Request, exc: RAGException):
    logger.error(f"RAG Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": f"RAG Error: {str(exc)}"}
    )

@app.exception_handler(DocumentProcessingError)
async def document_exception_handler(request: Request, exc: DocumentProcessingError):
    logger.error(f"Document Processing Error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"message": f"Document Error: {str(exc)}"}
    )

# Routes
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    rag_service: RAGService = Depends(get_rag_service)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Guardar archivo
        contents = await file.read()
        document = Document(
            filename=file.filename,
            content=contents,
            size=len(contents)
        )
        
        # Procesar documento
        success = await rag_service.process_document(file.filename)
        
        if success:
            return {"message": f"Document {file.filename} uploaded and processed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to process document")
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chatting", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})

@app.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    rag_service: RAGService = Depends(get_rag_service)
):
    await websocket.accept()
    session_id = "default"  # En producción, generar ID único
    
    try:
        while True:
            user_input = await websocket.receive_text()
            response = await rag_service.query(user_input, session_id)
            await websocket.send_text(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
'''
    
    return examples

def main():
    """Función principal para generar la guía de mejoras"""
    
    print("="*60)
    print("GUÍA DE MEJORAS PARA LOCAL-RAG-JJ")
    print("="*60)
    
    print("\n1. ESTRUCTURA RECOMENDADA:")
    print("-" * 30)
    structure = create_improved_structure()
    
    def print_structure(struct, indent=0):
        for key, value in struct.items():
            print("  " * indent + f"📁 {key}/")
            if isinstance(value, dict):
                print_structure(value, indent + 1)
            elif isinstance(value, list):
                for item in value:
                    print("  " * (indent + 1) + f"📄 {item}")
    
    print_structure(structure)
    
    print("\n2. EJEMPLOS DE CÓDIGO MEJORADO:")
    print("-" * 30)
    examples = generate_improved_code_examples()
    
    for filename, code in examples.items():
        print(f"\n📄 {filename}:")
        print("```python")
        print(code.strip())
        print("```")
    
    print("\n3. COMANDOS DE MIGRACIÓN:")
    print("-" * 30)
    print("""
# 1. Crear nueva estructura
mkdir -p src/{api,services,repositories,models,factories,exceptions,config}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{api,architecture,deployment}
mkdir -p scripts config

# 2. Mover archivos existentes
mv app/main.py src/api/main.py
mv app/utils.py src/services/document_service.py

# 3. Crear archivos de configuración
touch src/__init__.py
touch tests/__init__.py
touch docs/README.md

# 4. Instalar dependencias adicionales
pip install pydantic[dotenv] pytest pytest-asyncio httpx
    """)
    
    print("\n4. PRÓXIMOS PASOS:")
    print("-" * 30)
    print("""
1. ✅ Implementar la nueva estructura de directorios
2. ✅ Crear modelos de configuración con Pydantic
3. ✅ Implementar Factory Pattern para LLMs
4. ✅ Crear Repository Pattern para documentos
5. ✅ Implementar Service Layer para RAG
6. ✅ Añadir manejo robusto de excepciones
7. ✅ Crear pruebas unitarias
8. ✅ Documentar API con OpenAPI
9. ✅ Implementar logging estructurado
10. ✅ Configurar CI/CD pipeline
    """)

if __name__ == "__main__":
    main()