from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_image(title, step, number) -> str:
    prompt='''Create a hyper realistic image for the cooking recipe step for a recipe {title} and the STEP is {step}. Focus more on the step for creating an image'''
    
    prompt = prompt.format(title=title, step=step)
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return [response.data[0].url, number]