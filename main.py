from flask import Flask, render_template, request, jsonify
from app.wikipedia_search import search_wikipedia
from app.summarizer import summarize_and_format
from app.renderer import render_summary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        wikipedia_content = search_wikipedia(query)
        summary = summarize_and_format(wikipedia_content)
        rendered_content = render_summary(summary)
        return render_template('summary.html', content=rendered_content, query=query.title())
    return render_template('index.html')

@app.route('/recursive_search', methods=['POST'])
def recursive_search():
    topic = request.json['topic']
    wikipedia_content = search_wikipedia(topic)
    summary = summarize_and_format(wikipedia_content)
    rendered_content = render_summary(summary)
    #diagram_path = generate_manim_diagram(summary)
    return jsonify({'content': rendered_content, 'diagram': ""})

if __name__ == '__main__':
    app.run(port = 4000, debug = True)
