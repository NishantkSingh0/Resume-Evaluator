# LLM-Based Advanced ATS Resume Evaluator

## Overview
This project is an advanced Applicant Tracking System (ATS) resume evaluator powered by Large Language Models (LLMs). It processes raw resumes, extracts structured information, and evaluates them based on key criteria such as experience, skills, education, designation, and role level. The system leverages multiple LLMs (e.g., GPT-4o-mini, LLaMA-4-16e, LLaMA-4-128e) to provide robust evaluation scores and insights.

## Features
Resume Processing: Converts raw resumes (PDF, DOCX, or unstructured text) into structured JSON format.
ATS Evaluation: Scores resumes based on experience, skills, education, designation, and role level.
Model Comparison: Analyzes evaluation performance across different LLMs.
Sample Data: Includes sample resumes and evaluation outputs for testing and demonstration.

## Project Structure\
```
├── Outputs/                  # Sample evaluation outputs from the model
├── Reports/                  # Analysis of evaluation scores across models (GPT-4o-mini, LLaMA-4-16e, LLaMA-4-128e)
├── SampleResume/             # Raw resumes in PDF and DOCX formats for testing
├── SampleResume.py           # 10 sample unstructured text-based resumes for evaluation
├── main.py                   # Main script to execute the evaluation workflow
├── Resume_utils.py           # Core utilities for resume processing and ATS scoring
└── README.md                 # Project documentation
```

## Installation
#### 1. Clone the Repository:
```
git clone https://github.com/your-username/llm-ats-resume-evaluator.git
cd llm-ats-resume-evaluator
```
#### 2. Set Up Environment: Ensure Python 3.8+ is installed. Install dependencies:
```
pip install -r requirements.txt
```
`Note`: Ensure you have access to the LLMs (e.g., GPT-4o-mini, LLaMA models) via APIs or local deployment. Update configurations in main.py accordingly.

#### 3. Install Additional Tools:
```
For PDF/DOCX processing: Install PyPDF2, python-docx, or similar libraries.
For LLM inference: Configure access to models (e.g., OpenAI API, Hugging Face, or local LLaMA models).
```


## Usage

### Prepare Resumes:

1. Place raw resumes in `PDF/DOCX format in the SampleResume/ directory` or use the provided `SampleResume.py for set of 10 unstructured text-based resumes`.
2. `Run the Evaluator`: Execute the main script to process resumes and generate ATS scores:
```
python main.py
```

### This will:

- Process resumes using `Resume_utils.py`.
- Generate structured JSON outputs on `process_resume()` call.
  ```
  {
    "InterviewInfo": {
        "areas": ["Machine Learning Algorithms", "Data Preprocessing", "Model Evaluation Techniques", "Project Deployment", "Leadership and Teamwork"], 
        "subtopics": [
            "Understanding and application of various ML algorithms like Linear Regression, K-Means, ANN, and CNN.", 
            "Techniques for cleaning, merging, and handling missing data to enhance model performance.", 
            "Knowledge of metrics such as F1 Scores, MAE, MSE, and accuracy for evaluating model effectiveness.", 
            "Experience in deploying models using modern ML pipelines and tools like TensorFlow and Gradio.", 
            "Experience in leading teams in a hackathon setting and during live projects, showcasing collaboration and leadership skills."
        ]
    }, 
    "Formate Resume": {
        "FullName": "NISHANT KUMAR", 
        "Designation": "Data Scientist", 
        "Years of experience": 0.17, 
        "Educations": [
            {
                "UniversityName": "Haridwar University", 
                "Course": "Bachelor's in Computer Application", 
                "Year": [2023, 2026]
            }
        ], 
        "Skills": ["Advanced-Python", "C/C++", "Java", "JavaScript", "NumPy", "Pandas", "Scikit-learn", "OpenCV", "Matplotlib", "Keras", "Seaborn", "NLP", "LoRA", "TensorFlow", "LangChain", "LangGraph", "Flask", "React", "Jupyter", "Kaggle", "Colab", "VS-Code", "Github", "Git", "Firebase", "Fly.io", "Vercel", "Render", "Gradio", "StreamLit"], 
        "Experience": [
            {
                "OrgName": "Haridwar University", 
                "Year": [2025, 2025], 
                "Designation": "Data Science Intern"
            }, {
                "OrgName": "Onlei Technologies", 
                "Year": [2025, 2025], 
                "Designation": "Data Science Intern"
            }
        ]
    }
  }
  ```
- Calculate ATS scores based on your `Designation, RoleLevel, and Years_of_experience` on `calculate_ats_score` call.
```
{
    "total_score": 78, 
    "category_scores": {
        "Relevant skills and technologies": 32, 
        "Experience matching the job role": 20, 
        "Education and certifications": 12, 
        "Summary clarity and completeness": 14
    }, 
    "feedback": "The applicant demonstrates a strong understanding of key data science concepts and tools, with relevant internship experience and a solid educational background. However, the experience is somewhat limited for a one-year level, and the summary could benefit from clearer articulation of career objectives and skills alignment."
}
```

## View Reports:

Check the Reports/ directory for comparative analysis of evaluation scores across different LLMs (GPT-4o-mini, LLaMA-4-16e, LLaMA-4-128e). Your can adjust model based on your need and efficiency..  



## Key Files

- `main.py`: Orchestrates the workflow, calling resume processing and ATS evaluation functions.
- `Resume_utils.py`:
  - `process_resume()`: Extracts structured information (e.g., skills, experience, education) from raw resumes and outputs JSON.
  - `Calculate_ATS_scores()`: Evaluates resumes based on experience, skills, education, designation, and role level.
- `SampleResume.py`: Contains 10 sample unstructured text resumes for testing.
- `Outputs/`: Stores sample evaluation results from the model.
- `Reports/`: Contains analysis of model performance across different LLMs.
- `SampleResume/`: Includes raw resumes in PDF and DOCX formats for testing.

## Example Workflow

1. Place a resume (PDF, DOCX, or text) in `SampleResume/`.
2. Run `main.py` to process the resume and generate ATS scores.
3. Check `Outputs/` for the evaluation results in JSON format.
4. Review `Reports/` for insights on model performance.

## Model Details
The current evaluator mainly uses GPT-4o-mini. but you can adjust them based on your needs. and our reports on each each below models on different raw resumes
- `GPT-4o-mini`: Lightweight, efficient model for general-purpose evaluation.
- `LLaMA-4-16e`: Optimized for high accuracy in structured data extraction.
- `LLaMA-4-128e`: Enhanced model for complex resume evaluations.
`Note`: Ensure you have proper access to these models (via API or local deployment) and configure credentials in resume_utils.py.
