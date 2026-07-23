from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_document(text):

    prompt = f"""
            You are an expert AI Learning & Development Assistant for industrial organizations.

            Your task is to analyze the entire document and generate a structured, high-quality summary.

            Important Rules

            1. Read the ENTIRE document before summarizing.
            2. Summarize the complete document, not just the beginning.
            3. Use ONLY information present in the document.
            4. Never invent facts.
            5. Merge duplicate information instead of repeating it.
            6. Prioritize important concepts over examples or filler text.
            7. Write in clear, simple English suitable for trainees and employees.
            8. Keep the summary concise but informative (approximately 250–500 words depending on document size).
            9. If the document is short, create a concise summary.
           10. If the document is long, summarize every major section.

            The document may be ANY type, including:

            • Safety manuals
            • SOPs
            • Technical documentation
            • Employee handbooks
            • Learning modules
            • Policies
            • HR training
            • Equipment manuals
            • Manufacturing procedures
            • Compliance documents
            • General educational material

            Identify the document type automatically.

            Generate ONLY the sections that actually exist in the document.

            Possible sections include (use only relevant ones):

            Overview

            Key Concepts

            Objectives

            Key Safety Rules

            Required PPE

            Operating Procedure

            Work Process

            Responsibilities

            Equipment Used

            Maintenance Guidelines

            Inspection / Checklist

            Hazards

            Precautions

            Best Practices

           Emergency Response

           Quality Standards

           Important Warnings

           Definitions

          Do NOT include empty headings.

            For every section:

           • Use short bullet points.
           • Each bullet should contain one complete idea.
           • Avoid paragraphs.
           • Avoid repeating information.

            For long procedures:

            Convert them into numbered steps inside bullet points.

            If the document contains:

            Instructions → summarize as steps.

            Policies → summarize as rules.

            Training modules → summarize as learning points.

            Technical manuals → summarize as operating guidelines.

            Safety manuals → emphasize hazards, PPE, precautions and emergency response.

            At the end include exactly one section:

            <h3>Key Takeaway</h3>

            <p>
                One concise sentence describing the single most important message of the document.
            </p>

            Formatting Requirements

            Return ONLY valid HTML.

            Use this format:

            <h3>Heading</h3>
             <ul>
                <li>Point 1</li>
                <li>Point 2</li>
                <li>Point 3</li>
            </ul>

            Never use Markdown.

            Never use code blocks.

            Never output plain text.

            Output only HTML.
           Training Document:

{text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content