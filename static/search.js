let timer;

const searchInput = document.getElementById('movieSearch');
const resultsDiv = document.getElementById('results');

if (!searchInput || !resultsDiv) {
    // Prevent runtime errors if elements are missing from the DOM
} else {
    searchInput.addEventListener('input', () => {
        clearTimeout(timer);

        const query = searchInput.value.trim();

        if (query.length < 2) {
            resultsDiv.style.display = 'none';
            return;
        }

        // Debounce to avoid firing a request on every keystroke
        timer = setTimeout(() => {
            fetch(`/api/movies/search?q=${encodeURIComponent(query)}`)
                .then((res) => res.json())
                .then((data) => {
                    resultsDiv.innerHTML = '';

                    data.forEach((movie) => {
                        const item = document.createElement('div');
                        item.className = 'autocomplete-item';
                        item.textContent = movie.title;

                        // Direct navigation improves UX for autocomplete selection
                        item.onclick = () => {
                            window.location.href = `/movie/${movie.id}`;
                        };

                        resultsDiv.appendChild(item);
                    });

                    resultsDiv.style.display = 'block';
                });
        }, 300);
    });

    document.addEventListener('click', (e) => {
        // Hide suggestions when clicking outside the search input
        if (e.target !== searchInput) {
            resultsDiv.style.display = 'none';
        }
    });
}