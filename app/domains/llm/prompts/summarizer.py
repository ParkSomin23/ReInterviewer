prompt_template = """
### Task ###
You are a strict data analysis bot. Follow these instructions step-by-step.

### INSTRUCTIONS ###
Step 1. Read the [Target Interview Text] and divide the entire text based on each interview 'Question'.

Step 2. For each divided question text, classify and extract the fields based on these strict definitions:
  - 'question': The core interview question asked by the interviewer.
  - 'user_answer': What the user explained or said in response to the question.
  - 'interviewer_reaction': What the interviewer said, their facial expressions, feedback, or quotes like "~라고 들었음", "~라고 하셨음".
  - 'self_evaluation': The user's own thoughts, regrets, self-reflections, or future plans like "~연습 필요", "~했어야 했다", "아쉬움".
  - 'etc': Any other information that doesn't fit the above fields.

Step 3. Convert the extracted data into a raw JSON format. If any field is not explicitly mentioned, it MUST be null.

### OUTPUT FORMAT SCHEMA ###
__SCHEMA_PLACEHOLDER__

Let's think step by step. Output your analysis for Step 1, Step 2, and then output the final Step 3 JSON inside the ```json ``` block.
"""


# Target Text: __TEXT_PLACEHOLDER__
# Result JSON:
