import os
import json
from datetime import datetime
from utils.logger import get_logger
from typing import Optional, Literal
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
    "academic": """You are a research assistant tasked with generating structured, detailed research profiles for academic professionals.
    
    Your objective is to gather factual, well-sourced, and relevant data that would support academic grant writing and collaboration strategy.
    
    Focus Areas:
    1. Current and past research focus areas
    2. Notable publications and projects
    3. Academic or industry collaborations and affiliations
    4. Previous grants or research funding
    5. Public mentions or recognition (e.g., news, awards)
    6. Strategic insights to support grant planning
    
    Guidelines:
    - Use only verifiable data from credible sources (e.g., university websites, Google Scholar, Scopus, ORCID, funding agency databases).
    - Do not guess or fabricate insights. If a section has fewer than 3 items, include only what is known.
    - Include exactly the fields defined in the JSON schema. Return an empty array for any category where data could not be verified.
    """,
    
    "startup": """You are a research assistant tasked with generating structured, detailed profiles for startup founders and their companies.
    
    Your objective is to gather factual, well-sourced, and relevant data that would support funding strategy and strategic alignment.
    Focus Areas:
    1. Business focus areas and market positioning
    2. Products, services, and technological innovations
    3. Strategic partnerships and industry collaborations
    4. Previous funding rounds, grants, and investors
    5. Public mentions or recognition (e.g., press coverage, awards, accelerators)
    6. Strategic insights to support investment pitches or partnership outreach
    Guidelines:
    - Use only verifiable data from credible sources (e.g., Crunchbase, company websites, press releases, LinkedIn, funding databases).
    - Do not guess or fabricate insights. If a section has fewer than 3 items, include only what is known.
    - Include exactly the fields defined in the JSON schema. Return an empty array for any category where data could not be verified.
    """
    }
    return prompts.get(entity_type, prompts["academic"])

def get_user_prompt(name, title, affiliation):
    user_prompt = f"""Provide detailed research on {name}, {title} at {affiliation}.

    All data must be specifically linked to this person. Do not include information about the general research at {affiliation} unless it is explicitly tied to {name}'s work.
    
    Return a valid JSON object with EXACTLY the following structure:
    {{
        "research_focus": [
            "Focus area 1",
            "Focus area 2"
        ],
        "projects_publications": [
            "Project or publication 1",
            "Project or publication 2"
        ],
        "institutional_connections": [
            "Collaborator or institution 1",
            "Collaborator or institution 2"
        ],
        "funding_history": [
            "Funding agency, project name, year (if known)"
        ],
        "public_mentions": [
            "Mention or recognition 1"
        ],
        "strategic_insights": [
            "Insight derived from verified information to support grants or partnerships"
        ]
    }}
    - Include 3–7 items per field if available. Return fewer if needed, but do not generate unverifiable data.
    - All information must be accurate, specific, and relevant.
    - Return only the JSON object. Do not include any extra explanations.
    """
    return user_prompt

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
        # logger.info(f"System prompt - Research: {system_prompt}")
        # logger.info(f"User prompt - Research: {user_prompt}")
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return None

def generate_research(entity_info, entity_type: EntityType):
    """
    Generate comprehensive research based on the verified entity

    Args:
        entity_info (dict): Information about the entity
        entity_type: Either 'academic' or 'startup'
    
    Returns:
        dict: Comprehensive research information
    """
    try:

        # Extract entity information
        name = entity_info.get('full_name', '')
        affiliation = entity_info.get('affiliation', '')
        title = entity_info.get('title', '')

        logger.info(f"Generating research for: {name} from {affiliation}")

        # System prompt based on entity type
        system_prompt = get_system_prompt(entity_type)

        # User prompt
        user_prompt = get_user_prompt(name, title, affiliation)

         # Call OpenAI API
        api_response = call_openai_api(system_prompt, user_prompt)
        # logger.info(f"Research API Response: {api_response}")
        content = api_response
        
        # Attempt to parse as JSON
        try:
            # Find the JSON object in the response (in case there's any extra text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = content[json_start:json_end]
                result = json.loads(json_content)
                
                # Ensure all required sections exist
                required_sections = [
                    'research_focus', 
                    'projects_publications', 
                    'institutional_connections',
                    'funding_history',
                    'public_mentions',
                    'strategic_insights'
                ]
                
                for section in required_sections:
                    if section not in result or not isinstance(result[section], list):
                        result[section] = ["Information not available"]
                
                # Add metadata
                result['entity_type'] = entity_type
                result['generated_at'] = datetime.now().isoformat()
                
                return result
            else:
                # Return a structured fallback if JSON extraction fails
                return create_fallback_research(entity_type)
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in research generation: {e}")
            return create_fallback_research(entity_type)
            
    except Exception as e:
        logger.error(f"Research generation error: {e}")
        return {
            "error": str(e),
            "research_focus": ["Error generating research"],
            "projects_publications": ["Error generating research"],
            "institutional_connections": ["Error generating research"],
            "funding_history": ["Error generating research"],
            "public_mentions": ["Error generating research"],
            "strategic_insights": ["Error generating research"]
        }

def create_fallback_research(entity_type: EntityType):
    """Create a fallback research structure if the AI response can't be parsed"""
    logger.info(f"Creating fallback research for entity type: {entity_type}")
    
    fallback = {
        "entity_type": entity_type,
        "generated_at": datetime.now().isoformat()
    }
    
    if entity_type == "academic":
        fallback.update({
            "research_focus": [
                "Research interests could not be automatically determined",
                "Consider reviewing their institutional profile or academic publications"
            ],
            "projects_publications": [
                "Publication information could not be automatically retrieved",
                "Check academic databases like Google Scholar or ResearchGate"
            ],
            "institutional_connections": [
                "Institutional connections could not be automatically mapped",
                "Consider reviewing their CV or institutional biography"
            ],
            "funding_history": [
                "Funding history could not be automatically retrieved",
                "Check institutional grant databases or academic profiles"
            ],
            "public_mentions": [
                "Public mentions could not be automatically collected",
                "Consider a manual search in academic news sources"
            ],
            "strategic_insights": [
                "Consider aligning grant applications with their known research interests",
                "Explore potential collaborative opportunities based on complementary expertise",
                "Review successful grants in their field for strategic approaches"
            ]
        })
    else:
        fallback.update({
            "research_focus": [
                "Business focus areas could not be automatically determined",
                "Consider reviewing their company website or LinkedIn profile"
            ],
            "projects_publications": [
                "Product information could not be automatically retrieved",
                "Check their company website or industry databases"
            ],
            "institutional_connections": [
                "Industry connections could not be automatically mapped",
                "Consider reviewing their LinkedIn profile or company partnerships"
            ],
            "funding_history": [
                "Funding history could not be automatically retrieved",
                "Check startup databases like Crunchbase or PitchBook"
            ],
            "public_mentions": [
                "Public mentions could not be automatically collected",
                "Consider a manual search in business news sources"
            ],
            "strategic_insights": [
                "Consider examining market fit and differentiation factors",
                "Explore potential investment opportunities based on growth trajectory",
                "Review successful startups in their sector for strategic approaches"
            ]
        })
    
    logger.debug(f"Created fallback research: {fallback}")
    return fallback