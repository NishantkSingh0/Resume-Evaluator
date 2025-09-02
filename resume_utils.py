from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from docx import Document
from pdfminer.high_level import extract_text
from typing import Union
import zipfile
import json
import os
import re

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

gpt4o_mini = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.7,
    openai_api_key=os.getenv('OPENAI_API_KEY'),
)

def resume_type(data: bytes) -> str:
    """Checks type of input buffer (Docx, PDF, DOC)"""

    if hasattr(data, "getvalue"):
        data = data.getvalue()

    # Checks for if buffer type is PDF
    if data.startswith(b'%PDF'):
        return 'pdf'

    # Checks for if buffer type is Docx
    if data.startswith(b'PK'):
        try:
            with zipfile.ZipFile(BytesIO(data)) as zf:
                names = zf.namelist()
                if any(n.startswith('word/') for n in names):
                    return 'docx'
        except zipfile.BadZipFile:
            pass  # Not a valid zip → not a docx

    # Checks for if buffer type is Doc
    if data[:8] == b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1':
        return 'doc'

    return ''


def Formate_Resume(file_bytes: bytes) -> str:
    """Extracts text informations from Buffer bytes"""

    ftype = resume_type(file_bytes)
    if ftype.lower() not in ['pdf','docx']:
        return "Invalid formate Error"

    if ftype == 'pdf':
        return extract_text(file_bytes)
    
    if ftype == 'docx':
        doc = Document(file_bytes)
        return "\n".join(p.text for p in doc.paragraphs)
    
    return "Invalid formate Error"


def _get_comprehensive_analysis(resume: str, date, model) -> dict:
    """takes raw resume fetched text and date -> returns a structured json containing all specific details"""

    SystemPrompt="""You are an expert HR analyst and career coach. Your task is to process a raw text resume and extract structured details, then generate 5 core areas for interview assessment."""
    UserInput=f"""### Input:
    - Raw Resume: {resume}
    - Current Date: {date}"""+"""
    ### Output:
    Return a **valid JSON** in the following structure:

    {
      "InterviewInfo": {
        "areas": ["area1", "area2", "area3", "area4", "area5"],
        "subtopics": ["Desc1", "Desc2", "Desc3", "Desc4", "Desc5"]
      },
      "Formate Resume": {
        "FullName": string,
        "Designation": string,
        "Years of experience": float,
        "Educations": [
          {"UniversityName": string, "Course": string, "Year": [start_year, end_year]}
        ],
        "Skills": ["skill1", "skill2", ...],
        "Experience": [
          {"OrgName": string, "Year": [start_year, end_year], "Designation": string}
        ]
      }
    }

    ### Rules:
    1. Extract details accurately from the raw resume.
    2. Use the current date to calculate total years of experience.
    3. For "InterviewInfo", choose 5 areas relevant to the candidate's domain and experience.
    4. Provide a short description on every InterviewInfo -> Role
    5. Return only **valid JSON** without extra text."""

    response = model.invoke([
            {"role": "system", "content": SystemPrompt},
            {"role": "user", "content": UserInput},
        ])
    
    json_match = re.search(r'({[\s\S]*})', response.content)
    if json_match:
        json_str = json_match.group(1)
        return json.loads(json_str)
    else:
        return {
            "InterviewInfo": {
                "areas": [],
                "Desc": [],
            },
            "Formate Resume": {
                "FullName": "Arjun Mehta", 
                "Designation": "HR Administrator/Marketing Associate", 
                "Years of experience": 15.75, 
                "Educations": [{
                    "UniversityName": "", 
                    "Course": "", 
                    "Year": [2005, 2015 ]
                }], 
                "Skills": [],
                "Experience": [{
                    "OrgName": "", 
                    "Year": [2007, 2010], 
                    "Designation": ""
                }]
            }
        }


def process_resume(ResumeBuffer: bytes) -> dict:
    """Takes File as buffer, Read them, and Structure into processed json formate"""
    resumeText=Formate_Resume(ResumeBuffer)
    date=datetime.now().strftime("%Y-%m")
    jsonOut=_get_comprehensive_analysis(resumeText, date, model=gpt4o_mini)
    return jsonOut


def calculate_ats_score(resume_text: str, job_role: str, experience_level: Union[int, str], resume_type: str="summary") -> dict:
    """
    Calculates ATS score based on resume content and job requirements.
    Sample input:- resume_text: str, job_role: str, experience_level: Union[int, str], resume_type: str, model: ChatOpenAI
    """
    try:
        # Define the system and user messages
        if resume_type.lower() == "summary":
            system_message = """You are an ATS system, you just have to answer json structured output of resume score
        
            "total_score": numeric value between 0 to 100
            "category_scores":{
                  Relevant skills and technologies (0 to 40 points), 
                  Experience matching the job role (0 to 30 points), 
                  Education and certifications (0 to 15 points), 
                  Summary clarity and completeness (0 to 15 points)
                }
            "feedback": brief feedback explaining the score"""
            user_message = f"""evaluate the following **AI-generated LinkedIn applicant summary**. for a {job_role} position with {experience_level} experience level. \n\n Applicant Summary: {resume_text}"""
        
        else:
            system_message = """You are an ATS system evaluator for resume. you just have to answer json structured output of resume score
            
            "total_score": numeric value between 0 to 100
            "category_scores":{
                  Relevant skills and technologies (0 to 40 points), 
                  Experience matching the job role (0 to 30 points), 
                  Education and certifications (0 to 15 points), 
                  Resume formatting and clarity (0 to 15 points)
                }
            "feedback": brief feedback explaining the score"""
            user_message = f"""evaluate the following resume for a {job_role} position with {experience_level} experience level. \n\n Resume: {resume_text}"""

        # Invoke the model with the messages
        response = gpt4o_mini.invoke([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ])

        # Access the content of the response
        if hasattr(response, 'content'):  # For AIMessage objects
            result_text = response.content
        elif isinstance(response, dict) and "choices" in response:
            result_text = response["choices"][0]["message"]["content"]
        else:
            raise ValueError("Unexpected response format")

        # Extract JSON from the result
        json_match = re.search(r'({[\s\S]*})', result_text)
        if json_match:
            json_str = json_match.group(1)
            parsed_result = json.loads(json_str)
        else:
            parsed_result = {
                "total_score": 0,
                "category_scores": {
                    "skills": 0,
                    "experience": 0,
                    "education": 0,
                    "formatting": 0,
                },
                "feedback": "JSON parsing failed. Default score assigned.",
            }

        return parsed_result

    except Exception as e:
        return {
            "total_score": 0,
            "category_scores": {
                "skills": 0,
                "experience": 0,
                "education": 0,
                "formatting": 0,
            },
            "feedback": f"Error in ATS scoring: {e}",
        }