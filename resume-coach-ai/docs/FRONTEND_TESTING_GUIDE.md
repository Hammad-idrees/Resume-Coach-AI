# Frontend End-to-End Testing Guide

**Your frontend is running at**: `http://localhost:5173`

Follow these test flows step-by-step and check off each item as you complete it.

---

## 🧪 TEST FLOW 1: Job Parser

### Steps to Test:

1. **Open**: `http://localhost:5173/job-parser` in your browser

2. **Paste this sample job description**:
```
We are seeking a Senior Machine Learning Engineer with 5+ years of experience in Python, TensorFlow, and PyTorch. Must have strong NLP skills and experience with model deployment on AWS. Responsibilities include building and deploying ML models, working with large datasets, and collaborating with cross-functional teams. Master's degree in Computer Science preferred. Salary: $140,000 - $180,000.
```

3. **Click "Parse Job Description"** button

4. **✅ Expected Results**:
   - Loading spinner appears
   - After 2-3 seconds, results displayed:
     - **Skills**: Python, TensorFlow, PyTorch, NLP, AWS (5+ skills)
     - **Experience**: "5+ years" or "5 years"
     - **Entities**: Multiple items with labels (ORG, DATE, PRODUCT, etc.)
     - **Job Title**: Machine Learning Engineer or similar
     - **Salary**: $140,000 - $180,000

5. **❌ Check for Issues**:
   - [ ] Does loading spinner show?
   - [ ] Does it take longer than 5 seconds?
   - [ ] Are skills displayed?
   - [ ] Is experience extracted?
   - [ ] Any console errors? (Press F12)

6. **Test Edge Case**: Clear the text area and click parse
   - Should show error message "Job description required"

---

## 🧪 TEST FLOW 2: ATS Optimization

### Steps to Test:

1. **Open**: `http://localhost:5173/ats-optimization`

2. **Paste Sample Resume** (Left text area):
```
John Doe
Software Engineer

EXPERIENCE
Software Engineer at Tech Corp (2019-2024)
- Developed REST APIs using Python and FastAPI
- Built microservices with Docker and Kubernetes
- Managed PostgreSQL databases
- Implemented CI/CD pipelines with Jenkins

Junior Developer at StartupXYZ (2017-2019)
- Created web applications using React and Node.js
- Worked with MongoDB databases

SKILLS
Python, JavaScript, React, Node.js, Docker, PostgreSQL, Git

EDUCATION
BS Computer Science, State University (2017)
```

3. **Paste Sample Job Description** (Right text area):
```
Senior Software Engineer

Requirements:
- 5+ years of Python experience
- Strong knowledge of FastAPI or Django
- Experience with AWS and cloud deployment
- Docker and Kubernetes expertise
- PostgreSQL or MySQL database skills
- CI/CD pipeline management
- RESTful API design

Skills: Python, FastAPI, AWS, Docker, Kubernetes, PostgreSQL, Terraform, Redis
```

4. **Click "Analyze ATS Score"** button

5. **✅ Expected Results**:
   - ATS Score displayed (expect 40-70/100)
   - Score color coded:
     - Green if ≥70
     - Yellow if 50-69
     - Red if <50
   - **Keyword Match Percentage** (expect 50-70%)
   - **Missing Keywords** (red badges): AWS, Terraform, Redis, Django
   - **Matched Keywords** (green badges): Python, FastAPI, Docker, Kubernetes, PostgreSQL
   - **Suggestions** (5-9 items):
     - Specific recommendations like "Add AWS experience"
     - Section suggestions

6. **❌ Check for Issues**:
   - [ ] Does score calculate correctly?
   - [ ] Are colors correct?
   - [ ] Do badges show for keywords?
   - [ ] Are suggestions actionable?
   - [ ] Any errors in console?

7. **Test Edge Cases**:
   - Leave resume empty → Should show error
   - Leave job empty → Should show error
   - Very short text (10 words) → Should still work

---

## 🧪 TEST FLOW 3: Interview Simulation (CRITICAL TEST)

### Steps to Test:

1. **Open**: `http://localhost:5173/interview`

2. **Paste Job Description**:
```
Full Stack Developer position requiring React, Node.js, Express, and MongoDB. Must have 3+ years of experience building scalable web applications. Knowledge of TypeScript and REST APIs required. Experience with Agile methodology preferred.
```

