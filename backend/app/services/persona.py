"""
Persona service for generating and managing AI personas
"""
import json
import uuid
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.services.llm import LLMService
from app.services.prompts import (
    PERSONA_GENERATION_SYSTEM_PROMPT,
    PERSONA_GENERATION_USER_PROMPT,
    validate_persona_response,
    create_persona_reaction_prompt,
    PERSONA_REACTION_SYSTEM_PROMPT,
    validate_reaction_response
)
from app.db.models import Persona, User
from app.schemas import PersonaResponse

logger = logging.getLogger(__name__)


class PersonaService:
    """Service for persona generation and management"""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def generate_personas(
        self,
        audience_description: str,
        user_id: int,
        db: Session,
        save_to_library: bool = True
    ) -> Dict[str, Any]:
        """
        Generate 5 AI personas based on audience description
        
        Args:
            audience_description: Description of target audience
            user_id: User ID for persona ownership
            db: Database session
            save_to_library: Whether to persist personas to database
        
        Returns:
            Dictionary with set_id and list of personas
        """
        logger.info(f"Generating personas for audience: {audience_description[:50]}...")
        
        # Create prompt
        messages = [
            {"role": "system", "content": PERSONA_GENERATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": PERSONA_GENERATION_USER_PROMPT.format(
                    audience_description=audience_description
                )
            }
        ]
        
        # Call LLM
        try:
            response = await self.llm_service.generate(messages, max_tokens=2000)
            content = response["content"]
            
            # Parse JSON response
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                data = json.loads(content.strip())
            
            # Validate response structure
            if not validate_persona_response(data):
                raise ValueError("Invalid persona response structure")
            
            personas_data = data["personas"]
            set_id = str(uuid.uuid4())
            
            # Save to database if requested
            if save_to_library:
                personas = []
                for persona_data in personas_data:
                    persona = Persona(
                        user_id=user_id,
                        set_id=set_id,
                        name=persona_data["name"],
                        archetype=persona_data["archetype"],
                        loyalty_level=persona_data["loyalty_level"],
                        core_values=persona_data["core_values"],
                        audience_description=audience_description
                    )
                    db.add(persona)
                    personas.append(persona)
                
                db.commit()
                
                for persona in personas:
                    db.refresh(persona)
                
                logger.info(f"Saved {len(personas)} personas to database with set_id: {set_id}")
            
            return {
                "set_id": set_id,
                "personas": personas_data,
                "audience_description": audience_description,
                "generation_cost": response["cost"],
                "generation_duration": response["duration"]
            }
        
        except Exception as e:
            logger.error(f"Error generating personas: {e}")
            raise
    
    async def generate_persona_reaction(
        self,
        persona: Dict[str, Any],
        content: str,
        audience_description: str
    ) -> Dict[str, Any]:
        """
        Generate a single persona's reaction to content
        
        Args:
            persona: Persona data dictionary
            content: Content to react to
            audience_description: Context about the audience
        
        Returns:
            Dictionary with reaction data
        """
        messages = [
            {"role": "system", "content": PERSONA_REACTION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": create_persona_reaction_prompt(
                    persona, content, audience_description
                )
            }
        ]
        
        try:
            response = await self.llm_service.generate(messages, max_tokens=800)
            content_response = response["content"]
            
            # Parse JSON
            try:
                data = json.loads(content_response)
            except json.JSONDecodeError:
                if "```json" in content_response:
                    content_response = content_response.split("```json")[1].split("```")[0]
                elif "```" in content_response:
                    content_response = content_response.split("```")[1].split("```")[0]
                data = json.loads(content_response.strip())
            
            # Validate response
            if not validate_reaction_response(data):
                raise ValueError("Invalid reaction response structure")
            
            return {
                "persona_id": persona.get("id"),
                "persona_name": persona["name"],
                "internal_monologue": data["internal_monologue"],
                "public_comment": data["public_comment"],
                "scores": data["scores"],
                "reasoning": data.get("reasoning"),
                "status": "success",
                "cost": response["cost"]
            }
        
        except Exception as e:
            logger.error(f"Error generating reaction for {persona['name']}: {e}")
            return {
                "persona_id": persona.get("id"),
                "persona_name": persona["name"],
                "status": "error",
                "error_message": str(e)
            }
    
    def get_persona_set(self, set_id: str, user_id: int, db: Session) -> Optional[List[Persona]]:
        """Retrieve a persona set from database"""
        personas = db.query(Persona).filter(
            Persona.set_id == set_id,
            Persona.user_id == user_id
        ).all()
        
        return personas if personas else None
    
    def list_persona_sets(
        self,
        user_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all persona sets for a user"""
        query = db.query(Persona).filter(Persona.user_id == user_id)
        
        if search:
            query = query.filter(Persona.audience_description.contains(search))
        
        personas = query.order_by(Persona.created_at.desc()).offset(skip).limit(limit * 5).all()
        
        # Group by set_id
        sets_dict = {}
        for persona in personas:
            if persona.set_id not in sets_dict:
                sets_dict[persona.set_id] = {
                    "set_id": persona.set_id,
                    "audience_description": persona.audience_description,
                    "created_at": persona.created_at,
                    "personas": []
                }
            sets_dict[persona.set_id]["personas"].append(persona)
        
        return list(sets_dict.values())[:limit]
    
    def delete_persona_set(self, set_id: str, user_id: int, db: Session) -> bool:
        """Delete a persona set"""
        deleted = db.query(Persona).filter(
            Persona.set_id == set_id,
            Persona.user_id == user_id
        ).delete()
        
        db.commit()
        return deleted > 0
