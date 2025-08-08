# Example where unstructured text is processed to extract structured information about a Spiderman

import textwrap
import langextract as lx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Define the prompt and extraction rules
prompt = textwrap.dedent("""\
    Extract the superhero's name, writer's name, type of book, publication date, superhero's appearance, award, born, activities, characters, jobs, enemies.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "Superman is a superhero created by writer Jerry Siegel and artist Joe Shuster, first appearing"
            "in the comic book Action Comics #1, published in the United States on April 18, 1938.[1] Superman has been regularly published in American comic books since then,"
            "and has been adapted to other media including radio serials, novels, films, television shows, theater, and video games. Superman is the archetypal superhero: "
            "he wears an outlandish costume, uses a codename, and fights evil and averts disasters with the aid of extraordinary abilities. Although there are earlier characters who arguably "
            "fit this definition, it was Superman who popularized the superhero genre and established its conventions. He was the best-selling superhero in American comic books up until the 1980s.[2]"
            "Superman was born Kal-El, on the fictional planet Krypton. As a baby, his parents Jor-El and Lara sent him to Earth in a small spaceship shortly before Krypton was destroyed in an apocalyptic cataclysm. "
            "His ship landed in the American countryside near the fictional town of Smallville, Kansas, where he was found and adopted by farmers Jonathan and Martha Kent, who named him Clark Kent. "
            "The Kents quickly realized he was superhuman; due to the Earth's yellow sun, all of his physical and sensory abilities are far beyond those of a human, and he is nearly impervious to harm and capable of unassisted flight. "
            "His adoptive parents having instilled him with strong morals, he chooses to use his powers to benefit humanity, and to fight crime as a vigilante. To protect his personal life, he changes into a primary-colored costume "
            "and uses the alias Superman when fighting crime. Clark resides in the fictional American city of Metropolis, where he works as a journalist for the Daily Planet alongside supporting characters including his love "
            "interest and fellow journalist Lois Lane, photographer Jimmy Olsen, and editor-in-chief Perry White. His enemies include Brainiac, General Zod, and archenemy Lex Luthor."
        ),
        extractions=[
            lx.data.Extraction(extraction_class="superhero", extraction_text="Superman"),
            lx.data.Extraction(extraction_class="writer", extraction_text="Jerry Siegel"),
            lx.data.Extraction(extraction_class="artist", extraction_text="Joe Shuster"),
            lx.data.Extraction(extraction_class="type", extraction_text="Action Comics"),
            lx.data.Extraction(extraction_class="publication date", extraction_text="United States on April 18, 1938."),
            lx.data.Extraction(extraction_class="appearance", extraction_text="n outlandish costume, uses a codename"),
            lx.data.Extraction(extraction_class="award", extraction_text="best-selling superhero in American comic books up until the 1980s"),
            lx.data.Extraction(extraction_class="parent", extraction_text="Jor-El and Lara"),
            lx.data.Extraction(extraction_class="born", extraction_text="Kal-El, on the fictional planet Krypton"),
            lx.data.Extraction(extraction_class="work", extraction_text="works as a journalist for the Daily Planet"),
            lx.data.Extraction(extraction_class="character", extraction_text="Lois Lane, Jimmy Olsen, Perry White"),
            lx.data.Extraction(extraction_class="enemies", extraction_text="Brainiac, General Zod, Lex Luthor"),
        ],
    )
]

# 3. Run the extraction on your input text

result = lx.extract(
    text_or_documents="https://raw.githubusercontent.com/suddeb/langextract/main/data/spiderman.txt",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    extraction_passes=3,      # Multiple passes for improved recall
    max_workers=20,           # Parallel processing for speed
    max_char_buffer=1000      # Smaller contexts for better accuracy
)

# Define output paths
OUTPUT_JSONL_FILENAME = "spiderman_extraction_results.jsonl"
OUTPUT_HTML_FILENAME = "spiderman_visualization.html"

script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level from 'code' to the project root, then into the 'data' directory
OUTPUT_JSONL_PATH = os.path.join(script_dir, "..", "test_output", OUTPUT_JSONL_FILENAME)
OUTPUT_HTML_PATH = os.path.join(script_dir, "..", "test_output", OUTPUT_HTML_FILENAME)

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name=OUTPUT_JSONL_FILENAME)

# Generate the interactive visualization from the file
html_content = lx.visualize(OUTPUT_JSONL_PATH)
with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(str(html_content))
print(f"Visualization successfully saved to '{OUTPUT_HTML_PATH}'")