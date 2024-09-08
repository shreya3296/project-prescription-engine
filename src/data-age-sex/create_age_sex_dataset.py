#!/usr/bin/env python

import ast 
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import random

# Function to map evidence ID to its description
def map_evidence_to_description(evidence_id, patient_evidence_value, evidences):
    evidence = evidences.get(evidence_id)
    if not evidence:
        return 'Unknown evidence'

    description = evidence.get('question_en', 'Unknown question')
    
    if evidence['data_type'] in ['C', 'M']:
        value_meaning = evidence.get('value_meaning', {})
        value_description = value_meaning.get(patient_evidence_value, {}).get('en', 'Unknown value')
        description += " (" + value_description + ")"
    
    return description


# Function to map condition ID to its ICD-10 code
def map_condition_to_icd10(condition_id, conditions):
    condition = conditions.get(condition_id)
    if condition:
        return condition.get('icd10-id', 'Unknown')
    return 'Unknown'

# Load evidences and conditions
with open('/data/release_evidences.json') as f:
    evidences = json.load(f)

with open('/data/release_conditions.json') as f:
    conditions = json.load(f)

# Read patient data (assuming CSV format)
patients_df = pd.read_csv('/data/release_train_patients')

# Create DataFrame with required columns
df = pd.DataFrame(columns=['age', 'gender', 'diagnosis', 'ICD 10 code', 'symptoms', 'antecedents'])

print(patients_df.columns)

rows = []

for index, row in patients_df.iterrows():
    # Map diagnosis to ICD-10 code
    icd_10_code = map_condition_to_icd10(row['PATHOLOGY'], conditions)

    # Convert symptoms and antecedents to natural language
    symptoms = []
    antecedents = []

    # Convert the 'EVIDENCES' string to a list
    try:
        evidences_list = ast.literal_eval(row['EVIDENCES'])
    except ValueError:
        # Handle cases where 'EVIDENCES' is not a valid list string
        evidences_list = []

    for evidence_str in evidences_list:
        parts = evidence_str.split('_@_')
        evidence_id = parts[0]
        value = parts[1] if len(parts) > 1 else None

        description = map_evidence_to_description(evidence_id, value, evidences)
        if evidences.get(evidence_id, {}).get('is_antecedent', False):
            antecedents.append(description)
        else:
            symptoms.append(description)

    # Append the data to the DataFrame
    rows.append({
        'age': row['AGE'],
        'gender': row['SEX'],
        'diagnosis': row['PATHOLOGY'],
        'ICD 10 code': icd_10_code,
        'symptoms': ' '.join(symptoms),
        'antecedents': ' '.join(antecedents)
    })

df = pd.DataFrame(rows)

len(df['ICD 10 code'].unique())

# Randomly select 10 rows
sampled_rows = df.sample(n=10, random_state=random.seed())

# Extract symptoms and antecedents
sampled_symptoms = sampled_rows['symptoms'].tolist()
sampled_antecedents = sampled_rows['antecedents'].tolist()

# Print the sampled symptoms and antecedents
print("Sampled Symptoms:")
for symptom in sampled_symptoms:
    print(symptom)

print("\nSampled Antecedents:")
for antecedent in sampled_antecedents:
    print(antecedent)

#now, lets transform the questionarie into narratives
#first, we are going to sample our data set, we have 1 million observations
# Stratify the DataFrame based on 'age', 'gender', 'ICD 10 code'

# first, we remove classes with 1 observations
# Combining stratification columns into a single column
df['combined_stratify'] = df['age'].astype(str) + '_' + df['gender'] + '_' + df['ICD 10 code']

# Filter out combinations with fewer than the threshold
min_members_threshold = 2
value_counts = df['combined_stratify'].value_counts()
to_keep = value_counts[value_counts >= min_members_threshold].index
filtered_df = df[df['combined_stratify'].isin(to_keep)]

# Perform stratified sampling on the filtered DataFrame
sampled_df, _ = train_test_split(filtered_df, test_size=0.99, stratify=filtered_df['combined_stratify'], random_state=42)

sampled_df.to_csv(sys.argv[1], index=False)