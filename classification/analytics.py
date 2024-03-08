import pandas as pd


def analyzeData():
    # topics = pd.read_csv("data/topic-terms.csv")
    topics = pd.read_csv("classification/data/topic-terms.csv")
    # documents = pd.read_csv("data/doc-topics.csv")
    documents = pd.read_csv("classification/data/doc-topics.csv")

    documents_filtered = documents[documents['proportion'] > 0.75]
    topic_dict = {"topic": [0,1,2,3,4,5,6,7,8,9],
                "keyword": ['Online Communication', "Programming", "Racket", 'Virtual Classroom', 'Assignments', 'Labs', 'Online Learning Platforms', 'Academics', 'Data Types', 'Academic Support']}
    topic_dict = pd.DataFrame(topic_dict)
    keyword_counts = {"keyword": [],
                    "count": []}
    for i in range(10):
        keyword_counts['keyword'].append(topic_dict['keyword'][i])
        keyword_counts['count'].append(len(documents_filtered[documents_filtered['topic'] == i]))
        
    keyword_counts = pd.DataFrame(keyword_counts)
    return keyword_counts










