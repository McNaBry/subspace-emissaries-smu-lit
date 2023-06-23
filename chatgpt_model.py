# -*- coding: utf-8 -*-
from llama_index import (
    SimpleDirectoryReader, 
    GPTListIndex, 
    VectorStoreIndex, 
    LLMPredictor, 
    PromptHelper,
    ServiceContext,
    StorageContext,
    load_index_from_storage
)
from langchain.chat_models import ChatOpenAI
import openai
import gradio as gr
import time
import sys
import os
import re
import database_interaction as db
import random

# Function that construct the index which serves as the "container" for our trained model
def construct_index(directory_path):
    # Load in the custom data (Raw data)
    # Data will be stored in a Document - Lightweight container around the data source
    documents = SimpleDirectoryReader(directory_path).load_data()

    # Parameters for prompt helper
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 0.2
    chunk_size_limit = 600

    prompt_helper = PromptHelper(
        max_input_size, num_outputs, 
        max_chunk_overlap, chunk_size_limit=chunk_size_limit
    )
    # The LLM model that will leverage chatGPT 3.5 turbo to train on custom data
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs
        )
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, chunk_size=512
    )

    # Construction of index from source data
    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context, 
        llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )
    
    # Persist index to disk for later usage
    index.set_index_id("vector_index")
    index.storage_context.persist('./storage')

    return index

valid_tags = ["family", "civil", "criminal", "incapacity", "inheritance"]

# Function that accept the prompt (input text) and the language choice
def query_chatbot(input_text, language="en"):
    str_tags = ", ".join(valid_tags)

    modified_input = (
        f'{input_text}'
        'Append the specific field of law from the list of "{valid_tags}" within "{}" at the end of your entire response. '
        'If there is none relevant, choose "{N/A}"'
    )

    print("MODIFIED INPUT", modified_input)
    # Load in index from memory
    # Must match what was set in construct_index()
    storage_context = StorageContext.from_defaults(persist_dir='storage')
    index = load_index_from_storage(storage_context, index_id="vector_index")

    # Create the query engine
    query_engine = index.as_query_engine()
    # Pass in the prompt to the query engine
    response = query_engine.query(modified_input)

    raw_res = response.response
    # Search for all possible tags that chatGPT added within curly braces
    tags = re.findall("{(.*?)}", raw_res)
    print("TAGS EXTRACTED: ", tags)
    if len(tags) == 0:
        tags = ["N/A"]

    # Cleanup response - remove all the tags gpt added
    print(raw_res)
    cleaned_res = re.sub("{(.*?)}", "", raw_res)
    # Strip any trailing whitespace
    cleaned_res.strip()
    print("CLEANED RESPONSE: " + cleaned_res)

    # Returns the output to gradio to be displayed
    return cleaned_res, tags[0]

# TODO: INSERT API KEY HERE
os.environ["OPENAI_API_KEY"] = 'API-KEY'
openai.api_key = 'API-KEY'

with gr.Blocks() as demo:
    # Chatbot interface that contains the chat messages
    chatbot = gr.Chatbot()
    # Textbox input field for user to type their prompt
    msg = gr.Textbox(label="Enter query here")
    # Clear button that clears all the chat messages
    clear = gr.ClearButton([msg, chatbot], value="Clear Messages")

    def respond(message, chat_history):
        bot_output = query_chatbot(message)
        bot_message = bot_output[0]
        tag = bot_output[1]
        for query in tag.split():
            if query not in valid_tags:
                lawyers = db.see_all("lawyers")
                bot_message += "\n\nHere are some lawyers you may contact for advice:"
                for i in range(2):
                    lawyer = lawyers.pop(random.randint(0,len(lawyers)-1))
                    name = lawyer[0]
                    firm = lawyer[1] 
                    exp = lawyer[2]
                    deets = f"\n\nName: {name}\nFirm: {firm}\nYears of experience: {exp}"
                    bot_message += deets
            else:
                lawyers = db.query_lawyers(query,"mandarin")
                bot_message += "\n\nRecommended Lawyers:"
                for lawyer in lawyers:
                    name = lawyer[0]
                    firm = lawyer[1] 
                    exp = lawyer[2]
                    deets = f"\n\nName: {name}\nFirm: {firm}\nYears of experience: {exp}"
                    bot_message += deets
                    print(bot_message)
            break
        chat_history.append((message, bot_message))
        # db.save_user_convo("CHINESE", f"{message}{bot_message}")
        time.sleep(1)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()

# Construct index to be used later
# index = construct_index("docs")
