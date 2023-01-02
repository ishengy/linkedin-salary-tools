# linkedin-salary-tools

## Abstract

Since November 1st 2022, NYC law mandates that salary bands are included in the job description. This makes New York City one of a handful of locations that provide this information even before the interview stage. In an attempt to make this data even more easily accessible to people out looking for a new job or negotiating a raise, I created this repo to house a few classes that will gather job descriptions from LinkedIn for specific job titles, extract the salary band information, develop a distribution, and even attempt to rescale that data to another location based on cost of living adjustments indicies with NYC as its baseline.

It's not a perfect solution but I hope this information will provide some benefit for someone out there.

## Installation

Python >= 3.6 required!

This repo can be pip installed via: 
`pip install git+https://github.com/ishengy/linkedin-salary-tools`

A pypi option is on the roadmap.

## Getting started

```
from linkedin_salary_tools import ls_tools

# Authenticate using Linkedin account credentials
api = ls_tools.linkedin_job_search('email_here', 'password_here')

```
