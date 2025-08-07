import textwrap
import langextract as lx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Define the prompt and extraction rules
prompt = textwrap.dedent("""\
    Extract characters, emotions, and relationships in order of appearance.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "ROMEO. But soft! What light through yonder window breaks? It is"
            " the east, and Juliet is the sun."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"},
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"},
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor"},
            ),
        ],
    )
]

# 3. Run the extraction on your input text
input_text = (
    "Lady Juliet gazed longingly at the stars, her heart aching for Romeo"
)

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",
)

# Define output paths
OUTPUT_JSONL_FILENAME = "extraction_results.jsonl"
OUTPUT_JSONL_PATH = "test_output/" + OUTPUT_JSONL_FILENAME
OUTPUT_PATH = "test_output/visualization.html"

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name=OUTPUT_JSONL_FILENAME)

# Generate the interactive visualization from the file
html_content = lx.visualize(OUTPUT_JSONL_PATH)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(str(html_content))
print(f"Visualization successfully saved to '{OUTPUT_PATH}'")