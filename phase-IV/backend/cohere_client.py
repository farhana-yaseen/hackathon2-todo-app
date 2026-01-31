"""
Cohere API Client Utility
"""
import cohere
import os
from typing import Optional


class CohereClient:
    """
    Utility class to initialize and manage Cohere API client
    """
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)

    def get_client(self):
        """Returns the initialized Cohere client"""
        return self.client


# Global instance
cohere_client = CohereClient()