from flask import Flask, render_template, request, jsonify, session
from modal_inference import llm_inference
from modal_manim import generate_manim_animation
from suno_music import generate_music_snippet
import sqlite3

app = Flask(__name__)
app.secret_key = 'x'  # Replace with a real secret key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        return process_query(query)
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    try:
        query = request.json['query']
        
        # Call the Modal function for LLM inference
        content = llm_inference.remote(f"Provide a detailed explanation about: {query}")
        
        # Check if it's a STEM query
        if is_stem_query(query):
            # Generate Manim animation
            animation_path = generate_manim_animation.remote(content)
        else:
            animation_path = None
        
        # Check if it's a music query
        if is_music_query(query):
            music_path = generate_music_snippet(query)
        else:
            music_path = None
        
        return jsonify({
            'content': content,
            'animation': animation_path,
            'music': music_path
        })
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': 'An error occurred while processing your query.'}), 500
    
@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json['message']
        highlighted_text = request.json.get('highlighted_text')
        response = chat_with_assistant(message, highlighted_text)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing chat: {e}")  # Log the error
        return jsonify({'error': 'An error occurred while processing your chat.'}), 500

def search_wikipedia(query):
    # This function is no longer needed
    pass

def summarize_and_format(content, user_interests):
    prompt = f"""
    Summarize the following content, taking into account the user's interests: {user_interests}.
    Include hyperlinks for relevant subtopics.
    Content: {content}
    """
    return llm_inference(prompt)

def add_interest(user_id, interest):
    conn = sqlite3.connect('user_interests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS interests
                 (user_id TEXT, interest TEXT)''')
    c.execute("INSERT INTO interests VALUES (?, ?)", (user_id, interest))
    conn.commit()
    conn.close()

def get_user_interests(user_id):
    return ["math", "physics", "chemistry", "biology", "engineering", "computer science", "technology"]

def chat_with_assistant(message, highlighted_text=None):
    prompt = f"User message: {message}\n"
    if highlighted_text:
        prompt += f"Highlighted text: {highlighted_text}\n"
    prompt += "Please provide a helpful response."
    return llm_inference(prompt)

def is_stem_query(query):
    stem_keywords = [
        'math', 'mathematics', 'algebra', 'geometry', 'calculus', 'statistics', 'probability',
        'physics', 'mechanics', 'thermodynamics', 'electromagnetism', 'quantum', 'relativity',
        'chemistry', 'organic', 'inorganic', 'biochemistry', 'molecular', 'atomic',
        'biology', 'genetics', 'ecology', 'evolution', 'cell', 'organism', 'anatomy',
        'engineering', 'mechanical', 'electrical', 'civil', 'chemical', 'software',
        'computer science', 'algorithm', 'data structure', 'programming', 'coding',
        'artificial intelligence', 'machine learning', 'neural network', 'deep learning',
        'robotics', 'automation', 'cybernetics', 'nanotechnology', 'biotechnology',
        'astronomy', 'astrophysics', 'cosmology', 'planet', 'star', 'galaxy',
        'environmental science', 'climate', 'geology', 'meteorology', 'oceanography',
        'neuroscience', 'cognitive science', 'psychology', 'behavioral science',
        'data science', 'big data', 'analytics', 'visualization', 'modeling',
        'cryptography', 'information theory', 'network theory', 'graph theory',
        'optimization', 'linear algebra', 'differential equations', 'number theory',
        'topology', 'set theory', 'logic', 'discrete mathematics', 'combinatorics',
        'operations research', 'systems engineering', 'control theory', 'signal processing',
        'materials science', 'polymer', 'metallurgy', 'ceramics', 'composites',
        'bioinformatics', 'genomics', 'proteomics', 'systems biology', 'synthetic biology'
    ]
    return any(keyword in query.lower() for keyword in stem_keywords)

def is_music_query(query):
    music_keywords = [
        'music', 'song', 'melody', 'rhythm', 'harmony', 'composer', 'singer', 'musician',
        'band', 'orchestra', 'symphony', 'concert', 'opera', 'jazz', 'blues', 'rock',
        'pop', 'hip hop', 'rap', 'classical', 'baroque', 'romantic', 'contemporary',
        'electronic', 'dance', 'techno', 'house', 'ambient', 'folk', 'country',
        'reggae', 'ska', 'punk', 'metal', 'alternative', 'indie', 'r&b', 'soul',
        'funk', 'disco', 'gospel', 'choral', 'acapella', 'instrumental', 'vocal',
        'lyrics', 'chord', 'scale', 'key', 'tempo', 'time signature', 'pitch',
        'timbre', 'tone', 'note', 'staff', 'clef', 'octave', 'interval', 'triad',
        'arpeggio', 'progression', 'cadence', 'modulation', 'transposition',
        'counterpoint', 'fugue', 'sonata', 'concerto', 'suite', 'etude', 'nocturne',
        'prelude', 'overture', 'aria', 'recitative', 'libretto', 'score', 'arrangement',
        'orchestration', 'instrumentation', 'ensemble', 'quartet', 'quintet', 'sextet',
        'conductor', 'virtuoso', 'improvisation', 'jam', 'gig', 'tour', 'album',
        'single', 'EP', 'remix', 'cover', 'sample', 'loop', 'beat', 'bassline',
        'riff', 'hook', 'verse', 'chorus', 'bridge', 'coda', 'intro', 'outro',
        'crescendo', 'diminuendo', 'forte', 'piano', 'staccato', 'legato', 'vibrato',
        'tremolo', 'glissando', 'portamento', 'syncopation', 'polyrhythm', 'ostinato',
        'leitmotif', 'tone row', 'atonality', 'microtonality', 'serialism', 'minimalism'
    ]
    return any(keyword in query.lower() for keyword in music_keywords)

if __name__ == '__main__':
    app.run(port=4001, debug=True)
