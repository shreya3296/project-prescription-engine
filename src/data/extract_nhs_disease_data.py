#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
import sys


def collect(output_path):
    # ensure output path is writable before starting
    f = open(sys.argv[1], 'w')

    # Make a request to the website
    r = requests.get('https://www.nhsinform.scot/illnesses-and-conditions/a-to-z#A')
    r.raise_for_status()  # Check if the request was successful

    # Parse the HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Initialize an empty dictionary
    diseases_dict = {}

    # Iterate through all the anchor tags in the HTML
    for a_tag in soup.find_all('a'):
        # Get the text content of the anchor tag, which is the disease name
        disease_name = a_tag.text.strip()
        diseases_dict[disease_name] = None  # You can replace None with any relevant data


    # In[4]:


    # Make a request to the website
    r = requests.get('https://www.nhsinform.scot/illnesses-and-conditions/a-to-z#A')
    r.raise_for_status()  # Check if the request was successful

    # Parse the HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Initialize an empty dictionary
    diseases_dict = {}

    # Find all the disease names and URLs
    for a_tag in soup.find_all('a', href=True):
        if 'illnesses-and-conditions' in a_tag['href']:
            disease_name = a_tag.text.strip()
            disease_url = a_tag['href']
            if not disease_url.startswith('https://'):
                disease_url = 'https://www.nhsinform.scot' + disease_url
            diseases_dict[disease_name] = disease_url


    # In[5]:


    # Assuming diseases_dict is your dictionary

    keys_to_remove = list(diseases_dict.keys())[:list(diseases_dict.keys()).index('Abdominal aortic aneurysm')]

    for key in keys_to_remove:
        diseases_dict.pop(key)

    # Now diseases_dict will only have entries from 'Abdominal aortic aneurysm' onwards


    # In[6]:


    # Assuming diseases_dict is your dictionary

    keys_to_remove = list(diseases_dict.keys())[list(diseases_dict.keys()).index('Yellow fever') + 1:]

    for key in keys_to_remove:
        diseases_dict.pop(key)

    # Now diseases_dict will only have entries up to 'Yellow fever'


    # In[7]:


    diseases_dict.pop("Back to top", None)


    # In[8]:


    df = pd.DataFrame(list(diseases_dict.items()), columns=['Disease', 'URL'])

    # Initialize empty lists to hold the disease descriptions and symptoms
    descriptions = []
    symptoms = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Make a request to the disease page
        try:
            r = requests.get(row['URL'])
            r.raise_for_status()  # Check if the request was successful
        except Exception as e:
            print(f"{row['URL']}: {e}", file=sys.stderr)

        
        # Parse the HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract the disease description
        description_heading = soup.find('h2', string=re.compile('About|Introduction'))
        if description_heading:
            description = description_heading.find_next('p').text
        else:
            # If the About/Introduction heading is not found, extract all text from the parent tag of the disease name
            disease_name_tag = soup.find('h1', string=row['Disease'])
            if disease_name_tag:
                parent_tag = disease_name_tag.find_parent()
                description = parent_tag.get_text(separator=' ', strip=True)
            else:
                description = 'Description not found'
        
        # Extract the symptoms
        symptoms_heading = soup.find('h2', string=re.compile('Symptoms|Signs and symptoms|symptoms'))
        if symptoms_heading:
            symptom = symptoms_heading.find_next('p').text
        else:
            symptom = 'Symptoms not found'
        
        # Append the extracted information to the lists
        descriptions.append(description)
        symptoms.append(symptom)

    # Add the extracted information to the DataFrame
    df['Description'] = descriptions
    df['Symptoms'] = symptoms

    # Now df contains all the extracted information


    # In[9]:


    df['text'] = df['Description'] + ' ' + df['Symptoms']


    # In[10]:


    df['formatted'] = df.apply(lambda row: f'("{row["text"]}", "{row["Disease"]}")', axis=1)

    # Now, df['formatted'] contains the formatted strings
    formatted_data = df['formatted'].tolist()


    # In[11]:


    ## OJO TOCA LIMPIAR UN POCO LA DATA PORQUE AUN HAY UNAS POCAS ENFERMEDADES
    # QUE NO LAS ESTA COGIENDO DE LA PAGINA. SON POCAS PERO HAY QUE IR DEPURANDO LA BASE.


    # In[21]:


    # If you want to see the first 5 formatted strings
    for formatted_string in formatted_data[:5]:
        print(formatted_string)


    # In[22]:


    data_list = df[['Disease', 'text']].to_dict('records')


    # In[23]:


    # Initialize an empty list to hold the transformed data
    training_data = []

    # Iterate over each dictionary in the original data
    for item in data_list:
        # Construct a new dictionary with the desired keys and values
        new_item = {
            'prompt': item['text'] + ' ->',
            'completion': item['Disease'] + '\n'
        }
        # Append the new dictionary to the transformed data list
        training_data.append(new_item)


    # In[25]:


    for entry in training_data:
        # Add a whitespace character at the beginning of the completion value
        # this is a requirement of OpenAI API due to the tokenization they use
        entry['completion'] = ' ' + entry['completion']


    # In[26]:


    # Convert the list of dictionaries to JSON
    training_data_json = json.dumps(training_data, indent=4)

    # Save the JSON to a file
    f.write(training_data_json)


# In[27]:


## OJO TOCA LIMPIAR UN POCO LA DATA PORQUE AUN HAY UNAS POCAS ENFERMEDADES
## QUE NO LAS ESTA COGIENDO DE LA PAGINA. SON POCAS PERO HAY QUE IR DEPURANDO LA BASE.

if __name__ == '__main__':
    collect(sys.argv[1])