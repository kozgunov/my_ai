import torch
import logging
import os
from typing import List, Dict, Optional
import numpy as np
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Document:
    """Simple document class to store text content and its embedding"""
    content: str  # The actual text content
    embedding: Optional[np.ndarray] = None  # Vector representation of the text

class SimpleRAG:
    def __init__(self):
        """
        Initialize the RAG (Retrieval-Augmented Generation) system
        Sets up BERT model for both embeddings and text generation
        """
        # Load the BERT model and tokenizer
        model_name = "bert-base-uncased"  # Using basic BERT model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)  # For converting text to tokens
        self.model = AutoModel.from_pretrained(model_name)  # The BERT model itself
        self.model.eval()  # Set model to evaluation mode (no training)
        
        # Initialize empty document storage
        self.documents = []  # Will store Document objects
        
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Convert text to its vector representation using BERT
        
        Args:
            text: Input text to embed
            
        Returns:
            numpy array of embeddings
        """
        # Tokenize the input text
        inputs = self.tokenizer(
            text,
            max_length=512,  # Maximum sequence length
            truncation=True,  # Cut off if too long
            padding=True,  # Add padding if too short
            return_tensors="pt"  # Return PyTorch tensors
        )
        
        # Generate embeddings without gradient calculation
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Average the last hidden states to get a single vector
            embedding = outputs.last_hidden_state.mean(dim=1)
            return embedding.squeeze().numpy()

    def add_documents(self, texts: List[str]):
        """
        Add new documents to the knowledge base
        
        Args:
            texts: List of text documents to add
        """
        for text in texts:
            # Get embedding for each text
            embedding = self.get_embedding(text)
            # Create and store Document object
            doc = Document(content=text, embedding=embedding)
            self.documents.append(doc)
        logger.info(f"Added {len(texts)} documents")

    def get_relevant_docs(self, query: str, k: int = 3) -> List[Document]:
        """
        Find most relevant documents for a query using cosine similarity
        
        Args:
            query: Search query
            k: Number of documents to return
            
        Returns:
            List of most relevant Document objects
        """
        if not self.documents:
            return []
            
        # Get embedding for the query
        query_embedding = self.get_embedding(query)
        
        # Calculate similarity with each document
        similarities = []
        for doc in self.documents:
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                doc.embedding.reshape(1, -1)
            )[0][0]
            similarities.append(similarity)
        
        # Get indices of top k most similar documents
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [self.documents[i] for i in top_indices]

    def generate_response(self, query: str, context_docs: List[Document]) -> str:
        """Generate a comprehensive response based on the query and relevant documents"""
        if not context_docs:
            return "I don't have enough information to answer that question."
            
        try:
            # Combine all relevant information
            all_info = []
            for doc in context_docs:
                # Clean and split the content into sentences
                sentences = [s.strip() for s in doc.content.split('.') if s.strip()]
                all_info.extend(sentences)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_info = [x for x in all_info if not (x in seen or seen.add(x))]
            
            # Create a comprehensive response
            response_parts = []
            
            # Add introduction
            response_parts.append(f"Based on the available information about '{query}':")
            
            # Add main points
            for i, info in enumerate(unique_info, 1):
                if len(info) > 20:  # Filter out very short fragments
                    response_parts.append(f"{i}. {info}")
            
            # Add conclusion
            if len(response_parts) > 1:
                response_parts.append("\nThis information is compiled from multiple sources and represents the most relevant details found.")
            else:
                response_parts.append("\nI found limited information about this topic.")
            
            # Combine all parts
            final_response = "\n".join(response_parts)
            
            # Ensure the response isn't too long
            if len(final_response) > 1000:
                final_response = final_response[:997] + "..."
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while generating the response."

    def chat(self, query: str) -> str:
        """
        Main chat function that combines retrieval and response generation
        
        Args:
            query: User's question
            
        Returns:
            Generated response
        """
        try:
            # Get relevant documents for the query
            relevant_docs = self.get_relevant_docs(query)
            
            # Generate and return response
            response = self.generate_response(query, relevant_docs)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I encountered an error while processing your query."
