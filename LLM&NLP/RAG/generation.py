import logging
import os
import datetime
import requests
from bs4 import BeautifulSoup
from retrieve import SimpleRAG
from typing import List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebQuerier:
    def __init__(self):
        """Initialize the web querying system"""
        self.rag = SimpleRAG()
        self.output_dir = "query_results"
        os.makedirs(self.output_dir, exist_ok=True)

    def search_web(self, query: str) -> List[str]:
        """
        Search the web using Google
        
        Args:
            query: Search query
            
        Returns:
            List of search results
        """
        try:
            # Try multiple search URLs for better coverage
            urls = [
                f"https://www.google.com/search?q={query}",
                f"https://www.google.com/search?q={query}+definition",
                f"https://www.google.com/search?q={query}+explained"
            ]
            
            # Set up comprehensive headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
            
            all_results = []
            
            # Search using each URL
            for url in urls:
                try:
                    # Make the request
                    response = requests.get(url, headers=headers, timeout=10)
                    response.encoding = 'utf-8'  # Set encoding to UTF-8
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for different types of result containers
                    # 1. Standard search results
                    for div in soup.find_all(['div', 'p'], class_=['BNeawe', 'st', 'r', 'Z26q7c', 'UK95Uc']):
                        text = div.get_text(strip=True)
                        if text and len(text) > 50:
                            text = text.replace('\u202f', ' ')  # Replace problematic Unicode space
                            text = ' '.join(text.split())  # Normalize whitespace
                            all_results.append(text)
                    
                    # 2. Featured snippets
                    featured = soup.find('div', class_=['kp-header', 'g'])
                    if featured:
                        text = featured.get_text(strip=True)
                        if len(text) > 50:
                            all_results.append(text)
                    
                    # 3. Knowledge panels
                    knowledge = soup.find('div', class_=['kno-rdesc', 'kp-blk'])
                    if knowledge:
                        text = knowledge.get_text(strip=True)
                        if len(text) > 50:
                            all_results.append(text)
                            
                except Exception as e:
                    logger.debug(f"Error with URL {url}: {e}")
                    continue
            
            # Remove duplicates while preserving order
            seen = set()
            unique_results = []
            for result in all_results:
                if result not in seen:
                    seen.add(result)
                    unique_results.append(result)
            
            # Ensure we have meaningful results
            if not unique_results:
                # Try a simpler search as fallback
                response = requests.get(
                    f"https://www.google.com/search?q={query}+simple+explanation",
                    headers=headers
                )
                soup = BeautifulSoup(response.text, 'html.parser')
                for div in soup.find_all(['div', 'p']):
                    text = div.get_text(strip=True)
                    if len(text) > 50:
                        unique_results.append(text)
            
            # Log the number of results found
            logger.info(f"Found {len(unique_results)} unique results")
            
            # Return top results, prioritizing longer, more informative snippets
            return sorted(unique_results, key=len, reverse=True)[:5]
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return [f"Failed to search for '{query}'. Error: {str(e)}"]

    def process_query(self, query: str):
        """Process a user query through the system"""
        try:
            results = self.search_web(query)
            self.rag.add_documents(results)
            
            response = self.rag.chat(query)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # Use UTF-8 encoding when writing file
            with open(f"{self.output_dir}/result_{timestamp}.txt", "w", encoding='utf-8') as f:
                f.write(f"Query: {query}\n\n")
                f.write("Search Results:\n")
                f.write("-" * 50 + "\n")
                for i, result in enumerate(results, 1):
                    f.write(f"{i}. {result}\n\n")
                f.write("-" * 50 + "\n")
                f.write("\nGenerated Response:\n")
                f.write("-" * 50 + "\n")
                f.write(response)
            
            print(f"\nBot: {response}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            print("\nBot: Sorry, I encountered an error.")

def main():
    """Main function to run the chat system"""
    querier = WebQuerier()
    print("Welcome! Ask me anything (type 'exit' to quit)")
    
    while True:
        query = input("\nYou: ").strip()
        if query.lower() in ['exit', 'quit', 'bye']:
            break
        if query:
            querier.process_query(query)
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main() 
