import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


class Chain:

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED JOB PAGE

            {page_data}

            -----------------------------

            You are an expert information extractor.

            Extract every job posting from the text.

            Return ONLY valid JSON.

            Each job must contain the following fields:

            {{
                "company": "",
                "role": "",
                "experience": "",
                "skills": [],
                "description": ""
            }}

            Rules:
            - company = Hiring company's name (Nike, Amazon, Google, etc.)
            - role = Job title
            - experience = Required years of experience (if available)
            - skills = Technical skills as a list
            - description = Short summary of the job

            If multiple jobs exist, return a JSON array.

            Do not include explanations.
            Do not include markdown.
            Return only JSON.
            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(
            input={
                "page_data": cleaned_text
            }
        )

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)

        except OutputParserException:
            raise OutputParserException(
                "Context too big. Unable to parse jobs."
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION

            {job_description}

            -----------------------------

            You are Trigun, Business Development Executive at XYZ.

            XYZ is an AI & Software Consulting company specialising in:

            - Artificial Intelligence
            - Cloud Engineering
            - Software Development
            - Data Engineering
            - Automation

            Write a professional cold email to the hiring company.

            Requirements:

            - Mention the company naturally.
            - Keep the email concise (200–250 words).
            - Personalise it according to the job description.
            - Highlight only relevant capabilities.
            - Include the most relevant portfolio links:
              {link_list}
            - End with a professional call to action.
            - Do not add any preamble.
            - Return only the email.
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke(
            {
                "job_description": str(job),
                "link_list": links
            }
        )

        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))