-- Step 1: Disable RLS for all tables (for demo/presentation)
ALTER TABLE IF EXISTS resumes DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS jobs DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS scores DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS ats_scores DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS interviews DISABLE ROW LEVEL SECURITY;

-- Step 2: Add more realistic job postings
INSERT INTO jobs (title, description, company, location, salary, requirements, skills) VALUES
(
  'React Frontend Developer',
  'We need a talented React developer to build beautiful, responsive user interfaces. You will work closely with designers and backend developers to create seamless user experiences.',
  'Digital Solutions Co',
  'New York, NY',
  '$100,000 - $130,000',
  '["3+ years React experience", "Strong JavaScript/TypeScript skills", "Experience with state management (Redux/Context)", "Responsive design", "RESTful APIs"]'::jsonb,
  '["React", "TypeScript", "Redux", "Tailwind CSS", "Git", "Jest"]'::jsonb
),
(
  'DevOps Engineer',
  'Looking for a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines. Experience with AWS, Docker, and Kubernetes required.',
  'CloudTech Systems',
  'Remote',
  '$130,000 - $160,000',
  '["5+ years DevOps experience", "AWS/Azure/GCP", "Docker and Kubernetes", "CI/CD pipelines", "Infrastructure as Code"]'::jsonb,
  '["AWS", "Docker", "Kubernetes", "Terraform", "Jenkins", "Python"]'::jsonb
),
(
  'Data Scientist',
  'Join our data science team to build machine learning models and extract insights from large datasets. Experience with Python, TensorFlow, and SQL required.',
  'Analytics Pro',
  'Boston, MA',
  '$110,000 - $140,000',
  '["MS/PhD in Computer Science or related field", "3+ years ML experience", "Python and SQL", "Statistical analysis", "Data visualization"]'::jsonb,
  '["Python", "TensorFlow", "Pandas", "SQL", "scikit-learn", "Tableau"]'::jsonb
),
(
  'Mobile App Developer (React Native)',
  'Build cross-platform mobile applications using React Native. Work on consumer-facing apps with millions of users.',
  'MobileFirst Inc',
  'Los Angeles, CA',
  '$105,000 - $135,000',
  '["3+ years mobile development", "React Native experience", "iOS and Android deployment", "RESTful APIs", "Git"]'::jsonb,
  '["React Native", "JavaScript", "TypeScript", "Redux", "Firebase", "Git"]'::jsonb
),
(
  'Backend Engineer (Node.js)',
  'We are seeking a backend engineer to build scalable APIs and microservices. Strong experience with Node.js, Express, and databases required.',
  'WebScale Solutions',
  'Austin, TX',
  '$115,000 - $145,000',
  '["4+ years Node.js experience", "Express/NestJS", "MongoDB or PostgreSQL", "Microservices architecture", "Testing frameworks"]'::jsonb,
  '["Node.js", "Express", "MongoDB", "PostgreSQL", "Redis", "Docker"]'::jsonb
),
(
  'UI/UX Designer',
  'Create beautiful and intuitive user interfaces. Work with product managers and developers to design user-centered experiences.',
  'Design Hub',
  'Seattle, WA',
  '$90,000 - $120,000',
  '["3+ years UI/UX design", "Figma/Sketch expertise", "User research", "Prototyping", "Design systems"]'::jsonb,
  '["Figma", "Sketch", "Adobe XD", "Prototyping", "HTML/CSS", "User Research"]'::jsonb
),
(
  'Machine Learning Engineer',
  'Build and deploy ML models at scale. Work on computer vision, NLP, and recommendation systems.',
  'AI Innovations',
  'Remote',
  '$140,000 - $180,000',
  '["MS/PhD preferred", "5+ years ML experience", "PyTorch or TensorFlow", "MLOps", "Cloud platforms"]'::jsonb,
  '["Python", "PyTorch", "TensorFlow", "Docker", "Kubernetes", "AWS"]'::jsonb
),
(
  'Cybersecurity Analyst',
  'Protect our systems and data from security threats. Perform security audits, vulnerability assessments, and incident response.',
  'SecureNet Corp',
  'Washington, DC',
  '$100,000 - $130,000',
  '["3+ years security experience", "CISSP or CEH certified", "Network security", "Penetration testing", "Security frameworks"]'::jsonb,
  '["Network Security", "Penetration Testing", "SIEM", "Python", "Linux", "Cloud Security"]'::jsonb
),
(
  'Product Manager',
  'Define product strategy and roadmap. Work with engineering, design, and business teams to deliver successful products.',
  'ProductCo',
  'San Diego, CA',
  '$125,000 - $155,000',
  '["5+ years product management", "Technical background", "Agile/Scrum", "Data-driven decision making", "Stakeholder management"]'::jsonb,
  '["Product Strategy", "Agile", "SQL", "Analytics", "Jira", "Roadmapping"]'::jsonb
),
(
  'QA Automation Engineer',
  'Build automated testing frameworks and ensure product quality. Experience with Selenium, Cypress, or similar tools required.',
  'Quality First Labs',
  'Chicago, IL',
  '$95,000 - $125,000',
  '["3+ years QA automation", "Selenium/Cypress", "JavaScript or Python", "CI/CD integration", "Test planning"]'::jsonb,
  '["Selenium", "Cypress", "JavaScript", "Python", "Jest", "Jenkins"]'::jsonb
)
ON CONFLICT DO NOTHING;

-- Verify jobs exist
SELECT COUNT(*) as total_jobs FROM jobs;
