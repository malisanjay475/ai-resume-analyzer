"""
Skills dictionary used by the skill-extraction module (M3).

Each key is the skill name shown to the user; the list holds the other
ways the same skill is commonly written in resumes and job descriptions.
Matching is case-insensitive, so only spelling variants need listing.
"""

SKILLS = {
    # Programming languages
    "Python": ["python3"],
    "Java": ["core java"],
    "JavaScript": ["js", "javascript es6", "es6"],
    "TypeScript": ["ts"],
    "C": ["c language", "c programming"],
    "C++": ["cpp", "c plus plus"],
    "C#": ["c sharp", "csharp"],
    "Go": ["golang"],
    "Rust": [],
    "Kotlin": [],
    "Swift": [],
    "PHP": [],
    "Ruby": [],
    "R": ["r programming", "r language"],
    "Dart": [],
    "SQL": ["structured query language"],
    "Bash": ["shell scripting", "shell script", "bash scripting"],

    # Web frontend
    "HTML": ["html5"],
    "CSS": ["css3"],
    "React": ["react.js", "reactjs", "react js"],
    "Angular": ["angularjs", "angular.js"],
    "Vue.js": ["vue", "vuejs", "vue js"],
    "Next.js": ["nextjs", "next js"],
    "Redux": [],
    "Tailwind CSS": ["tailwind", "tailwindcss"],
    "Bootstrap": [],
    "jQuery": ["jquery"],

    # Backend and frameworks
    "Node.js": ["node", "nodejs", "node js"],
    "Express.js": ["express", "expressjs"],
    "Django": [],
    "Flask": [],
    "FastAPI": ["fast api"],
    "Spring Boot": ["springboot", "spring"],
    "Hibernate": [],
    "ASP.NET": [".net", "dotnet", "asp.net core"],
    "Laravel": [],
    "REST API": ["rest", "restful", "rest apis", "restful api", "restful apis", "rest api development"],
    "GraphQL": [],
    "Microservices": ["microservice", "micro services"],
    "JMS": ["java message service"],

    # Databases
    "MySQL": [],
    "PostgreSQL": ["postgres"],
    "MongoDB": ["mongo"],
    "Oracle": ["oracle db", "oracle database"],
    "SQLite": [],
    "Redis": [],
    "Firebase": [],
    "DBMS": ["database management", "database management system", "rdbms"],

    # Cloud and DevOps
    "AWS": ["amazon web services"],
    "Azure": ["microsoft azure"],
    "Google Cloud": ["gcp", "google cloud platform"],
    "Docker": [],
    "Kubernetes": ["k8s"],
    "Jenkins": [],
    "CI/CD": ["ci cd", "continuous integration", "continuous deployment"],
    "Git": [],
    "GitHub": [],
    "Linux": ["unix"],
    "Terraform": [],
    "Kafka": ["apache kafka"],
    "RabbitMQ": ["rabbit mq"],

    # Data, AI and ML
    "Machine Learning": ["ml"],
    "Deep Learning": ["dl"],
    "Natural Language Processing": ["nlp"],
    "Computer Vision": ["opencv"],
    "Generative AI": ["genai", "gen ai", "llm", "llms", "large language models"],
    "Data Analysis": ["data analytics"],
    "Data Visualization": [],
    "Statistics": [],
    "Pandas": [],
    "NumPy": ["numpy"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "TensorFlow": [],
    "PyTorch": [],
    "Keras": [],
    "Matplotlib": [],
    "Power BI": ["powerbi"],
    "Tableau": [],
    "Excel": ["ms excel", "microsoft excel", "advanced excel"],

    # CS fundamentals
    "Data Structures": ["dsa", "data structures and algorithms"],
    "Algorithms": [],
    "OOP": ["object oriented programming", "object-oriented programming", "oops"],
    "Operating Systems": [],
    "Computer Networks": ["networking"],
    "System Design": [],
    "Unit Testing": ["unit tests", "pytest", "junit"],
    "Agile": ["scrum"],

    # Tools
    "Postman": [],
    "Figma": [],
    "Jira": [],
    "VS Code": ["visual studio code"],

    # Soft skills
    "Communication": ["communication skills"],
    "Teamwork": ["team player", "team work"],
    "Problem Solving": ["problem-solving"],
    "Leadership": [],
}