3. **Click "Start Interview"** button

4. **✅ Expected Results - Question Generation**:
   - After 2-3 seconds, see:
     - **5 questions** displayed
     - Progress bar showing "Question 1 of 5"
     - Categories visible: Introduction, Technical, Behavioral, Situational, Motivation
   - Questions relevant to the job (should mention React, Node.js, etc.)

5. **Answer Question 1** - Type this answer:
```
I have 4 years of experience as a Full Stack Developer. I've worked extensively with React on the frontend, building component-based UIs with hooks and state management. On the backend, I use Node.js with Express to create RESTful APIs. I'm passionate about building user-friendly applications and writing clean, maintainable code. I've led a team of 3 developers on a major e-commerce project that handles 10,000+ daily users.
```

6. **Click "Submit Answer"** button

7. **✅ Expected Results - Answer Evaluation**:
   - Loading spinner for 1-2 seconds
   - Evaluation card appears showing:
     - **Score**: 7-10/10 (green if ≥7, yellow if 5-6, red if <5)
     - **Strengths** (2-4 items):
       - "Provided specific examples"
       - "Mentioned relevant technologies"
       - etc.
     - **Improvements** (0-2 items)
   - Progress updates to "Question 2 of 5"
   - Next question appears below

8. **Answer Question 2** - Type short answer:
```
Yes, I know Node.js.
```

9. **Click "Submit Answer"**

10. **✅ Expected Results - Low Score**:
    - Score: 2-4/10 (red or yellow)
    - Improvements should mention:
      - "Answer too brief"
      - "No specific examples"
      - "Could provide more details"

11. **Answer Remaining 3 Questions** with decent answers (50+ words each)

12. **✅ Expected Results - Final Results**:
    - After submitting 5th answer, see:
      - **Overall Score**: 0-100
      - **Grade**: A+, A, B, C, or D
      - **Average Score**: X.X/10
      - **Category Breakdown**:
        - Introduction: X.X/10
        - Technical: X.X/10
        - Behavioral: X.X/10
        - Situational: X.X/10
        - Motivation: X.X/10
      - All 5 answers with scores visible
      - Color-coded score badges

13. **❌ Check for Issues**:
    - [ ] Do all 5 questions generate?
    - [ ] Does progress bar update?
    - [ ] Do evaluations appear after each answer?
    - [ ] Are scores color-coded correctly?
    - [ ] Does final results page show?
    - [ ] Any console errors?

14. **Test Edge Cases**:
    - Empty job description → Should show error
    - Submit empty answer → Should show validation error
    - Very long answer (500+ words) → Should still work

---

## 🧪 TEST FLOW 4: Navigation & Routing

### Steps to Test:

1. **Open**: `http://localhost:5173/`

2. **Check Sidebar**:
   - [ ] Can you see sidebar on left?
   - [ ] Does it have 4 menu items?
     - Job Parser
     - ATS Optimization  
     - Interview Practice
     - (possibly Home/Dashboard)

3. **Click Each Menu Item**:
   - [ ] Click "Job Parser" → Goes to `/job-parser`
   - [ ] Click "ATS Optimization" → Goes to `/ats-optimization`
   - [ ] Click "Interview Practice" → Goes to `/interview`

4. **Test Browser Navigation**:
   - [ ] Click browser back button → Goes to previous page
   - [ ] Click browser forward button → Goes forward
   - [ ] Refresh page → Stays on same route (no 404)

5. **Test Direct URL Access**:
   - Type `http://localhost:5173/job-parser` → Loads correctly
   - Type `http://localhost:5173/ats-optimization` → Loads correctly
   - Type `http://localhost:5173/interview` → Loads correctly
   - Type `http://localhost:5173/invalid-route` → Shows 404 or redirects

6. **❌ Check for Issues**:
   - [ ] Any route gives 404?
   - [ ] Sidebar active state highlights correct item?
   - [ ] Page content loads on each route?

---

## 🧪 TEST FLOW 5: Responsive Design (Mobile/Tablet)

### Steps to Test:

1. **Open DevTools**: Press `F12` → Click "Toggle Device Toolbar" (Ctrl+Shift+M)

2. **Test Mobile (iPhone 12 - 390x844)**:
   - Select "iPhone 12" from dropdown
   - [ ] Sidebar collapses to hamburger menu?
   - [ ] Text areas stack vertically on ATS page?
   - [ ] Buttons are touchable (min 44x44px)?
   - [ ] Text is readable (not too small)?
   - [ ] No horizontal scrolling?

