AC215-Milestone 3
==============================

------------
```
.
├── Dockerfile                         <- Dockerfile for dvc container
├── LICENSE
├── README.md
├── compose.yml
├── data
│   └── raw
│       └── training_data.json.dvc     <- Processed webscraped data
├── notebooks                          <- Jupyter notebooks for webscraping and model testing
│   ├── extract_nhs_disease_data.ipynb
│   └── fine_tune_API_GPT35.ipynb
├── references                         <- Reference papers
│   ├── 2212.13138.pdf
│   ├── 2303.18223.pdf
│   ├── 2306.05052.pdf
│   ├── 2307.03109.pdf
│   └── 2308.07633.pdf
├── reports                            <- Previous milestone markdown submissions
│   └── milestone2.md
├── requirements.txt                   <- requirements.txt for dvc container
└── src
    ├── data                           <- Container to scrape NHS data
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   └── extract_nhs_disease_data.py
    └── models                         <- model training/fine-tuning container
        └── gpt35
            ├── Dockerfile
            ├── Pipfile
            ├── Pipfile.lock
            └── fine_tune_API_GPT35.py
```
--------

# AC215 - Milestone3

**Team Members**
Shreya Chaturvedi, Alvaro Morales, Phil Salazar, Nathan Weeks

**Group Name**
The Prescribers

**Project**
This project aims to develop a solution that offers diagnostic recommendations and prescription suggestions to healthcare providers in developing countries.

### Milestone3

We changed the strategy we were using and decided to compile our database from medical websites that offer medical guidelines freely accessible online. Scraping data from these websites proved more feasible than using the text of the physical versions of these guides because the patterns in the books vary widely. As a result, we structured a web scraping tool that navigates through a set of pages. For this milestone, we only included the scraper for the NHS as we finalize formatting the outputs from other scrapes. The tool then creates a dataframe with the disease in the first column and the associated symptoms in the second.

For predicting diagnoses based on symptoms, we utilized OpenAI's API. We fine-tuned a classification model where the symptoms serve as the prompt, and the completion is the diagnosis. From initial testing, the model appears to be performing well, but it requires further tuning. However, it shows promise. A significant drawback to this approach is the cost of fine-tuning. As we increase the number of tokens in the training dataset, the cost of fine-tuning also rises. As a result, we're exploring the use of Llama-derived models that possess fewer parameters without compromising accuracy. These models can run locally, which may benefit our project.

Once we solidify the diagnosis prediction, we'll move on to matching the prediction with its corresponding ICD-10 code. This will ensure standardized diagnoses based on symptoms. Subsequently, we'll delve into predicting prescriptions.

**Experiment Tracking**

Below you can see the output from our Weights & Biases page. We used this tool to track our model fine-tuning. It was tracked using the `wandb` library we included inside of our script. 

![Captura de pantalla 2023-10-05 a la(s) 8 54 13 p m](https://github.com/AC215-The-Prescribers/ac215_the_prescribers/assets/40676504/02666509-dc8f-4278-8655-7ee84007fd35)
![Captura de pantalla 2023-10-05 a la(s) 8 54 01 p m](https://github.com/AC215-The-Prescribers/ac215_the_prescribers/assets/40676504/6114f4e1-6d5b-4e8f-b531-5f6c52f8fc9c)
![Captura de pantalla 2023-10-05 a la(s) 8 53 52 p m](https://github.com/AC215-The-Prescribers/ac215_the_prescribers/assets/40676504/09aebd92-957c-451c-8cfd-00d59676b8c3)

#### Code Structure

**Secrets**

A GCP service account token providing access to the GCS bucket is expected to reside on the host at `../secrets/data-service-account.json`.

**Data Folder**

Data in ./data are versioned using DVC.
DVC commands can be run in a container thus:
```
docker compose run dvc [command]
```
The container image will be automatically built if it doesn't exist.

**Data Processing Container**

- This container scraps the data from the web and then creates a data frame with the variables of interest.
- Output from this container stored in ./data/raw/training_data.json

(1) `src/data/extract_nhs_disease_data.py`  - scrapes HTML data from the NHS website and writes output to a JSON file

(3) `Dockerfile` and  `requirements.txt` - define the software environment for the dvc container

** GPT3.5 Training Container**

- This container contains our training script.
- The input for this container is ./data/raw/training_data.json.
- Output is customized GPT3.5 model (at OpenAI)
- Weights & Biases used for experiment tracking

(1) `src/models/gpt35/fine_tune_API_GPT35.py` - This script converts incoming data to TFRecords, applies standard image augmentation, and fits the model. It takes the following arguments:

**Notebooks** 
This folder contains the code of the data exploration and the experimentations with the model. 

## Operations

1. Save GCS service account token at ../secrets/data-service-account.json
2. Download training data using dvc:

```
docker compose run --rm dvc pull -r ac215-milestone3
```

3. (Optional) Update the training data:

```
docker compose run --rm extract_nhs_disease_data
```

4. Set environment variables `OPENAI_API_KEY` and `WANDB_API_KEY` (e.g., in a [.env file](https://github.com/compose-spec/compose-spec/blob/master/spec.md#env_file))

5. Run training container

```
docker compose run --rm train
```
