import os
import re
import PyPDF2
import docx2txt

# A comprehensive list of common professional/technical skills to look out for
COMMON_SKILLS = [
    'python', 'django', 'flask', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
    'node.js', 'express', 'sql', 'mysql', 'postgresql', 'mongodb', 'docker', 'kubernetes',
    'aws', 'azure', 'gcp', 'linux', 'git', 'github', 'agile', 'scrum', 'jira', 'c++', 'c#',
    'java', 'ruby', 'php', 'swift', 'kotlin', 'dart', 'flutter', 'typescript', 'tailwind',
    'bootstrap', 'sass', 'figma', 'ui/ux', 'seo', 'marketing', 'sales', 'management',
    'leadership', 'communication', 'problem solving', 'machine learning', 'ai', 'data science',
    'pandas', 'numpy', 'tensorflow', 'pytorch', 'excel', 'word', 'powerpoint', 'project management'
]

# Common words to ignore when dynamically finding keywords
STOP_WORDS = {
    'the', 'is', 'a', 'and', 'or', 'in', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by',
    'as', 'this', 'that', 'it', 'be', 'are', 'was', 'were', 'will', 'experienced', 'seeking',
    'we', 'our', 'us', 'you', 'your', 'skills', 'experience', 'years', 'looking', 'work', 'team'
}

def extract_text_from_file(file_path):
    """
    Extracts plain text from a given PDF or DOCX file path.
    """
    if not os.path.exists(file_path):
        return ""

    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
        elif ext in ['.docx', '.doc']:
            text = docx2txt.process(file_path)
        else:
            # Fallback for plain text or unsupported formats
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return ""

    return text.strip()


def extract_keywords(text):
    """
    Extracts potential keywords from text by comparing against known SKILLS
    and picking up larger non-stop-words.
    """
    text = text.lower()
    
    # Simple tokenization
    words = re.findall(r'\b[a-z0-9+#\.]+\b', text)
    
    found_keywords = set()
    
    # 1. Match against known IT / Domain skills
    for skill in COMMON_SKILLS:
        if skill in text:
            found_keywords.add(skill)
            
    # 2. Add other interesting words from text (excluding stop words and tiny words)
    for w in words:
        if len(w) > 4 and w not in STOP_WORDS and not w.isnumeric():
            found_keywords.add(w)

    return found_keywords

def analyze_resume_against_job(resume_text, job_description, job_title):
    """
    Compares resume text against job description & title.
    Returns:
    - percent_match (int)
    - matched_keywords (list)
    - missing_keywords (list)
    """
    
    # 1. Prepare Text
    comb_jd = f"{job_title} {job_description}"
    resume_cleaned = resume_text.lower()
    
    # 2. Extract strictly relevant keywords from JD
    jd_keywords_potential = extract_keywords(comb_jd)
    
    # To avoid bloat, let's filter JD keywords to only things that look "important"
    # For a simple ATS, standard skills get priority
    strict_jd_keywords = set()
    for kw in jd_keywords_potential:
        # If it's a known skill or mentioned multiple times, it's important
        if kw in COMMON_SKILLS:
            strict_jd_keywords.add(kw)
            
    # If the job description is sparse on known skills, fallback to using all extracted keywords
    if len(strict_jd_keywords) < 5:
        # Take up to 15 long words from JD
        strict_jd_keywords = set(list(jd_keywords_potential)[:15])
        
    # 3. Match against Resume
    matched_keywords = []
    missing_keywords = []
    
    for kw in strict_jd_keywords:
        # Simple string match in resume text
        if re.search(r'\b' + re.escape(kw) + r'\b', resume_cleaned):
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)
            
    # 4. Calculate Percentage
    total_important = len(strict_jd_keywords)
    if total_important == 0:
        percent_match = 100 # Nothing special requested
    else:
        percent_match = int((len(matched_keywords) / total_important) * 100)
    
    # Bonus points for Title matching
    title_words = extract_keywords(job_title)
    title_bonus = 0
    for tw in title_words:
        if tw in resume_cleaned:
            title_bonus += 5
            
    final_score = min(percent_match + title_bonus, 100)

    # Clean up results for UI
    return {
        'score': final_score,
        'matched': sorted(list(set(matched_keywords))),
        'missing': sorted(list(set(missing_keywords))),
        'resume_preview': resume_text[:600] + "..." if len(resume_text) > 600 else resume_text
    }
