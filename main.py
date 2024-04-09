import ast
import json 
import multiprocessing

from video2chat.llms.openai import OpenAILLM
from video2chat.memory.chromadb import ChromaDB
from video2chat.process_data.utils.read_transcripts import read_transcripts
from video2chat.utils.response_cleaner import response_cleaner
from video2chat.image_gen.image_generation import generate_image
from video2chat.utils.html_generator_util import html

llm = OpenAILLM()

COOKING_RECIPE_GENERATOR_PROMPT = """
You are an expert chef and cooking teacher. You have deep understanding of cooking, baking and teching making food.
Your job is to generate a cooking recipes.
Your Goals are as follows :
1) Create a recipe for the below query :
    {query}
2) You have to describe the recpie in steps with description of each step
3) INPUT you will be given
    You will get detailed 1 or multiple recipes like below example
    {recipe}
    
You will generate a recpie with the steps in the style of the given recipes. Do not change the style of cooking present in the given recipies - 

Always respond in the json format given below - 
{{
    "thought_on_cooking_style":"Think descriptively and include your thought on the overall cooking techniques and style of cooking",
    "thought_on_recipe":"Think carefully based on above examples and include your thought for making a recipie",
    "recipe":
        {{
            "title":"<Title of the recipe>",
            "description":"<Detailed Description of the Recipe>",
            "list_of_steps": [
                "step": "<Detailed description of the step>"
            ]
        }}
}}
"""

def chat_interface(chat_id, message) -> str:
    data = read_transcripts(f"chats/{chat_id}.json")
    messages = data["messages"]

    if len(messages) == 0:
        recipes = format_recipe_for_prompt(message)
        prompt = COOKING_RECIPE_GENERATOR_PROMPT.format(query=message, recipe=recipes)
        messages.append({
            "role": "user",
            "content": prompt
        })

    else:
        messages.append({
            "role": "user",
            "content": message
        })


    llm_response = llm.chat_completion(messages)
    llm_response = response_cleaner(llm_response)

    response_obj = ast.literal_eval(llm_response)

    messages.append({
        "role": "assistant",
        "content": llm_response
    })

    with open(f"chats/{chat_id}.json", "w") as f:
        json.dump(
            {
                "chat_id": chat_id,
                "messages": messages
            },
            f
        )
    data_for_image_gen = [
        [response_obj['recipe']['title'], step["step"], idx]
        for idx, step in enumerate(response_obj["recipe"]["list_of_steps"])
    ]
    with multiprocessing.Pool(processes=5) as pool:
        image_urls = pool.starmap(generate_image, data_for_image_gen)

    image_urls = sorted(image_urls, key=lambda x: x[1])
    images = [image[0] for image in image_urls]
    
    html(recipe_json=response_obj, image_urls=images, output_file_path=f"recipes/{chat_id}.html")
    
    return f"recipes/{chat_id}.html"

def format_recipe_for_prompt(query):
    recipes = get_cooking_recipes(query)
    print(recipes)
    recipe_prompt = ""
    for recipe_name, recipe_path in recipes:
        recipe_data = read_transcripts(recipe_path)
        recipe = recipe_data["dish_description"]
        for step in recipe_data["cooking_steps"]:
            recipe += f"\n {step['step_number']}: {step['description']}"
        
        recipe_prompt += recipe + "\n\n"
    
    return recipe_prompt

def get_cooking_recipes(query):
    data = query_cooking_vector_db(query)
    if data['distances'][0][0] < 0.13:
        return [(data['documents'][0][0], data['metadatas'][0][0]['path'])]

    if similar_recipes := [
        (data['documents'][0][idx], data['metadatas'][0][idx]['path'])
        for idx, similaity in enumerate(data['distances'][0])
        if similaity < 0.20
    ]:
        return similar_recipes
    else:
        return [
        (data['documents'][0][idx], data['metadatas'][0][idx]['path'])
        for idx, similaity in enumerate(data['distances'][0])
        if idx < 5
        ]

def query_cooking_vector_db(query):
    collection_name = "jacques_pepin_cooking"
    db = ChromaDB(collection_name=collection_name, embedding_model=None, text_field="dish_description")
    
    return db.get_matching_text(query, top_k=10)
        