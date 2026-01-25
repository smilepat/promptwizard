import re
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class BaseValidator(ABC):
    """Abstract base class for all validators."""
    
    def __init__(self, name: str, description: str = "", failure_message: str = "Validation failed"):
        self.name = name
        self.description = description
        self.failure_message = failure_message

    @abstractmethod
    def validate(self, content: str) -> bool:
        """
        Validate the content.
        Returns:
            bool: True if validation passes, False otherwise.
        """
        pass

    def get_error_message(self) -> str:
        return self.failure_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "description": self.description
        }


class RegexValidator(BaseValidator):
    """Validates if content matches a regex pattern."""
    
    def __init__(self, pattern: str, name: str = "Regex Check", description: str = "", failure_message: str = "Format mismatch"):
        super().__init__(name, description, failure_message)
        self.pattern = pattern

    def validate(self, content: str) -> bool:
        return bool(re.search(self.pattern, content, re.MULTILINE | re.DOTALL))


class KeywordValidator(BaseValidator):
    """Validates presence (or absence) of keywords."""
    
    def __init__(self, keywords: List[str], must_include: bool = True, name: str = "Keyword Check", description: str = "", failure_message: str = "Keyword validation failed"):
        super().__init__(name, description, failure_message)
        self.keywords = keywords
        self.must_include = must_include

    def validate(self, content: str) -> bool:
        content_lower = content.lower()
        found_keywords = [k for k in self.keywords if k.lower() in content_lower]
        
        if self.must_include:
            # All keywords must be present
            return len(found_keywords) == len(self.keywords)
        else:
            # No keywords must be present
            return len(found_keywords) == 0


class JsonSchemaValidator(BaseValidator):
    """Validates if content is valid JSON and optionally matches a schema."""
    
    def __init__(self, schema: Optional[Dict] = None, name: str = "JSON Check", description: str = "", failure_message: str = "Invalid JSON"):
        super().__init__(name, description, failure_message)
        self.schema = schema

    def validate(self, content: str) -> bool:
        try:
            # Try to find JSON block if wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = content
                
            data = json.loads(json_str)
            
            # TODO: Add schema validation (requires jsonschema lib, but sticking to stdlib for now)
            # if self.schema:
            #     validate(instance=data, schema=self.schema)
            
            return True
        except json.JSONDecodeError:
            return False
        except Exception:
            return False