3. **Navigate to Each Page**:
   - `/job-parser` - Check text area and button layout
   - `/ats-optimization` - Check dual text areas stack
   - `/interview` - Check question/answer layout

4. **Test Tablet (iPad - 768x1024)**:
   - Select "iPad" from dropdown
   - [ ] Layout looks good?
   - [ ] Two-column layouts work?
   - [ ] Buttons and inputs properly sized?

5. **Test Landscape Mode**:
   - Rotate device (click rotate icon)
   - [ ] Layout adjusts properly?
   - [ ] No content cut off?

6. **❌ Check for Issues**:
   - [ ] Any overlapping text?
   - [ ] Buttons too small to tap?
   - [ ] Scrolling issues?
   - [ ] Content overflows?

---

## 🧪 TEST FLOW 6: Error Handling

### Steps to Test:

1. **Network Errors** (Test with ML service stopped):
   - Stop ML service: Go to uvicorn terminal, press `Ctrl+C`
   - Try to parse a job description
   - [ ] Does it show a clear error message?
   - [ ] No app crash?
   - Restart ML service: `uvicorn app:app --reload`

2. **Invalid Input**:
   - Enter special characters: `@#$%^&*()` in text areas
   - [ ] Does it handle gracefully?
   - Paste very long text (10,000+ words)
   - [ ] Does it process or show limit message?

3. **Empty Inputs**:
   - Click buttons without entering data
   - [ ] Shows validation errors?
   - [ ] Error messages are clear?

---

## 📋 TESTING CHECKLIST SUMMARY

### ✅ All Tests Completed:

- [ ] **Job Parser**: Extracts skills, experience, entities
- [ ] **ATS Optimization**: Shows score, keywords, suggestions
- [ ] **Interview Simulation**: 5 questions, evaluations, final results
- [ ] **Navigation**: All routes work, no 404s
- [ ] **Responsive**: Works on mobile (390px) and tablet (768px)
- [ ] **Error Handling**: Graceful failures, clear error messages

### 🐛 Bugs Found:

1. Bug: ___________________________________
   - Page: ___________________
   - Steps to reproduce: ___________________
   - Expected: ___________________
   - Actual: ___________________

2. Bug: ___________________________________
   - Page: ___________________
   - Steps to reproduce: ___________________
   - Expected: ___________________
   - Actual: ___________________

3. Bug: ___________________________________
   - Page: ___________________
   - Steps to reproduce: ___________________
   - Expected: ___________________
   - Actual: ___________________

---

## 🎯 CRITICAL FEATURES TO VERIFY

**Must Work Before Demo:**

1. ✅ Interview generates 5 questions
2. ✅ Interview evaluates each answer with score
3. ✅ Final interview results show overall grade
4. ✅ ATS shows color-coded score with keywords
5. ✅ Job parser extracts skills correctly
6. ✅ All pages load without console errors
7. ✅ Mobile layout doesn't break

---

## 📸 Screenshots to Take (For Presentation)

While testing, take screenshots of:

1. **Job Parser Page** - With parsed results showing skills
2. **ATS Optimization** - Showing score, keywords, suggestions
3. **Interview Start** - 5 questions displayed
4. **Interview Evaluation** - Single answer with score/feedback
5. **Interview Final Results** - Overall score and grade
6. **Mobile View** - One page on mobile layout

Save screenshots to: `docs/screenshots/` folder

---

## ⏱️ Estimated Testing Time

- **Flow 1 (Job Parser)**: 5 minutes
- **Flow 2 (ATS)**: 7 minutes
- **Flow 3 (Interview)**: 15 minutes ⭐ Most important
- **Flow 4 (Navigation)**: 5 minutes
- **Flow 5 (Responsive)**: 10 minutes
- **Flow 6 (Error Handling)**: 5 minutes

**Total**: ~45-50 minutes for complete testing

---

## 🚀 NEXT STEPS AFTER TESTING

1. Document any bugs found
2. Fix critical issues (if any)
3. Take screenshots for presentation
4. Move to creating presentation slides
5. Update README with screenshots

---

**Ready to Start Testing?** 🎬

Open `http://localhost:5173/interview` and begin with the Interview Simulation (most critical feature)!
