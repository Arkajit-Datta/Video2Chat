# Video2Chat
Analyses your Video and gives an interface to chat with. Powers with a RAG based system to query on the provided information, this makes an intelligent engine to solve all the queries. 

## 1. Acquire Data
donwload the video using download_video.py - downloads 102 videos from youtube
Transcribe the video using  transcribe_video.py  

## 2. Preprocess Data

Extract the steps of cooking using extract_cooking_steps_images.py
Also extracts when the cooking step was being discussed 
video_processor.py extracts images/ screenshots from the youtube video 
All the data is processed and kept in processes data folder 

## 3. Build RAG
chromadb with openai embeddings is used to create the RAG
implementation of the RAG is stored in memory folder > chromadb.py
Building the RAG > implementation in test.py > building_cooking_vector_db.py
It stores an intelligent concatenation of VideoName + Dish Description (extracted from GPT ) as the key the value/ metadata is path of the json file for the cooking steps 

Query the RAG > implemented in the test.py > Gets top_k matches from the vector db 

db is persistent placed in memory>db>chroma>chroma.sqlite3

## 4.Chat Interface 
### How to set it up 

- Install the requirements
`pip install -r requirements.txt`

- Create a .env with the following keys
`OPENAI_API_KEY=""`
`DEEPGRAM_API_KEY=""`
`GOOGLE_CLOUD_API_KEY=""`
`ANYSCALE_API_KEY=""`

- Running the fastapi server 
`python app.py` 

- Returns
`.html file path`


## 5. Handles multiple recipe and combines to cook for you
- According to the user query it finds the relevant dishes stored in the vectordb
    - If there is a match below the threshold 0.15 then we conclude the same dish is stored in the db hence we return 1
    - Else it returns all the dishes getting matches with a threshold of 0.20 and less 
    - All the dishes with steps are passed to gpt in a prompt to create a custom dish if required
    - Images are generated using Dalle-3 for each step 
    - Html file is rendered as a result 

