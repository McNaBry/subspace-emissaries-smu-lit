# SMU-Lit Hackathon 2023
Submission by Subspace Emissaries

Presenting Knowledge Interface Removing Barriers for You! **K.I.R.B.Y** is a custom trained chatbot that leverages OpenAI's chatgpt 3.5-turbo model using llama index

## How to run
- For the API KEY - Please view our submission form. We seek your understanding on this matter.
- Git clone the repository to your home directory
- Install all relevant dependencies
```
pip install -r requirements.txt
```
- Run the gradio program (via CLI or VSCode Code Runner - Select "Run Python File")
```
python chatbot_model.py
```

## Core Features
- [x] Access a chatbot that is trained on custom data (such as but not limted to legal documents) with  the chatgpt 3.5-turbo model
- [x] Allows user to converse in their preferred language (For proof of concept - only English and Chinese)
- [x] Suggest a lawyer that is relevant to the user's case (Name + Law Firm) according to what is stored in the database

## Future Features
- [ ] User accounts. Which will allow users to see their past chat logs (but not continue the conversation)
- [ ] Offers speech to text and text to speech functionalities
- [ ] [Improved User Interface](https://www.figma.com/file/Y1nCmINqy8xOhEY3FDUKvB/%3CTBC%3E?type=design&node-id=0%3A1&mode=design&t=CjS7SOMutXkIfspW-1)
- [ ] Web hosted database to support multiple user log in and chat history

## Tech Stack
1. python
2. llama_index (python)
3. gradio (python UI library)
4. openAI API
5. sqlite (database)
