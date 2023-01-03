# linkedin-salary-tools

Python tools built to retrieve job descriptions from LinkedIn jobs, extract salary band information, built distributions, adjust for cost of living, etc.

## Purpose
Since November 1st 2022, NYC law mandates that salary bands are included in most job descriptions. This makes New York City one of a handful of locations that provide this information even before the interview stage. In an attempt to make this data even more accessible to people out looking for a new job or negotiating a raise, I created this repo to house a couple classes that will gather job descriptions from LinkedIn for specific job titles, extract the salary band information, develop a distribution, and even attempt to rescale that data to another location based on cost of living adjustments indicies with NYC as its baseline.

## Credits
`Linkedin_salary_tools` directly inherits from [linkedin-api](https://github.com/tomquirk/linkedin-api), which was developed by [tomquirk and co](https://github.com/tomquirk/). 

As such, all parent [Legal Notices](https://github.com/tomquirk/linkedin-api#legal) and [Terms and Conditions](https://github.com/tomquirk/linkedin-api#terms-and-conditions) apply to this child repo too (also included at the bottom of this README).

## Installation
**Python > 3.6 required!**

This repo can be pip installed via:
`pip install git+https://github.com/ishengy/linkedin-salary-tools`

A pypi option is currently not on the roadmap.

## Getting started
**Finding Job Title Codes**

After selecting a *Title* within *All Filters* on the LinkedIn Job Search page:

![linkedin all filters](/images/linkedin_filter.png)

you can find the associated code after "f_T=" in the URL:
<pre>
https://www.linkedin.com/jobs/search/?currentJobId=1234567890&<b>f_T=25190</b>
</pre>


**Sample Code**
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

**Dealing with a `CHALLENGE`**

If you encounter a `CHALLENGE` after calling `linkedin_job_search()`, it's most likely due to 2FA. The parent repo states that rate limiting could also be a potential reason, but it looks like no jobs are returned instead of being issued a challenge.

## How does the API work?
Because this repo's main focus deals with salary extraction please refer to [linkedin-api's in-depth overview](https://github.com/tomquirk/linkedin-api#in-depth-overview).

## How are the salary distributions developed?
NYC only requires salary bands to be disclosed so we have an abundance of lower and upper bounds. This usually creates a short and wide bell shaped curve after extracting enough bands. Bootstrap resampling was implemented to develop the shape into what should be either a normal or skewed-normal distribution since averaging a few randomly sampled bounds should result in numbers that will fall in the middle and build up the peak if performed enough times. 

## Legal
This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Linkedin or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.

This project violates Linkedin's User Agreement Section 8.2, and because of this, Linkedin may (and will) temporarily or permanently ban your account. We are not responsible for your account being banned.

## Terms and Conditions
By using this project, you agree to the following Terms and Conditions. We reserve the right to block any user of this repository that does not meet these conditions.

### Usage
This project may not be used for any of the following:

- Commercial use
- Spam
- Storage of any Personally Identifiable Information
- Personal abuse (i.e. verbal abuse)
