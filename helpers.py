import time
import random
import boto3
import logging
import pandas as pd
import json
import re
import io

# def getPosts(topic):
#     # TODO: get the post numbers that match topic
#     # Dummy function to get breeds based on the selected animal
#     if topic == "Natural Recursion":
#         return ["Labrador Retriever", "German Shepherd", "Golden Retriever"]
#     elif topic == "template":
#         return ["Persian", "Siamese", "Maine Coon"]
#     elif topic == "office hours":
#         return ["Parrot", "Canary", "Finch"]
#     elif topic == "midterm":
#         return ["Goldfish", "Betta", "Guppy"]
#     else:
#         return []

def getKeywords():
    hi = 1

#-----------------------------------------------------------------------------
# Send question from front-end to llama2, retrieving the response and returning it
#-----------------------------------------------------------------------------
def getResponseFromModel(question):
    client = boto3.client('bedrock-agent-runtime')

    # modelArn = client.get_foundation_model(
    #     modelIdentifier = 'anthropic.claude-v2:1'
    # )

    # print(modelArn)
    print("The question is: " + question)

    response = client.retrieve_and_generate(
    input={
        'text': question
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'MFOWUQRVFC',
            'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-v2:1',
        }
    },
    sessionConfiguration={
        'kmsKeyArn': 'arn:aws:kms:us-west-2:852069794117:key/8c816af9-92bc-4084-8db2-a27a83bb3d87'
    }
    )

    text = response["output"]["text"]
    # print(text)

    return text

    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.1)

def uploadFileToS3(file):
    if not file:
        return
    print("in upload file to s3")
    # s3 = boto3.client('s3',
    #               aws_access_key_id="ASIA4MY2RIFCTGK3TSXM",
    #               aws_secret_access_key="z8jF19X0gvYBxGKtCIT2f4Lnumoj7HUFzCrUsidg")
    s3 = boto3.client('s3')
    try:
        # Upload file to S3
        # df = pd.read_csv(file)
        with open('finalData.txt', 'rb') as f:
            s3.upload_fileobj(f, "piazzadata", "finalData.txt")
        return 'File uploaded successfully to S3!'
        
    except Exception as e:
        logging.error(e)
        return f'Error uploading file to S3: {e}'

def parseCsv(file):
    if not file:
        return

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
            date = first_item.get('created', None)
            return subject, content, date
        return None, 'Content not provided'
    
    # Apply the function to each row and create new columns for 'subject' and 'content'
    df_history['first_subject'], df_history['first_content'], df_history['first_date'] = zip(*df_history['history_parsed'].apply(extract_first_subject_and_content))

    # delete the original history and history_parsed
    column_to_keep = ['first_subject', 'first_content', 'first_date']
    df_history = df_history.drop(columns=[col for col in df_history.columns if col not in column_to_keep])

    # merging first_subject and first_content
    df_history['Summary and Description'] = df_history['first_subject'].astype(str) + ' ' + df['first_content'].astype(str)

    # delete first_subject and first_content
    column_to_keep = ['first_date', 'Summary and Description']
    df_history = df_history.drop(columns=[col for col in df_history.columns if col not in column_to_keep])

    # In a separate file, we extracted the nr column the same way as history and saved it into a csv file
    # subtable 2 for nr
    df_date = pd.read_csv('output_nr.csv')
    df_date.rename(columns={'nr': 'post number'}, inplace=True)

    # merge df_history and df_date
    final_df = pd.concat([df_history, df_date], axis=1)
    final_df.rename(columns={'first_date': 'post date'}, inplace=True)

    # removing html and javascript tags from QuestionAndDescription
    def remove_html_tags(text):
        # Pattern to match HTML and script tags
        clean_text = re.sub('<.*?>', '', text)  # Remove HTML tags
        clean_text = re.sub('<script.*?</script>', '', clean_text, flags=re.DOTALL)  # Remove script tags
        return clean_text

    final_df['Summary and Description'] = final_df['Summary and Description'].apply(remove_html_tags)

    # convert the final csv file into a txt file
    final_df.to_csv('finalData.txt', sep='\t', index=False)

    # return
    with open('finalData.txt', 'r') as txtFile:
        file_contents = txtFile.read()
    return file_contents
