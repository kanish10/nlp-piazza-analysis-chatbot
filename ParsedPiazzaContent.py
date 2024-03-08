#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import re


# read the csv file into a dataframe
df = pd.read_csv('output_json.csv')
# subtable 1 for history
df_history = df


# delete all columns other than history
column_to_keep = 'history'
columns_to_delete = df.columns.difference([column_to_keep])
df_history.drop(columns=columns_to_delete, inplace=True)

# extract subject (summary of question), content of question, and date of post from history
df['history_parsed'] = df['history'].apply(lambda x: json.loads(x))

def extract_first_subject_and_content(history):
    if history:  # Check if the history is not empty
        first_item = history[0]  # Assuming the first item contains the relevant data
        subject = first_item.get('subject', None)
        content = first_item.get('content', 'Content not provided')
        return subject, content
    return None, 'Content not provided'

# Apply the function to each row and create new columns for 'subject' and 'content'
df_history['first_subject'], df_history['first_content'] = zip(*df_history['history_parsed'].apply(extract_first_subject_and_content))

# delete the original history and history_parsed and first_date
column_to_keep = ['first_subject', 'first_content']
df_history = df_history.drop(columns=[col for col in df_history.columns if col not in column_to_keep])

# merging first_subject and first_content
df_history['Summary and Description'] = df_history['first_subject'].astype(str) + ' ' + df['first_content'].astype(str)

# delete first_subject and first_content
column_to_keep = ['Summary and Description']
df_history = df_history.drop(columns=[col for col in df_history.columns if col not in column_to_keep])

# removing html and javascript tags from QuestionAndDescription
def remove_html_tags(text):
    # Pattern to match HTML and script tags
    clean_text = re.sub('<.*?>', '', text)  # Remove HTML tags
    clean_text = re.sub('<script.*?</script>', '', clean_text, flags=re.DOTALL)  # Remove script tags
    return clean_text

df_history['Summary and Description'] = df_history['Summary and Description'].apply(remove_html_tags)

# removing all key words that are unnecessary
df_history['Summary and Description'] = df_history['Summary and Description'].str.replace(r'\([^)]*\)|[\(\)]|\n|else|path|true|false|empty|todo|visited|los|lop|skip|acc|try|try1|try2|lon', '', regex=True)

df_history.to_csv('DataNoTimeOrKeyWord.csv', encoding= 'utf-8', index=False)

# convert the final csv file into a txt file
df_history.to_csv('DataNoTimeOrKeyWord.txt', sep='\t', index=False)

