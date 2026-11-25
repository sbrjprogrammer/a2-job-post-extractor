
# Job Post Extractor — Sample Tests

## Sample 1: Complete job post

**Input:**

Hiring MERN Stack Developer at ABC Technologies in Karachi.
Required skills: React, Node.js, MongoDB.
Salary 150000 PKR. 3 years experience. Hybrid role.

**Output:**

```json
{
  "title": "MERN Stack Developer",
  "company": "ABC Technologies",
  "location": "Karachi",
  "salary": 150000,
  "currency": "PKR",
  "skills": ["React", "Node.js", "MongoDB"],
  "remote": false,
  "experience": "3 years"
}
```

## Sample 2: Missing salary

**Input:**

We need a React Developer at Tech Solutions.
Location Lahore. Skills include React and JavaScript.
Fresh graduates can apply.

**Output:**

```json
{
  "title": "React Developer",
  "company": "Tech Solutions",
  "location": "Lahore",
  "salary": null,
  "currency": null,
  "skills": ["React", "JavaScript"],
  "remote": null,
  "experience": "Fresh graduates can apply."
}
```

## Sample 3: Minimal job post

**Input:**

Python Developer required. Apply now.

**Output:**

```json
{
  "title": "Python Developer",
  "company": null,
  "location": null,
  "salary": null,
  "currency": null,
  "skills": ["Python"],
  "remote": null,
  "experience": null
}
```

## Sample 4: Remote job

**Input:**

Remote Backend Engineer at CloudWorks.
Work from anywhere. Skills: Python, FastAPI, PostgreSQL.
Salary 2500 USD. 4 years experience.

**Output:**

```json
{
  "title": "Backend Engineer",
  "company": "CloudWorks",
  "location": null,
  "salary": 2500,
  "currency": "USD",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "remote": true,
  "experience": "4 years"
}
```

## Sample 5: Salary range

**Input:**

Hiring Senior Node.js Engineer in Islamabad.
Salary range 200000 to 300000 PKR monthly.
Skills: Node.js, Redis, Docker.
Minimum 5 years experience.

**Output:**

```json
{
  "title": "Senior Node.js Engineer",
  "company": null,
  "location": "Islamabad",
  "salary": 300000,
  "currency": "PKR",
  "skills": ["Node.js", "Redis", "Docker"],
  "remote": null,
  "experience": "Minimum 5 years experience"
}
```
