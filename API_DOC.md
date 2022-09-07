## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method not allowed 

### Endpoints 
#### GET /questions
- General:
    - Returns a list of question objects, success value, categories, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "questions": [
    {
      "id": 1,
      "question": "This is a question1",
      "answer": "This is an answer1",
      "difficulty": 5,
      "category": 2
    },
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 1
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "success: True
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. 
    - Returns the success value, message. 
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }'`
```
{
  "success": True,
  "message": "Question Saved",
}
```

#### POST /questions/search
- General:
  - Using searchTerm submitted, searches for a specific question by search term
  - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
  "searchTerm": "This is the search term"}'`
```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```
#### POST /quizzes
- General:
  - Sends a post request in order to get the next question
  - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": 'current category'
 }'`
```
{
    "id": 1,
    "question": {
      "id": 1,
      "question": "This is a question1",
      "answer": "This is an answer1",
      "difficulty": 5,
      "category": 2
    },
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
```


#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
    - Returns a list of question objects, success value, categories, and total number of questions
    - Results are paginated in groups of 10.

- `curl -X DELETE http://127.0.0.1:5000/question/16`
``` {
  "questions": [
    {
      "id": 1,
      "question": "This is a question1",
      "answer": "This is an answer1",
      "difficulty": 5,
      "category": 2
    },
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 1
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "success: True
}