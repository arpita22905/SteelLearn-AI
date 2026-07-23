import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_quiz(text):

    prompt = f"""
You are an expert AI Learning &Development Assistant specializing in corporate training, industrial learning, technical documentation, compliance, and safety education.

Your task is to generate a professional multiple-choice assessment from the uploaded document.

The uploaded document may be ANY type, including:

• Safety manuals
• SOPs
• Machine manuals
• Technical documentation
• Manufacturing procedures
• Employee handbooks
• HR policies
• Learning modules
• Compliance documents
• General educational material

First understand the purpose, structure, and key concepts of the document before creating questions.

The goal is to evaluate whether a learner actually understood the document—not whether they can memorize isolated facts.

=========================
Question Requirements
=========================

Generate questions that test:

• Understanding
• Application
• Decision making
• Best practices
• Correct procedures
• Safety awareness
• Responsibilities
• Cause and effect
• Appropriate actions
• Correct sequence of steps
• Interpretation of document concepts

Avoid questions that simply ask the user to copy a sentence from the document.

=========================
Difficulty Distribution
=========================

Generate approximately:

• 30% Easy
• 50% Medium
• 20% Challenging

The quiz should become gradually more difficult.

=========================
Distractor Quality
=========================

Every incorrect option must be:

• Realistic
• Plausible
• Similar in wording and length to the correct answer
• Related to the document topic
• Able to mislead someone who only skimmed the document

Do NOT create obviously wrong options such as:

Casual clothes
Shoes
Bananas
Cars
Nothing

Avoid humorous or absurd choices.

The correct answer should require understanding of the document.

=========================
Document-specific Guidance
=========================

If the document is about safety:

Focus on:

• PPE
• Hazards
• Risk prevention
• Emergency response
• Safe operating procedures
• Inspection requirements
• Responsibilities
• Best practices
• Unsafe behaviours
• Correct actions in different situations

If the document is technical:

Focus on:

• Concepts
• Components
• Functions
• Configuration
• Troubleshooting
• Best practices
• Correct usage

If the document is procedural:

Focus on:

• Correct order of steps
• Required actions
• Decision points
• Preconditions
• Common mistakes

If the document is policy based:

Focus on:

• Responsibilities
• Rules
• Compliance
• Appropriate actions
• Violations
• Employee obligations

=========================
Quality Rules
=========================

1. Use ONLY information contained in the document.
2. Never invent facts.
3. Ignore duplicate text.
4. Ignore page numbers.
5. Ignore formatting.
6. Every question should assess an important concept.
7. Avoid repeating the same idea in multiple questions.
8. Every question must have exactly ONE correct answer.
9. Every option should be similar in length.
10. Avoid using words like "always" or "never" unless they appear in the document.
11. Avoid giving away the answer through wording.
12. Do not make the correct answer noticeably longer than the others.

=========================
Output Rules
=========================

Generate EXACTLY 10 questions whenever sufficient information exists.

If the document is too short, generate fewer questions rather than inventing information.

Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question text",
    "options":[
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer":2
  }}
]

Where:

0 = first option
1 = second option
2 = third option
3 = fourth option

Do NOT return Markdown.

Do NOT explain anything.

Do NOT wrap JSON inside ```.

Return ONLY valid JSON.

Training Document:

{text}
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        temperature=0.3,
    )

    response = completion.choices[0].message.content.strip()

    
    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    try:
        quiz = json.loads(response)
        return quiz

    except json.JSONDecodeError:
        print(response)
        return []