async function searchBooks() {
    const queryInput = document.getElementById('bookQuery');
    const query = queryInput.value.trim();
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const searchBtn = document.getElementById('searchBtn');

    if (!query) {
        resultsDiv.innerHTML = '<p style="color:blue;">Please enter a book title.</p>';
        return;
    }

    resultsDiv.innerHTML = '';
    loadingDiv.style.display = 'block';

    queryInput.disabled = true;
    searchBtn.disabled = true;

    queryInput.value = '';


    try {
        const response = await fetch(`https://https://book-search-tau.vercel.app/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        loadingDiv.style.display = 'none';

        const description = data.description || '';
        const lines = description.split('\n').map(line => line.trim()).filter(line => line.length > 0);
        let formattedDescription = '';

        if (lines.length > 1) {
            formattedDescription = `
                <ul>
                    ${lines.map(line => `<li>${line}</li>`).join('')}
                </ul>
            `;
        } else {
            formattedDescription = `<p>${lines[0] || ''}</p>`;
        }

        if (data.error) {
            resultsDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
        } else if (data.message && data.corrected_spelling) {
            resultsDiv.innerHTML = `
                <p style="color:blue;">${data.message}</p>
                <h2>Closest Results</h2>
                <ul>
                    ${data.books
                        .map(
                            (book) => `
                            <li>
                                <strong>Title:</strong> ${book.title}<br>
                                <strong>Author(s):</strong> ${book.author}<br>
                                <strong>First Published:</strong> ${book.year}
                            </li>`
                        )
                        .join('')}
                </ul>
                ${formattedDescription}
            `;
        } else {
            resultsDiv.innerHTML = `
                <p style="color:blue;">${data.message}</p>
                <ul>
                    ${data.books
                        .map(
                            (book) => `
                            <li>
                                <strong>Title:</strong> ${book.title}<br>
                                <strong>Author(s):</strong> ${book.author}<br>
                                <strong>First Published:</strong> ${book.year}
                            </li>`
                        )
                        .join('')}
                </ul>
                ${formattedDescription}
            `;
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        resultsDiv.innerHTML = `<p style="color:blue;">An error occurred. Please try again later.</p>`;
    } finally {
        queryInput.disabled = false;
        searchBtn.disabled = false;
    }
}
