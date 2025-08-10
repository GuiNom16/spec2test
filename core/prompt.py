def get_prompt(requirements_text):
    return f"""
You are an AI assistant that extracts software test cases from the provided requirements.

Output ONLY a valid CSV table with exactly two columns separated by a pipe "|":

Title|Description

RULES:
- The header row must be exactly: Title|Description
- Each row must contain one meaningful test case Title and a full Description
- Titles or Descriptions cannot be empty or placeholders like "-" or "N/A"
- Do NOT include any IDs, numbering, bullet points, notes, explanations, or extra text
- If no valid test cases exist, output exactly these two lines and nothing else:

Title|Description
-|-

CRITICAL: When no test cases are found, output ONLY the two lines above. Do NOT add any explanatory text, notes, or comments about why no test cases were found.

- Do NOT output anything else, no extra lines or comments
- Every test case must be clear and meaningful, no placeholders or empty fields allowed
- Absolutely do NOT output any notes, comments, explanations, or summaries after the CSV table.
- The output must end immediately after the last test case row; no trailing text or blank lines.
- NO EXPLANATORY TEXT EVER - not even when no test cases are found

NEGATIVE EXAMPLES — DO NOT OUTPUT:
Title|Description
-|-
Note: no test cases found.

or

Title|Description
-|-
This is because no requirements matched.

or any other text after or before the CSV

Example correct output:

Title|Description
Editor Can Automate Article Review Process|The system allows the editor to automate the article review process by providing tools for efficient organization, tracking, and approval of articles.
Editor Cannot Automate Incomplete or Unreviewed Articles|The system prevents the editor from automating the publishing process until all necessary reviews are complete.

Example when no test cases found (output exactly this, nothing more):

Title|Description
-|-

Now extract test cases from the following requirements and output ONLY the CSV in the above format:

{requirements_text}
"""
