from manim import *
import tempfile
import os
import json

class SummaryScene(Scene):
    def construct(self):
        # Parse the summary JSON
        summary_data = json.loads(self.summary)

        # Create title
        title = Text("Summary Visualization", font_size=40)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Create general summary
        general_summary = Text(summary_data['general_summary'][:100] + "...", font_size=24)
        self.play(Write(general_summary))
        self.play(general_summary.animate.next_to(title, DOWN))

        # Create subtopics
        subtopics = VGroup()
        for i, subtopic in enumerate(summary_data['subtopics']):
            subtopic_text = Text(f"{subtopic['name']}: {subtopic['summary'][:50]}...", font_size=18)
            subtopics.add(subtopic_text)

        subtopics.arrange(DOWN, aligned_edge=LEFT)
        subtopics.next_to(general_summary, DOWN)

        self.play(Write(subtopics))

        # Create example or case study
        example = summary_data['example_or_case_study']
        example_text = Text(f"{example['type']}: {example['content'][:100]}...", font_size=18)
        example_text.next_to(subtopics, DOWN)

        self.play(Write(example_text))

        # Wait at the end
        self.wait(2)

def generate_manim_diagram(summary: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdirname:
        scene = SummaryScene()
        scene.summary = summary
        config.output_file = os.path.join(tmpdirname, "SummaryScene")
        config.video_dir = tmpdirname
        scene.render()
        
        output_file = os.path.join(tmpdirname, "SummaryScene.mp4")
        if os.path.exists(output_file):
            return output_file
        else:
            return ""

# Example usage
if __name__ == "__main__":
    sample_summary = json.dumps({
        "general_summary": "This is a general summary of the topic.",
        "subtopics": [
            {"name": "Subtopic 1", "summary": "Summary of subtopic 1"},
            {"name": "Subtopic 2", "summary": "Summary of subtopic 2"},
        ],
        "example_or_case_study": {
            "type": "case_study",
            "content": "This is a brief case study example."
        }
    })
    
    output = generate_manim_diagram(sample_summary)
    print(f"Output file: {output}")