from resume_utils import calculate_ats_score, Formate_Resume, process_resume
from io import BytesIO

with open("Nishant_Singh_Resume.pdf", "rb") as f:
    buffer = BytesIO(f.read())

# print(calculate_ats_score(resume_text=Formate_Resume(buffer), job_role="Data Scientist", experience_level="I"))

print(process_resume(buffer))
