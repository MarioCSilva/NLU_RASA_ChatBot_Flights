# NLU RASA ChatBot Flights

NLU Chatbot that performs searches for available flights and prices, with a web app, flutter mobile app, built with Django Fast API for backend, and Rasa for the text-based Level 3 conversational AI, where the bot can understand the context, user changing their mind and even unexpected queries.

## How to Run

### Client Flutter Mobile App


### Real Agent React App
On the `website` folder, install the necessary dependencies. Make sure to have `yarn` installed.
```
yarn install
```
To start the app:
```
yarn start
```

### Backend

On the `backend` directory, install the dependencies to run the API:
```
pip3 install -r requirements.py
```
Make sure to have a Postgres Database, you may use a docker container with the following command:

```
docker run --name chatbotdb -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=chatbotdb -d postgres
```

Change the environments variables needed on your `config.ini` file, and start the API using uvicorn

```
uvicorn main:app
```