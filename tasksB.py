import os
import requests
import sqlite3
import duckdb
import markdown
#from PIL import Image

# B1 & B2: Security Checks
def B12(filepath):
    """Ensure the filepath is inside /data and does not attempt deletion."""
    real_path = os.path.abspath(filepath)
    if not real_path.startswith('/data'):
        raise PermissionError(f"❌ Security Violation: {filepath} is outside /data.")
    return real_path  # Return safe absolute path

# B3: Fetch Data from an API
def B3(url, save_path):
    """Fetch data from an API and save it securely."""
    save_path = B12(save_path)
    if os.path.exists(save_path):
        raise FileExistsError(f"⚠️ File {save_path} already exists. Aborting to prevent data loss.")
    
    response = requests.get(url)
    response.raise_for_status()  # Ensure request was successful
    
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    """Clone a Git repo into /data/repo and make a commit."""
    repo_path = B12('/data/repo')
    if os.path.exists(repo_path):
        raise FileExistsError(f"⚠️ Repo path {repo_path} already exists. Aborting.")

    os.system(f"git clone {repo_url} {repo_path}")
    os.system(f"git -C {repo_path} commit --allow-empty -m '{commit_message}'")

# B5: Run SQL Query on SQLite or DuckDB
def B5(db_path, query, output_filename):
    """Run a SQL query on SQLite or DuckDB and save the result."""
    db_path = B12(db_path)
    output_filename = B12(output_filename)
    
    if os.path.exists(output_filename):
        raise FileExistsError(f"⚠️ Output file {output_filename} already exists. Aborting.")

    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()

    with open(output_filename, 'w') as file:
        file.write(str(result))

    return result

# B6: Web Scraping
def B6(url, output_filename):
    """Extract data from a website and save it."""
    output_filename = B12(output_filename)
    if os.path.exists(output_filename):
        raise FileExistsError(f"⚠️ Output file {output_filename} already exists. Aborting.")
    
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Compress or Resize an Image
'''def B7(image_path, output_path, resize=None):
    """Resize an image safely."""
    image_path = B12(image_path)
    output_path = B12(output_path)
    
    if os.path.exists(output_path):
        raise FileExistsError(f"⚠️ Output file {output_path} already exists. Aborting.")

    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)'''

# B8: Transcribe Audio
def B8(audio_path):
    """Transcribe audio from MP3."""
    import openai
    audio_path = B12(audio_path)

    with open(audio_path, 'rb') as audio_file:
        return openai.Audio.transcribe("whisper-1", audio_file)

# B9: Convert Markdown to HTML
def B9(md_path, output_path):
    """Convert Markdown file to HTML securely."""
    md_path = B12(md_path)
    output_path = B12(output_path)
    
    if os.path.exists(output_path):
        raise FileExistsError(f"⚠️ Output file {output_path} already exists. Aborting.")

    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())

    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for Filtering CSV
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    """Filter a CSV file based on a column value and return JSON data."""
    data = request.json
    csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
    
    csv_path = B12(csv_path)

    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]

    return jsonify(filtered.to_dict(orient='records'))
