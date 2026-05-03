# Movie Review Website
Author - Leo Aghazarian  
Class - CS351

This is an API-first movie review website which retrieves and makes use of real-time metadata for movies through the use of TMDB's API.

## How to Run
- Install dependencies: `pip install flask flask-sqlalchemy requests werkzeug`
- Run the app: `python app.py`

## Core Design
- Hybrid Data Model:
    - Dynamic (TMDB API): Movie titles, posters, and trending lists are fetched on-demand ensuring a "zero-maintenance" catalog.
    - Persistent (SQLite): User accounts and reviews are stored locally, linked to global movies via a unique `tmdb_id`.
- Real-time UI: Features a debounced autocomplete search that queries a very large amount of titles instantly without page reloads.
- Responsive Layout: A CSS Grid-based interface that automatically scales from a 10-movie "Trending" desktop view to a single-column mobile view.

## Tech Stack
- Frontend: JS (Async/Fetch), CSS3 Grid/Flexbox.
- Backend: Python (Flask), SQLAlchemy.
- Integrations: TMDB REST API.

## Screenshots
<p>
    <img src="https://github.com/user-attachments/assets/634c26ce-da99-4a83-bfed-39aabcc5e7d6" width="49%">
    <img src="https://github.com/user-attachments/assets/43c4a182-6ab3-4418-930c-10c6b0fba47b" width="49%">
</p>

<p>
    <img src="https://github.com/user-attachments/assets/725b9bac-17fc-4011-aa7e-a4e2b0762b11" width="49%">
    <img src="https://github.com/user-attachments/assets/81c4db88-a1a8-4986-95c1-bff5f7c7c572" width="49%">
</p>
