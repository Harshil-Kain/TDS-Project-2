# TDS-Project-2

This repository contains the implementation for **Project 2** of the *Tools in Data Science* course at IIT Madras.

## Project Overview

The objective of this project is to develop an intelligent application powered by a **Large Language Model (LLM)** that can autonomously answer any of the graded assignment questions from the course. The application leverages the power of OpenAI's API to process natural language queries and generate accurate and relevant responses in real-time. 

### Key Features:
- **LLM Integration:** The core functionality of the application relies on an LLM that processes the input question and returns a detailed and well-structured answer.
- **Automatic Answer Generation:** Users can input a question (or upload relevant files), and the application will automatically fetch the answer by sending a request to OpenAI's API.
- **API-based Communication:** The system uses the OpenAI API to access the LLM's capabilities, ensuring scalability and high accuracy in response generation.

## How It Works
1. **User Input:** The user submits a query, either in the form of text or an attachment containing the relevant assignment question.
2. **API Request:** The application sends the input to the OpenAI API, which processes the request.
3. **Answer Generation:** The LLM returns a response based on the question, which is then displayed to the user.
4. **Output:** The system provides the answer in a structured format that is easy to understand and directly relevant to the query.

## Curl Commands for powershell
      curl.exe -X POST "https://tds-project-2-six.vercel.app/api/" -H "Content-Type: 	multipart/form-data" -F "question=Download and unzip file abcd.zip which 	has a     single extract.csv file inside. What is the value in the ""answer"" column 	of the CSV file?" -F file=@first.txt

## Curl Command for GitBash
      curl -X POST "https://tds-project-2-six.vercel.app/api/" \
  	   -H "Content-Type: multipart/form-data" \
  	   -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?" \  
  	   -F file=@first.txt
