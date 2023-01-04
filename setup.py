import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='linkedin-salary-tools',
    version='0.2.4',
    author='Ivan Sheng',
    author_email='is1048@nyu.edu',
    description='Python tools to pull job descriptions and extract salary bands from them.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ishengy/linkedin-salary-tools',
    project_urls = {
        "Bug Tracker": "https://github.com/ishengy/linkedin-salary-tools/issues"
    },
    license='MIT',
    packages=['linkedin_salary_tools'],
    install_requires=[
        'linkedin-api @ git+https://github.com/tomquirk/linkedin-api.git',
        'pandas',
        'numpy',
        'scipy',
        'requests',
        'bs4',
    ],
)
