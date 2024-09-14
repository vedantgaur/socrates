import markdown

def render_summary(summary: str) -> str:
    return markdown.markdown(summary)