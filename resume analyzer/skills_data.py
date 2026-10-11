"""
skills_data.py
--------------
A curated list of common skills (technical + soft) used to scan
resume and job description text for matches. Extend these lists
as needed for your target roles.
"""

TECHNICAL_SKILLS = [
    # Programming languages
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "r",
    "go", "rust", "php", "swift", "kotlin", "scala", "matlab",

    # Data / ML
    "machine learning", "deep learning", "data analysis", "data analytics",
    "data science", "data visualization", "natural language processing", "nlp",
    "computer vision", "artificial intelligence", "statistics",
    "linear regression", "logistic regression", "decision tree", "random forest",
    "neural networks", "tensorflow", "pytorch", "scikit-learn", "keras",
    "pandas", "numpy", "matplotlib", "seaborn", "power bi", "tableau",
    "big data", "hadoop", "spark", "etl",

    # Web / software dev
    "html", "css", "react", "angular", "vue", "node.js", "express",
    "django", "flask", "rest api", "graphql", "microservices",
    "software development", "object oriented programming", "oop",
    "agile", "scrum", "git", "github", "ci/cd", "docker", "kubernetes",

    # Cloud / infra
    "aws", "azure", "gcp", "cloud computing", "linux", "devops",

    # Databases
    "mysql", "postgresql", "mongodb", "oracle", "firebase", "redis",

    # Other tech
    "cybersecurity", "networking", "blockchain", "ui/ux", "figma",
    "excel", "vba", "salesforce", "sap",
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "project management", "attention to detail",
    "decision making", "conflict resolution", "presentation skills",
    "negotiation", "mentoring", "public speaking", "customer service",
    "analytical skills", "multitasking", "organization",
]

ALL_SKILLS = sorted(set(TECHNICAL_SKILLS + SOFT_SKILLS), key=len, reverse=True)