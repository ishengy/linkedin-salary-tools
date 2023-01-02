# linkedin-salary-tools

## Abstract
Since November 1st 2022, NYC law mandates that salary bands are included in the job description. This makes New York City one of a handful of locations that provide this information even before the interview stage. In an attempt to make this data even more easily accessible to people out looking for a new job or negotiating a raise, I created this repo to house a few classes that will gather job descriptions from LinkedIn for specific job titles, extract the salary band information, develop a distribution, and even attempt to rescale that data to another location based on cost of living adjustments indicies with NYC as its baseline.

It's not a perfect solution but I hope this information will provide some benefit for someone out there.

## Credits:
The foundations of this repo were developed by [tomquirk](https://github.com/tomquirk/). `Linkedin_salary_tools` directly inherits from his [linkedin-api repo](https://github.com/tomquirk/linkedin-api). 

As such, all parent [Legal Notices](https://github.com/tomquirk/linkedin-api#legal) and [Terms and Conditions](https://github.com/tomquirk/linkedin-api#terms-and-conditions) apply to this child repo too (also included at the bottom of this README).

## Installation
**Python >= 3.6 required!**

This repo can be pip installed via:
`pip install git+https://github.com/ishengy/linkedin-salary-tools`

A pypi option is currently not on the roadmap.

## Getting started
**Example usage:**
``` python
from linkedin_salary_tools import ljs

# Authenticate using Linkedin account credentials
api = ljs.linkedin_job_search('email_here', 'password_here')

job_searches = api.search_jobs(
    job_title = ['25190'],
    job_type=['F'],
    location_name = 'New York City Metropolitan Area',
    limit = 100,
)

job_desc_list = api.get_linkedin_job_desc(job_searches)
salaries = api.extract_salaries(job_desc_list)
```

## Legal
This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Linkedin or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.

This project violates Linkedin's User Agreement Section 8.2, and because of this, Linkedin may (and will) temporarily or permanently ban your account. We are not responsible for your account being banned.

## Terms and Conditions
By using this project, you agree to the following Terms and Conditions. We reserve the right to block any user of this repository that does not meet these conditions.

Usage
This project may not be used for any of the following:

- Commercial use
- Spam
- Storage of any Personally Identifiable Information
- Personal abuse (i.e. verbal abuse)
