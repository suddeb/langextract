# Example where unstructured text is processed to extract structured information from a story book.

import textwrap
import langextract as lx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Define the prompt and extraction rules
prompt = textwrap.dedent("""\
    Extract characters, emotions, and relationships from the given text.

    Provide meaningful attributes for every entity to add context and depth.

    Important: Use exact text from the input for extraction_text. Do not paraphrase.
    Extract entities in order of appearance with no overlapping text spans.

    Note: In play scripts, speaker names appear in ALL-CAPS followed by a period.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            ROMEO. But soft! What light through yonder window breaks?
            It is the east, and Juliet is the sun.
            JULIET. O Romeo, Romeo! Wherefore art thou Romeo?"""),
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"}
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe", "character": "Romeo"}
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor", "character_1": "Romeo", "character_2": "Juliet"}
            ),
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="JULIET",
                attributes={"emotional_state": "yearning"}
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="Wherefore art thou Romeo?",
                attributes={"feeling": "longing question", "character": "Juliet"}
            ),
        ]
    )
]

# Process Romeo & Juliet directly from Project Gutenberg
print("Downloading and processing Romeo and Juliet from Project Gutenberg...")

result = lx.extract(
    text_or_documents="https://www.gutenberg.org/files/1513/1513-0.txt",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    extraction_passes=3,      # Multiple passes for improved recall
    max_workers=20,           # Parallel processing for speed
    max_char_buffer=1000      # Smaller contexts for better accuracy
)

# Define output paths
OUTPUT_JSONL_FILENAME = "romeo_juliet_extraction_results.jsonl"
OUTPUT_JSONL_PATH = "test_output/" + OUTPUT_JSONL_FILENAME
OUTPUT_PATH = "test_output/romeo_juliet_visualization.html"

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name=OUTPUT_JSONL_FILENAME)

# Generate the interactive visualization from the file
html_content = lx.visualize(OUTPUT_JSONL_PATH)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(str(html_content))
print(f"Visualization successfully saved to '{OUTPUT_PATH}'")