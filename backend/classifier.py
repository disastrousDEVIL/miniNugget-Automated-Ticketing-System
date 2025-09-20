from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

def classify_ticket(problem_text:str)->dict:
    llm=ChatOpenAI(model="gpt-4o-mini",temperature=0)


    system_prompt ="""
    You are a strict complaint classifier for Zomato Support.

    You must classify customer complaints into exactly ONE of these categories:

    - order_delayed
    - items_missing
    - agent_rude
    - order_not_received
    - order_quality_issue

    Rules for classification:
    1. Always choose the single best matching category. 
    2. If the complaint clearly belongs to a category, assign high confidence (0.8–1.0).
    3. If the complaint partially fits but has ambiguity, assign medium confidence (0.65–0.79).
    4. If the complaint barely fits or is unclear, assign low confidence (0.3–0.64).
    5. If the complaint does not match any category at all, assign confidence = 0.0.

    You must return ONLY valid JSON with keys:

    - type: one of the 5 categories
    - confidence: float between 0 and 1
    - extracted_items: list of item names that are explicitly reported as missing in the complaint (only if type = "items_missing", else [])
    Example output:
    {{
    "type": "items_missing",
    "confidence": 0.92,
    "extracted_items": ["Paneer Butter Masala", "Naan"]
    }}
    """
    examples = [
        {
            "complaint": "My order came 40 minutes late",
            "output": '{{"type": "order_delayed", "confidence": 0.9, "extracted_items": []}}'
        },
        {
            "complaint": "The fries and coke were missing from my order",
            "output": '{{"type": "items_missing", "confidence": 0.9, "extracted_items": ["fries", "coke"]}}'
        },    
        {
            "complaint": "I received the burger and fries but the coke was missing",
            "output": '{{"type": "items_missing", "confidence": 0.9, "extracted_items": ["coke"]}}'
        },
        {
            "complaint": "The delivery guy was extremely rude",
            "output": '{{"type": "agent_rude", "confidence": 0.95, "extracted_items": []}}'
        },
        {
            "complaint": "I didn’t receive my food at all",
            "output": '{{"type": "order_not_received", "confidence": 0.9, "extracted_items": []}}'
        },
        {
            "complaint": "The food was not good",
            "output": '{{"type": "order_quality_issue", "confidence": 0.9, "extracted_items": []}}'
        },
        {
            "complaint": "The coke was warm and the fries were soggy",
            "output": '{{"type": "order_quality_issue", "confidence": 0.6, "extracted_items": ["coke", "fries"]}}'
        },
        {
            "complaint": "I think something was missing but I’m not sure",
            "output": '{{"type": "items_missing", "confidence": 0.4, "extracted_items": []}}'
        },
        {
            "complaint": "The delivery was kind of slow but maybe due to traffic",
            "output": '{{"type": "order_delayed", "confidence": 0.5, "extracted_items": []}}'
        },
        {
            "complaint": "The guy seemed rude, but maybe he was just in a hurry",
            "output": '{{"type": "agent_rude", "confidence": 0.45, "extracted_items": []}}'
        },
        {
            "complaint": "I didn’t like the taste of the burger but maybe it’s just me",
            "output": '{{"type": "order_quality_issue", "confidence": 0.55, "extracted_items": ["burger"]}}'
        },
        {
            "complaint": "Not sure if my order is late or if I misread the estimated time",
            "output": '{{"type": "order_delayed", "confidence": 0.35, "extracted_items": []}}'
        }
    ]

    messages=[("system",system_prompt)]
    for ex in examples:
        messages.append(("human",ex["complaint"]))
        messages.append(("ai",ex["output"]))
    messages.append(("human","{complaint}"))

    prompt=ChatPromptTemplate.from_messages(messages)

    chain=prompt|llm
    result=chain.invoke({"complaint":problem_text})
    output=result.content.strip()
    output_dict = json.loads(output)  

    try: 
        data =output_dict 
        print(data) 
        print(f"[Classifier LOG] Complaint: {problem_text}") 
        return data 
        
    except Exception: 
        return { "type": None, "confidence": 0.0, "extracted_items": []}