# bookSearch
**Overview**

The book search engine is an end to end application which has an LLM integrated into it. The application includes a browser based user interface allowing users to query for book titles, a Python backend to process requests and the integration of OpenLibrary to fetch books as well as OpenAI to generate a description on the fetched books. 

**Architecture**
1. Frontend  
   HTML, CSS and Javascript.  
   Provides the user an input field to query for books  
   Displays results in a structured format  
2. Backend  
   Exposes a /search endpoint for book search API  
   Integrates with OpenLibrary API to fetch book data  
   Uses OpenAI's API Key to generate a natural language description  
   Return JSON structure to the frontend  
3. API integreation  
   OpenLibrary - provides raw book data in JSON format  
   OpenAI - processes book titles and generates a brief description for human readibility 


**Flow**
1. User Interaction  
   User inputs a book in natural language  
   Frontend sends a request to the backend with the query
2. Backend Processing  
   The Flask API endpoint /search receives the request and sends it to OpenLibrary API to match for similar book titles
   The retrieved book titles are send to OenAI to generate a descrption in natural language
3. Response Rendering  
   The backend sends a structured JSON response containing book details and descriptions
   The frontend processes it and displays it in a user friendly manner
4. Application Hosting  
   Flask is deployed Gunicorn for multiple requests 
   
![Blank diagram (1)](https://github.com/user-attachments/assets/3da66da0-1ed5-48c2-9158-0414fe99cf4a)

 **Handling Test Cases**
 1. User inputs a book and the API endpoint returns information  
 2. User inputs a book but with a spelling mistake which returns no information, the query is then sent to OpenAI for spelling correction.
 3. User inputs a string of gibberish which yields no results(Tried a large variety of combinations to return relevant books but they were all computationally intensive)
