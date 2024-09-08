#!/usr/bin/env python

# do some fine tunning with Openai's API

import json
import openai
import signal
import datetime
import time
import requests
import os
import wandb
from wandb.sdk.data_types.trace_tree import Trace

# w&b needs to be run first: 
# wandb login API_KEY

# weights & biases
wandb.init(project='openai_finetuning', name="fine_tune_prescription_openapi")

### the API key is loaded to the enviroment in the object $OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")
# peterdemin/openai-cli uses OPENAI_API_TOKEN environment variable
os.environ["OPENAI_API_TOKEN"] = api_key

loaded_data = []
file_name = "./data/raw/training_data.json"
with open(file_name, "r") as input_file:
    training_data = json.load(input_file)

# this is to go from json to jsonl (the format required by OpenAI's API)
file_name = "./data/interim/training_data.jsonl"
with open(file_name, "w") as output_file:
    for entry in training_data:
        json.dump(entry, output_file)
        output_file.write("\n")

wandb.save("training_data.jsonl")

# this is to run int he terminal and check the consistency of the file to upload

os.system('openai tools fine_tunes.prepare_data -f ./data/interim/training_data.jsonl')

## Uploads the file and tries to fine tune
## I think I can improve the code -AM
os.system('openai api fine_tunes.create -t "./data/interim/training_data.jsonl" --compute_classification_metrics --classification_n_classes 316 -m ada')


# Set up the headers
headers = {"Authorization": f"Bearer {api_key}"}

# Make the request
response = requests.get('https://api.openai.com/v1/files', headers=headers)

# Print the response
print(response.json())

#load the API response to w&b
wandb.log({"API_Response": response.json()})

# code to start the fine tunning
training_file_id = "file-KmWn0bRL7eoPgoxRv0qi0Ct9"


# In[131]:


create_args = {"training_file": training_file_id,
               "model": "davinci", # this model is for classfication
               "n_epochs": 15,
               "batch_size": 3,
               "learning_rate_multiplier": 0.3
               }

response = openai.FineTune.create(**create_args)
job_id = response["id"]
status = response["status"]

print(f'Fine-tunning model with jobID: {job_id}.')
print(f"Training Response: {response}")
print(f"Training Status: {status}")

# log metrics to W&B
wandb.log({
    "job_id": job_id,
    "Training Response": str(response),
    "Training Status": status
})

# function created to check the characteristics of the job

def signal_handler(sig, frame):
    status = openai.FineTune.retrieve(job_id).status
    print(f"Stream interrupted. Job is still {status}.")
    return

print(f'Streaming events for the fine-tuning job: {job_id}')
signal.signal(signal.SIGINT, signal_handler)

events = openai.FineTune.stream_events(job_id)
try:
    for event in events:
        print(f'{datetime.datetime.fromtimestamp(event["created_at"])} {event["message"]}')

except Exception:
    print("Stream interrupted (client disconnected).")

# function to check constantly the status of the fine tunning in the API's

status = openai.FineTune.retrieve(id=job_id)["status"]
if status not in ["succeeded", "failed"]:
    print(f'Job not in terminal status: {status}. Waiting.')
    while status not in ["succeeded", "failed"]:
        time.sleep(2)
        status = openai.FineTune.retrieve(id=job_id)["status"]
        print(f'Status: {status}')
else:
    print(f'Finetune job {job_id} finished with status: {status}')

print('Checking other finetune jobs in the subscription.')
result = openai.FineTune.list()
print(f'Found {len(result.data)} finetune jobs.')

#retrive the fine-tuned model
model_id = "ft:davinci-002:personal::869HquyK" 
model = openai.Model(model_id) 

#create the prompt for the model
prompt = "the patient has abdominal pains and fever"

answer = openai.Completion.create(
  model = model_id,
  prompt = prompt
)

print(answer['choices'][0]['text'])

#end weights and balances
wandb.finish()