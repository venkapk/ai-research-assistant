import os
import json
from typing import Dict, Any, Optional, Literal
from utils.logger import get_logger
from openai import OpenAI

# Logger
logger = get_logger()

# OpenAI API Key
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY environment variable is not set")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Entity type definition
EntityType = Literal["academic", "startup"]

def get_system_prompt(entity_type: EntityType) -> str:
    """
    Returns the appropriate system prompt based on entity type

    Args:
        entity_type: Either 'academic' or 'startup'

    Returns:
        The system prompt as a string
    """
    prompts = {
        "academic": (
            "You are a research assistant that identifies academic professionals based on their name and affiliation.\n\n"
            "Your task is to return structured, accurate, and current information about the academic's identity.\n\n"
            "Focus on:\n"
            "- Full name\n"
            "- Current affiliation\n"
            "- Current position/title\n"
            "- A short professional description (including research interests)\n"
            "- Confidence in the match\n\n"
            "Guidelines:\n"
            "- If multiple matches exist, return the most relevant one based on recency and academic profile completeness.\n"
            "- If no exact match is found, return the closest relevant match with a reduced confidence score.\n"
            "- If no match is found at all, return an empty object with \"confidence_score\": 0.\n\n"
            "Confidence Score Guide:\n"
            "- 100 = Exact match (name + affiliation + title verified)\n"
            "- 80-99 = High match (1 fuzzy detail, like abbreviated name or outdated title)\n"
            "- 50-79 = Partial match (multiple fields fuzzy or inferred)\n"
            "- 0 = No match found"
        ),
        "startup": (
            "You are a research assistant that identifies startup founders and their companies based on provided names or organization details.\n\n"
            "Your task is to return structured, accurate, and current information about the founder and their startup.\n\n"
            "Focus on:\n"
            "- Full name of the founder\n"
            "- Role in the startup\n"
            "- Startup name and description (what it does)\n"
            "- Current funding stage and any notable achievements (e.g., awards, acquisitions, press)\n"
            "- Confidence in the match\n\n"
            "Guidelines:\n"
            "- If multiple matches exist, return the most relevant one based on recency and profile completeness.\n"
            "- If no exact match is found, return the closest relevant match with a reduced confidence score.\n"
            "- If no match is found at all, return an empty object with \"confidence_score\": 0.\n\n"
            "Confidence Score Guide:\n"
            "- 100 = Exact match (founder + startup + role + stage verified)\n"
            "- 80-99 = High match (1 fuzzy detail, like outdated role or partial name)\n"
            "- 50-79 = Partial match (multiple fields fuzzy or inferred)\n"
            "- 0 = No match found"
        )
    }
    return prompts.get(entity_type, prompts["academic"])

def call_openai_api(system_prompt: str, user_prompt: str) -> Optional[str]:
    """
    Call the OpenAI API with the given prompts.
    
    Args:
        system_prompt: The system prompt for the AI
        user_prompt: The user prompt for the AI
        
    Returns:
        The API response content or None if there was an error
    """
    try:
        # logger.info(f"System prompt - Verification: {system_prompt}")
        # logger.info(f"User prompt - Verification: {user_prompt}")
        response = client.chat.completions.create(
            model="gpt-4o-search-preview", #gpt-4c
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # tools=[{
            #     "type": "web_search_preview",  
            # }]
            web_search_options={
                "search_context_size": "low"
            },
            # temperature=0.3,
            max_tokens=500
            # tool_choice="required"
        )
        # logger.info(f"Message: {response.choices[0].message}")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return None
    
def clean_json_response(content: str) -> str:
    """
    Clean JSON response by removing markdown code block formatting.
    
    Args:
        content: The response content potentially containing markdown code blocks
        
    Returns:
        Cleaned JSON string
    """
    # Check if content is None or empty
    if not content:
        return "{}"
    
    # Remove markdown code block formatting
    if content.strip().startswith("```"):
        first_line_end = content.find("\n")
        if first_line_end != -1:
            content = content[first_line_end + 1:]
            closing_ticks = content.rfind("```")
            if closing_ticks != -1:
                content = content[:closing_ticks]
        else:
            content = content.replace("```", "")
    
    # Find and extract JSON-like content if present
    json_start = content.find('{')
    json_end = content.rfind('}') + 1
    
    if json_start >= 0 and json_end > json_start:
        return content[json_start:json_end].strip()
    
    # Return original content if no JSON-like structure was found
    return content.strip()
    
def parse_entity_data(content: Optional[str], name: str, affiliation: str) -> Dict[str, Any]:
    """
    Parse the API response into a structured entity data dictionary.
    
    Args:
        content: The API response content
        name: The original name
        affiliation: The original affiliation
        
    Returns:
        A dictionary containing the parsed entity data
    """
    error_response = {
        "full_name": name,
        "affiliation": affiliation,
        "title": "Unverified",
        "brief_description": "Information could not be verified automatically.",
        "confidence_score": 0,
        "verification_status": "failed"
    }
    if not content:
        return error_response
    
    try:
        # Clean the content to handle markdown code blocks
        cleaned_content = clean_json_response(content)
        logger.info(f"Cleaned content: {cleaned_content}")
        
        # Parse the cleaned JSON
        result = json.loads(cleaned_content)
        
        # Validate required fields
        required_fields = ['full_name', 'affiliation', 'title', 'brief_description', 'confidence_score']
        for field in required_fields:
            if field not in result:
                result[field] = error_response[field]
        
        # Ensure confidence_score is numeric and is within the expected range
        try:
            result['confidence_score'] = float(result['confidence_score'])
            result['confidence_score'] = max(0, min(100, result['confidence_score']))
        except (ValueError, TypeError):
            logger.warning(f"Invalid confidence score format: {result.get('confidence_score')}")
            result['confidence_score'] = 0
        
        result['verification_status'] = "success"
        return result
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
        return {**error_response, "raw_response": content}

def verify_entity(name: str, affiliation: str, entity_type: EntityType) -> Dict[str, Any]:
    """
    Verify and identify the correct entity based on minimal information

    Args:
        name: The name of the person or entity
        affiliation: The institution or company affiliation\
        entity_type: Either 'academic' or 'startup'

    Returns:
        Dict containing entity information including name, affiliation, title, etc.
    """
    try:
        logger.info(f"Verifying entity: {name} from {affiliation} as {entity_type}")
        
        # System prompt based on entity type
        system_prompt = get_system_prompt(entity_type)

        # Prompt for the user
        user_prompt = f"""Find information about {name} from {affiliation}.
        
        Return a valid JSON object with EXACTLY the following fields:
        {{
            "full_name": "Complete name of the person or empty string if not found",
            "affiliation": "Current institution or company, or empty string if not found",
            "title": "Current position or role, or empty string if not found",
            "brief_description": "1–2 sentence summary including research area and academic focus",
            "confidence_score": "A number from 0–100 indicating match confidence"
        }}
        
        Return only the JSON object. Do not include any additional explanations or commentary.
        """

        # Call OpenAI API
        api_response = call_openai_api(system_prompt, user_prompt)
        logger.info(f"Verify API Response: {api_response}")

        # Parse API response
        result = parse_entity_data(api_response, name, affiliation)

        return result

    except Exception as e:
        logger.error(f"Entity verification error: {e}")
        return {
            "error": str(e),
            "full_name": name,
            "affiliation": affiliation,
            "title": "Error",
            "brief_description": "An error occurred during verification.",
            "confidence_score": 0
        }