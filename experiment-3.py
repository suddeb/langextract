# Example where unstructured text is processed to extract structured information about relationship.

import textwrap
import langextract as lx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Define the prompt and extraction rules
prompt = textwrap.dedent("""\
    Extract the doctor's name, patient's name, diagnosis, medications, and usage.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "Patient: John Smith. Diagnosis: COVID-19 with mild symptoms. Allergies: Penicillin. Prescription: Molnupiravir 200mg capsules. "
            "Dosage: Take four capsules (800mg total) by mouth every 12 hours. Duration: 5 days. Refills: 0. Prescriber: Dr. E. Lopez"
        ),
        extractions=[
            lx.data.Extraction(extraction_class="doctor", extraction_text="Dr. E. Lopez"),
            lx.data.Extraction(extraction_class="patient", extraction_text="John Smith"),
            lx.data.Extraction(extraction_class="diagnosis", extraction_text="COVID-19"),
            lx.data.Extraction(extraction_class="symptoms", extraction_text="mild"),
            lx.data.Extraction(extraction_class="prescription", extraction_text="Molnupiravir 200mg capsules"),
            lx.data.Extraction(extraction_class="dosage", extraction_text="Take four capsules (800mg total) by mouth every 12 hours"),
        ],
    )
]

# 3. Run the extraction on your input text
input_text = """
            For patient Spider Man, the doctor has prescribed a few medications. For his Type 2 Diabetes, 
            he should take Metformin (Extended Release) 1000 mg once daily with dinner. 
            He will also be taking Liraglutide (Victoza) 1.8 mg, which is a subcutaneous injection, 
            to be administered once daily. To manage his high cholesterol, he has been prescribed Atorvastatin 40 mg 
            to be taken once daily at bedtime. Finally, for his chronic liver disease, he need to take Ursodiol 300 mg 
            three times a day with meals (breakfast, lunch, and dinner). The patient is advised to continue with a healthy diet 
            and to schedule a follow-up in three months to check their progress. The prescription is from Dr. Super Man, M.D. """

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",
)

# Define output paths
OUTPUT_JSONL_FILENAME = "exp2_extraction_results.jsonl"
OUTPUT_JSONL_PATH = "test_output/" + OUTPUT_JSONL_FILENAME
OUTPUT_PATH = "test_output/exp2_visualization.html"

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name=OUTPUT_JSONL_FILENAME)

# Generate the interactive visualization from the file
html_content = lx.visualize(OUTPUT_JSONL_PATH)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(str(html_content))
print(f"Visualization successfully saved to '{OUTPUT_PATH}'")