from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_document(text):

    prompt = f"""
You are an AI Learning & Development assistant for an industrial training platform.

Your task is to summarize the following training document in a clean, easy-to-read format.

Requirements:

- Use ONLY information present in the document.
- Keep the summary under 250 words.
- Use short bullet points instead of long paragraphs.
- Organize the summary into relevant sections based on the document.
- Include only sections that are applicable. Do NOT invent sections if the document doesn't mention them.
- Highlight the most important safety instructions, procedures, precautions, and best practices.
- Use simple English suitable for employees and trainees.
- Avoid repeating the same information.
- Do NOT include introductions or conclusions unless necessary.
- Do NOT use Markdown (no **, ##, or ```).

Output the summary as HTML only.

Use this structure exactly:

<h3>Key Safety Rules</h3>
<ul>
<li>Bullet point</li>
<li>Bullet point</li>
</ul>

<h3>Required PPE</h3>
<ul>
<li>Bullet point</li>
</ul>

<h3>Operating Procedure</h3>
<ul>
<li>Step</li>
<li>Step</li>
</ul>

<h3>Emergency Response</h3>
<ul>
<li>Bullet point</li>
</ul>

<h3>Inspection / Checklist</h3>
<ul>
<li>Bullet point</li>
</ul>

<h3>Important Warnings</h3>
<ul>
<li>Bullet point</li>
</ul>

Key Takeaway
• One short sentence summarizing the most important message.

Important:
- If a section is not relevant to the document, omit it completely.
- Never leave empty headings.
- Never invent information.
- Keep every bullet concise (one line whenever possible).

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