from resume_utils import calculate_ats_score, Formate_Resume, process_resume
from io import BytesIO
import SampleResumes as sr

# or r"SampleResume/Nishant_Kumar_Resume.docx" for docx evaluation
with open(r"SampleResume/Nishant_Singh_Resume.pdf", "rb") as f:
    buffer = BytesIO(f.read())

# print(calculate_ats_score(resume_text=Formate_Resume(buffer), job_role="Data Scientist", experience_level="I"))
# or 
# print(calculate_ats_score(resume_text=sr.R1, job_role="HR ADMINISTRATOR/MARKETING ASSOCIATE", experience_level="II"))

print(process_resume(buffer))
