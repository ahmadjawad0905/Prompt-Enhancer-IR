import streamlit as st
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(layout="wide")

st.title("Promptify")

st.markdown("### Enter your prompt")
user_query = st.text_input("", placeholder="Type your prompt here...")

st.subheader("Select Model")
model = st.selectbox('',['mistral:7b','phi3:3.8b'])

st.subheader("Select Enhancement Mode")
mode = st.radio("",["Academic","Coding","Research","Health","Travel"])

def stream_ollama(prompt, placeholder,model):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True
    )

    full_response = ""

    for line in response.iter_lines():

        if line:
            data = json.loads(line)

            if "response" in data:
                full_response += data["response"]

                # Live update UI
                placeholder.markdown(full_response)

    return full_response

# Enhance Button Click
if st.button("Enhance Prompt"):

    # Prompt and other stuff for classification of prompt
    classify_prompt = f"""
    Classify this query into one category only:

    - Coding
    - Academic
    - SEO
    - Creative
    - Business

    Query:
    {user_query}

    Return category only.
    """

    classify_payload = {
        "model": model,
        "prompt": classify_prompt,
        "stream": False
            }

    classify_response = requests.post(
                OLLAMA_URL,
                json=classify_payload
            )

    classify_result = classify_response.json()

    query_type = classify_result["response"]
    st.subheader("Query Type")
    st.success(query_type)

    # Prompt to generate Enhance Prompt
    if user_query:

         prompt = f"""
You are an expert Prompt Engineering Assistant.

The Prompt you are working on is: {user_query}

Your task is to transform vague, incomplete, or low-quality user prompts into highly detailed, optimized prompts that produce better outputs from large language models.

Your goals are:

1. Preserve the original user intent
2. Remove ambiguity
3. Add missing context when reasonable
4. Specify clear objectives
5. Add output formatting instructions
6. Define constraints and success criteria
7. Improve reasoning clarity
8. Make the prompt actionable and precise
9. Use modern prompt engineering best practices
10. Avoid changing the meaning of the original request

Enhance the prompt according to this feild: {mode}

When enhancing prompts, follow this structure whenever applicable:

- Role / Persona
- Task Objective
- Context
- Constraints
- Input Requirements
- Output Requirements
- Tone / Style
- Reasoning Instructions
- Examples (if useful)
- Success Criteria

If the original prompt lacks important information, intelligently infer likely intent without asking unnecessary questions.

Always produce:
1. An “Enhanced Prompt”
2. A short explanation of improvements made

IMPORTANT:
- Do not overcomplicate simple prompts
- Keep prompts concise but sufficiently detailed
- Maintain domain relevance
- Prefer clarity over verbosity
- Use structured formatting
- Ensure prompts are directly usable with LLMs

Example transformation:

Vague Prompt:
"write blog"

Enhanced Prompt:
"Write a 1200-word SEO-optimized blog post about the benefits of remote work for software engineers. Use a professional but conversational tone. Include an introduction, 5 clear section headings, practical examples, and a concluding summary. Target audience: early-career developers. Output in markdown format."
"""

    left_column, right_column = st.columns(2)

    with left_column:

            st.subheader("Enhanced Query")

            enhanced_placeholder = st.empty()

            enhanced_text = stream_ollama(
                prompt,
                enhanced_placeholder,
                model
            )

            st.subheader("Enhanced Query Results")

            result_placeholder = st.empty()

            # Generate Result from Enhanced Prompt
            prompt_enhance = f"""
{enhanced_text}

write a short, simple and structured response.
Maximum 2 paragraphs.
"""

            stream_ollama(
                prompt_enhance,
                result_placeholder,
                model
            )

    with right_column:

            st.subheader("Original Query")

            st.info(user_query)

            st.subheader("Original Query Results")

            original_placeholder = st.empty()

            # Generate Result for Orignal Prompt
            prompt_original = f"""
{user_query}

write a short, simple response.
Maximum 2 paragraphs.
"""

            stream_ollama(
                prompt_original,
                original_placeholder,
                model
            )

else:
 st.warning("Please enter a query first.")