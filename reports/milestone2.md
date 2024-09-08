AC215-Template (Milestone2)
==============================

AC215 - Milestone2

Project Organization
------------
      ├── LICENSE
      ├── README.md
      ├── notebooks
      ├── references
      ├── requirements.txt
      ├── setup.py
      └── src
            ├── preprocessing
            │   ├── Dockerfile
            │   ├── guideline-170-en.txt
            │   ├── preprocess.py
            │   └── requirements.txt
            └── validation


--------
# AC215 - Milestone2 - Diagnosis and prescription at a low cost for developing countries

**Team Members**
Shreya Chaturvedi, Alvaro Morales, Phil Salazar, Nathan Weeks

**Group Name**
The Prescribers

**Project**
This project aims to develop a solution that offers diagnostic recommendations and prescription suggestions to healthcare providers in developing countries.

### Milestone2 ###

---
We are in the process of constructing a comprehensive dataset. This dataset features a column dedicated to various diseases. Accompanying each disease entry, every row presents an additional column detailing the associated symptoms of that particular ailment. It's important to note that the symptom description column consists of unstructured text, which means it might contain diverse formats, phrases, or terminologies.

Our data collection methodology is thorough. We extract information from authoritative sources, such as medical guidelines, ensuring the accuracy and relevance of the content. Additionally, we consult medical textbooks that provide in-depth explanations of each disease, along with a detailed overview of their respective symptoms. It's worth mentioning that our initial dataset, which we've already incorporated into the repository, originates from Médecins Sans Frontières.

**Preprocess container**
- Input to this container is source and destincation GCS location, parameters for resizing, secrets needed - via docker
- Output from this container stored at GCS location

(1) `src/preprocessing/preprocess.py`  - Here, we are working with unstructured text, extracting information related to diagnosis and symptoms from medical guidelines. Our goal is to create a data frame that associates each symptom with a corresponding disease.

(2) `src/preprocessing/requirements.txt` - We used the following packages to help us preprocess here. 

(3) `src/preprocessing/Dockerfile` - This dockerfile starts with  `python:3.8-slim-buster`. This <statement> attaches volume to the docker container and also uses secrets (not to be stored on GitHub) to connect to GCS.

To run Dockerfile - `Instructions here`

**Cross validation, Data Versioning**
- This container reads preprocessed dataset and creates validation split and uses dvc for versioning.
- Input to this container is source GCS location, parameters if any, secrets needed - via docker

To run Dockerfile - `Instructions here`

**Notebooks** 
This folder contains code that is not part of container - for e.g: EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations. 

**GCP**

We have stood up a GKE cluster with Container-Optimized OS built in which will house our Docker container(s), and set up a bucket for training data and versioning of the training data to live.

----
You may adjust this template as appropriate for your project.
