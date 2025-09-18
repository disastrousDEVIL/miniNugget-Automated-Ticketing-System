from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
from langchain_core.messages import SystemMessage, HumanMessage

llm=ChatOpenAI(model="gpt-4o",temperature=0)

def extract_image_text(image_url:str)->list:
    # template = ChatPromptTemplate.from_messages([
    #     ("system",
    #      """You are an OCR + food item extractor.
    #      Look at the provided image. It may be a receipt or a food picture.

    #      Extract and return ONLY a JSON list of the items that are present 
    #      in the image. Do not guess missing items.

    #      Example output:
    #      ["burger", "fries", "coke"]"""
    #     ),
    #     ("human", "{image_input}")
    # ])
    messages = [
        SystemMessage(
            content="""You are an OCR + food item extractor.
            Look at the provided image. It may be a receipt or a food picture.

            Extract and return ONLY a JSON list of the items that are present 
            in the image. Do not guess missing items.

            Example output:
            ["burger", "fries", "coke"]"""
        ),
        HumanMessage(content=[
            {"type": "text", "text": "Extract items from this image."},
            {"type": "image_url", "image_url":{"url": image_url}}
        ])
    ]
    # prompt = template.format_messages(
    #     image_input={"type": "image_url", "image_url": image_url}
    # )
    response = llm.invoke(messages)
    text = response.content.strip()
    # print(response.content)
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "").replace("json", "").strip()
        print(text)
    try:
        items = json.loads(text)
        if isinstance(items, list):
            return items
    except Exception:
        pass

    return []

def classify_and_validate(image_url:str,missing_items:list)->tuple[float,str]:
    extracted_items=extract_image_text(image_url)
    print(extracted_items)
    if not extracted_items:
        return -1.0,"no"
    found_matches = set(extracted_items) & set(missing_items)
    if found_matches:
        return 0.3,"yes"
    else:
        return 0.95,"yes"

