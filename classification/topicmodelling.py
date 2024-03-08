import pandas as pd
import boto3

client = boto3.client('comprehend')

def topic_modelling():
    response = client.start_topics_detection_job(
        InputDataConfig = {'S3Uri': 's3://piazzadata/minidata.txt',
                        'InputFormat': 'ONE_DOC_PER_LINE',
                        #    'DocumentReaderConfig': 
                        #             {'DocumentReadAction': 'TEXTRACT_DETECT_DOCUMENT_TEXT'}
                        },
        OutputDataConfig = {'S3Uri': 's3://piazzadata/output.tar.gz'},
        DataAccessRoleArn = 'arn:aws:iam::852069794117:role/service-role/AmazonComprehendServiceRole-test1',
        JobName = 'topic_modelling',
        NumberOfTopics = 10,  
    )
    if response['JobStatus'] == 'submitted':
        return True
    else:
        return False

# response2 = client.describe_topics_detection_job(
#     JobId=response['JobId']
# )
# response2["TopicsDetectionJobProperties"]["JobStatus"]