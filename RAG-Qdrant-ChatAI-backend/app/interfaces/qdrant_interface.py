from abc import ABC, abstractmethod
from typing import Dict, Any ,List,Optional

class QdrantInterface(ABC):

    @abstractmethod
    def create_collection(self, name: str) -> Any:
        pass

    @abstractmethod
    def insert_point(self, data: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def does_collection_exist(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def search_point(self, data: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def get_questions_answers_paginated(self, collection_name: str, limit: int = 25, offset: Optional[str] = None) -> Any:
        """
        Fetch Q&A pairs from a collection with pagination (scroll API).
        """
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> Any:
        pass

    @abstractmethod
    def bulk_qa_insert(self, qa_list : List, collection_name: str) -> Any:
        """Bulk insert multiple Q&A into Qdrant"""
        pass

    @abstractmethod
    def delete_questionById(self, collection_name : str, question_id: str) -> Any:
        """Bulk insert multiple Q&A into Qdrant"""
        pass


    @abstractmethod
    def update_point(self, collection_name: str, point_id: str, question: str, answer: str) -> Any:
        """Update/overwrite a Q&A point in Qdrant with new payload and regenerated vector"""
        pass

    @abstractmethod
    def get_total_qa(self, collection_name: str) -> int:
        """Return total number of Q&A stored in a given collection"""
        pass