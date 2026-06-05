import httpx
from bs4 import BeautifulSoup
from src.utils.exceptions import ScrapingException

class ScraperService:
    @staticmethod
    async def fetch_and_clean(url: str) -> str:
        # Standard User-Agent header to minimize request rejections by target servers
        headers = {
            "User-Agent": "AuraWebScraper/1.0 (contact: karthii.71116@gmail.com)"
        }
        
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    raise ScrapingException("Target website blocked request (Anti-bot block detected).")
                raise ScrapingException(f"HTTP error occurred while fetching page: {e.response.status_code}")
            except httpx.RequestError as e:
                raise ScrapingException(f"Failed to connect to target webpage: {str(e)}")

        try:
            # Parse HTML and execute noise reduction to minimize token costs
            soup = BeautifulSoup(response.text, "html.parser")
            
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "svg", "noscript", "iframe"]):
                element.decompose()

            # Extract clean, normalized plain text
            text = soup.get_text(separator=" ")
            cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned_text = " ".join(cleaned_lines)
            
            if not cleaned_text:
                raise ScrapingException("No readable text content found on the webpage.")
                
            return cleaned_text
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise e
            raise ScrapingException(f"Failed to parse and clean HTML: {str(e)}")