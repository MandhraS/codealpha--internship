# Simple URL Shortener

A small Flask + SQLite URL shortener with:

- `POST /api/shorten` to create a short URL
- `GET /<short_code>` to redirect to the original URL
- `GET /api/stats/<short_code>` to view saved URL stats
- A basic frontend for creating and copying short links

## Project Structure

```text
url-shortener/
  app.py
  requirements.txt
  urls.db                # created automatically after the app runs
  templates/
    index.html
    404.html
  static/
    styles.css
    script.js
```

## How to Run in VS Code

1. Open this folder in VS Code:

   ```bash
   code .
   ```

2. Open the VS Code terminal.

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment.

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the Flask server:

   ```bash
   python app.py
   ```

7. Open the app in your browser:

   ```text
   http://127.0.0.1:5000
   ```

## API Examples

Create a short URL:

```bash
curl -X POST http://127.0.0.1:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d "{\"long_url\":\"https://www.example.com/some/long/path\"}"
```

Example response:

```json
{
  "short_code": "A1b2C3",
  "short_url": "http://127.0.0.1:5000/A1b2C3",
  "long_url": "https://www.example.com/some/long/path"
}
```

Visit the short URL in a browser to redirect to the original URL.
