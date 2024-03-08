import streamlit as st
import pandas as pd
import numpy as np
# from helpers import getPosts
from helpers import uploadFileToS3
from helpers import parseCsv
from classification.analytics import analyzeData

# # Checkbox to toggle day/night mode
# dark_mode = st.checkbox("Dark Mode")

#=============================================================================
# Upload Dataset Section
#=============================================================================
st.subheader("Upload Dataset")
# display file input button
uploaded_file = st.file_uploader("Choose a file", type="csv")
parsed = parseCsv(uploaded_file)

uploadFileToS3(parsed)
# if uploaded_file:

st.divider()


#=============================================================================
# Topics & Questions Section
#=============================================================================
anaylzedData = analyzeData() # get analyzed data
# st.write(anaylzedData)

#-------------------
# Select Topics
#-------------------
 # TODO: filter based on selected data

# st.write(keywords)
# options = st.multiselect(
#     'Topics',
#     ['Natural Recursion', 'Function Composition', 'Template Tags', 'Graphs'],
#     ['Natural Recursion', 'Graphs'])


#-------------------
# Topics List & Post Numbers
#-------------------
# Extract the keywords from the data
keywords = anaylzedData["keyword"].tolist()
topics = keywords
# setup the columns
topicsCol, postNumsCol = st.columns(2)
topicsCol.subheader("Most Frequent Topics:")

selectedTopic = topicsCol.radio("Select to view count", topics)
# postNums = getPosts(selectedTopic)
keywordCount = anaylzedData[anaylzedData["keyword"] == selectedTopic]["count"].iloc[0]
postNumsCol.subheader(f"Number of posts on {selectedTopic}:")
postNumsCol.divider()
# postNumsCol.subheader(keywordCount)
postNumsCol.header(":red[" + str(keywordCount) + "]")
postNumsCol.divider()

# for postNum in postNums:
#     postNumsCol.write(postNum)


st.write("") # blank space

#-------------------
# Bar Chart
#-------------------
st.subheader("Stats")
freqCounts = anaylzedData["count"].tolist()
color_data = {
    'Topics': topics,
    'Post Count': freqCounts
}

df = pd.DataFrame(color_data)
# df.set_index('Color', inplace=True)
st.bar_chart(df, x="Topics", y="Post Count", color="#0000FF", width=5) # display
