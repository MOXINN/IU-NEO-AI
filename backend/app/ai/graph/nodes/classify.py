"""
IU NWEO AI — LangGraph Classification Node
Maintainer: Architect
"""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from app.ai.models.gemini import get_gemini_pro_model
from app.ai.graph.state import AgentState

# We use the non-streaming model for quick classification output in JSON format
# Note: Google's GenAI doesn't strictly adhere to format enforcements blindly yet, so we prompt heavily
class_llm = get_gemini_pro_model(temperature=0.0, streaming=False)

CLASSIFY_PROMPT = """You are an intent classification agent for a University Chatbot.
Analyze the user's latest query and determine the best route to find an answer.
Respond with a JSON object containing exactly two keys:
1. "intent": string. Choose one of:
   - "academic": general university courses, curriculum.
   - "administrative": fees, admissions, schedules.
   - "prerequisite": specific questions about "what is required before course X" or dependencies.
   - "greeting": general say hello.
   - "unknown": if you do not understand.
2. "confidence": float between 0.0 and 1.0.

User Query: {query}
"""

async def classify_intent_node(state: AgentState) -> AgentState:
    """
    Classifies the user query by extracting the intent.
    Updates the 'intent' and 'confidence' in the AgentState.
    """
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""

    prompt_text = CLASSIFY_PROMPT.format(query=last_message)
    response = await class_llm.ainvoke(prompt_text)
    
    # Simple parse - assuming the LLM obeys JSON formatting
    # In production, use langchain's OutputParser with retry logic
    try:
        # Quick cleanup just in case there are markdown blocks
        clean_text = response.content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_text)
        
        intent = parsed.get("intent", "unknown")
        confidence = float(parsed.get("confidence", 0.0))
    except Exception:
        intent = "unknown"
        confidence = 0.0

    return {"intent": intent, "confidence": confidence}
