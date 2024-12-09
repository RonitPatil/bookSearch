from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import openai

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

openai.api_key = ""

def fetch_books(search_query):
    #hit the openlibrary endpoint
    openlibrary_url = f"http://openlibrary.org/search.json?title={search_query}"
    response = requests.get(openlibrary_url)
    #checking if response is successful
    if response.status_code == 200:
        # return list of books
        return response.json().get('docs', [])
    #empty list otherwise
    return []

def create_description(books):
    #get titles
    titles = [b['title'] for b in books]
    #descriptive response from openai api based on book titles
    prompt = (
        f"Based on the following book titles: {', '.join(titles)}, "
        "create a natural language response that lists each book with a short description. "
        "For each title, include a brief summary highlighting its main theme or storyline. "
        "Make the response clear, engaging, and informative."
    )

    llm_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7
    )

    return llm_response.choices[0].message.content.strip()

@app.route('/search', methods=['GET'])
def search_books():
    #get params and remove whitespaces
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "Please enter a book"}), 400

    # fetch books from openLibrary
    books = fetch_books(query)
    total_books = len(books)

    if total_books == 0:
        #prompt for spelling checks
        correction_prompt = (
            f"The user searched for a book title: '{query}'. "
            "If this title is misspelled or gibberish, suggest the closest correctly spelled. "
            "If the spelling is correct, repeat the same title. "
            "Return only the corrected or closest known title as a single line of text, with no additional explanations, "
            "no quotes, and no extra formatting."
        )

        #use prompt to get the closest title
        correction_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": correction_prompt}],
            max_tokens=20,
            temperature=0.0
        )

        corrected_title = correction_response.choices[0].message.content.strip()

        #checking if new title is different from the original query
        if corrected_title.lower() != query.lower():
            #fetch books wiht new title
            corrected_books = fetch_books(corrected_title)
            total_corrected_books = len(corrected_books)
            if total_corrected_books > 0:
                #top 5 books
                book_details = []
                for book in corrected_books[:5]:
                    book_details.append({
                        "title": book.get("title", "N/A"),
                        "author": ", ".join(book.get("author_name", ["Unknown"])),
                        "year": book.get("first_publish_year", "Unknown")
                    })

                #create description for cloest found titles
                description = create_description(book_details)

                print(f"No results found for '{query}'. Closest matching title found is '{corrected_title}'.")

                message = f"No results found for '{query}'. Showing top 5 results out of {total_corrected_books} for '{corrected_title}':"

                #return json response
                return jsonify({
                    "message": message,
                    "corrected_spelling": corrected_title,
                    "total_books": total_corrected_books,
                    "books": book_details,
                    "description": description
                }), 200
            else:
                #return 404 if no books are found
                return jsonify({"error": f"No information was found about '{query}'"}), 404
        else:
            #return 404 for correct spelling but no books are found
            return jsonify({"error": f"No information was found about '{query}'."}), 404
    else:
        book_details = []
        #top 5 results
        for book in books[:5]:
            book_details.append({
                "title": book.get("title", "N/A"),
                "author": ", ".join(book.get("author_name", ["Unknown"])),
                "year": book.get("first_publish_year", "Unknown")
            })

        description = create_description(book_details)

        #showing total number of matching books
        message = f"Showing top 5 results out of {total_books} for '{query}':"

        return jsonify({
            "message": message,
            "total_books": total_books,
            "books": book_details,
            "description": description
        })

@app.route('/')
def home():
    """Serve the index.html file."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
