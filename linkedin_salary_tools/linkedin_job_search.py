#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 02:17:06 2022

@author: isheng
"""

from linkedin_api import Linkedin
from .col_adjustments import col_adjustments
import pandas as pd
import re
import time
import numpy as np
import scipy.stats as stats


class linkedin_job_search(Linkedin):
    """
    Class that inherits from the linkedin_api package.

    Additional functions are explicitly used to obtain job descriptions,
    perform salary extraction, and other help functions such as developing KDE,
    bootstrap resampling, etc.
    """
    def find_salary(self, text):
        """
        Find dollar amounts within a provided string.

        Parameters:
            text (str): text containing dollar amounts to extract

        Returns:
            (list) list of string representation of dollar amounts
        """
        return re.findall(r"\$\d{2,3}\,\d{3}", text)

    def flatten(self, big_list):
        """
        Flatten list of lists into a list object, while converting
        string dollar amounts to int amounts.

        Parameters:
            big_list (list of lists): list of lists containing dollar amounts as strings

        Returns:
            (list) list of dollar amounts as ints
        """
        return [
            int(item.replace("$", "").replace(",", ""))
            for sublist in big_list
            for item in sublist
        ]

    def outlier_removal(self, arr, how="tukey"):
        """
        Remove salary outliers via a specified removal method.

        Parameters:
            arr (Pandas Series): series containing int salaries
            how (str): outlier removal methods of tukey, z-score, or modified-z

        Returns:
            removed (Pandas Series): series containing int salaries with outliers removed
        """
        if how == "tukey":
            q1 = np.quantile(arr, 0.25)
            q3 = np.quantile(arr, 0.75)
            iqr = q3 - q1

            upper_bound = q3 + (1.5 * iqr)
            lower_bound = q1 - (1.5 * iqr)

            removed = arr[(arr >= lower_bound) & (arr <= upper_bound)]
        elif how == "z-score":
            mean, std = np.mean(arr), np.std(arr)
            z_score = np.abs((arr - mean) / std)
            removed = arr[z_score < 2]
        elif how == "modified-z":
            mad = abs(arr - arr.median()).sum() / len(arr)
            m = 0.6745 * (arr - np.median(arr)) / mad
            removed = arr[abs(m) < 3.5]
        return removed

    def get_linkedin_job_desc(self, job_searches):
        """
        Aquire the job description of a LinkedIn job posting.

        Parameters:
            job_searches (list of dict): list containing job posting metadata as dict objects

        Returns:
            job_desc_list (list): list of job descriptions
        """
        job_desc_list = []
        i = 0
        cum_time = 0
        for job in job_searches:
            t0 = time.time()
            i += 1
            delimited = job["entityUrn"].split(":")
            job_id = delimited[len(delimited) - 1]
            job_desc_list.append(self.get_job(job_id)["description"]["text"])
            cum_time += time.time() - t0
            print(i, "Elapsed Time:", cum_time)

        return job_desc_list

    def extract_salaries(self, job_desc_list, exempt=True):
        """
        Function to extract salaries from job descriptions and
        flatten the object to a 1D list.

        Parameters:
            job_desc_list (list): list of job descriptions
            exempt (boolean): Whether or not to remove non-exempt salaries. Default value is True.

        Returns:
            flattened_salaries (Pandas Series): series of dollar amounts as ints
        """
        salaries = [
            self.find_salary(job_text)
            for job_text in job_desc_list
            if len(self.find_salary(job_text)) > 0
        ]
        flattened_salaries = pd.Series(self.flatten(salaries), name="salaries")

        if exempt:
            flattened_salaries = flattened_salaries[flattened_salaries >= 58500]

        return flattened_salaries

    def extract_job_title(self, job_searches):
        """
        Acquire job title from LinkedIn job postings.

        Parameters:
            job_searches (list of dict): list containing job posting metadata as dict objects

        Returns:
            (string): most frequent job title
        """
        job_title_list = [str.lower(jd["title"]) for jd in job_searches]
        return max(set(job_title_list), key=job_title_list.count)

    def bootstrap_resample(self, arr):
        """
        Bootstrap resample salaries from 3 random draws

        Parameters:
            arr (list): list containing int salaries

        Returns:
            bootstrapped_salaries (Pandas Series): bootstrapped salaries
        """
        resampled_means = pd.Series(
            [arr.sample(3).mean() for i in range(0, 1000)], name="salaries"
        )
        bootstrapped_salaries = pd.concat(
            [arr, resampled_means], ignore_index=True
        )
        return bootstrapped_salaries

    def test_normality(self, observed_data, alpha=1e-3):
        """
        Performs Chi-Square Test for Normality to check whether or not 
        the sample set of salaries follows an approximately normal distribution.

        Parameters:
            observed_data (Pandas Series): series of salaries
            alpha (float): the critical value used to reject the null hypothesis.

        Returns:
            (boolean): If the null hypothesis was rejected (False)
        """
        chi_square_test_statistic, p_value = stats.normaltest(observed_data)
        # null hypothesis: x comes from a normal distribution
        if p_value < alpha:
            # reject null hypothesis
            return False
        else:
            # can't reject null hypothesis
            return True

    def kde_estimate(self, salaries, bw_method):
        """
        Perform kernel density estimation on a sample set.

        Parameters:
            salaries (Pandas Series): series containing salaries
            bw_method (str, scalar or callable):
                The method used to calculate the estimator bandwidth.
                Sample parameter found in scipy.stats.gaussian_kde

        Returns:
            kde (numpy array): numpy array containing the KDE trained on the provided sample set.
        """
        xmin, xmax = min(salaries), max(salaries)
        x = np.linspace(xmin, xmax, 100)
        kernel = stats.gaussian_kde(salaries, bw_method=bw_method)
        kde = kernel(x)
        return kde

    def build_distribution(
        self,
        job_title_code,
        days,
        bootstrap=True,
        update_table=False,
        col_adj_city="New York, NY, United States",
        col_with_rent=True,
        limit=-1,
        experience=None,
        numbeo_path=None,
    ):
        """
        Function used to streamline process used to gather job descriptions,
        extract salaries, and develop distribution to explain the sampled salaries.

        Parameters:
            job_title_code (string): the job title code found in the URL
            days (int): the number of days to look back 
            bootstrap (boolean): whether or not to bootstrap resample the sample set
            update_table (boolean): whether or not to update the Numbeo table
            col_adj_city (string): location where you are located
            col_with_rent (boolean): use the CoL With Rent Index instead of the normal CoL (True)
            limit (int): the maximum number of job descriptions to pull (use -1 for no limit)
            experience (list of strings): 
                A list of experience levels, one or many of “1”, “2”, “3”, “4”, “5” and “6” 
                (internship, entry level, associate, mid-senior level, director, and executive, respectively)
            numbeo_path (str): path to Numbeo cost of living indices.

        Returns:
            salaries_no_outliers (Pandas Series): series containing int salaries with outliers removed
            common_title (string): most frequently used job title, 
            a (float): alpha, 
            mu (float): shape or average,
            sigma (float): scale or standard deviation, 
            n (int): number of salaries found
        """

        # GET a profile
        print("Gathering Job Postings")
        job_searches = self.search_jobs(
            job_title=[job_title_code],
            job_type=["F"],
            location_name="New York City Metropolitan Area",
            listed_at=24 * 60 * 60 * days,
            limit=limit,
            experience=experience,
        )
        common_title = self.extract_job_title(job_searches)
        num_jobs = len(job_searches)
        print(
            num_jobs,
            "jobs found. Approximately",
            num_jobs * 4,
            "seconds to extract job descriptions.",
        )

        job_desc_list = self.get_linkedin_job_desc(job_searches)
        flattened_salaries = self.extract_salaries(job_desc_list)

        salaries_no_outliers = self.outlier_removal(flattened_salaries, how="tukey")
        n = len(salaries_no_outliers)

        if bootstrap:
            print("Bootstrapping")
            try:
                resampled_means = self.bootstrap_resample(salaries_no_outliers)
                salaries_no_outliers = pd.concat(
                    [salaries_no_outliers, resampled_means], ignore_index=True
                )
                salaries_no_outliers = self.outlier_removal(
                    salaries_no_outliers, how="tukey"
                )
            except ValueError:
                print(
                    "Not enough salaries to initiate bootstrap. Try increasing the number of days."
                )

        if col_adj_city != "New York, NY, United States":
            col_table = col_adjustments(numbeo_path)
            if update_table:
                print("Updating Table")
                col_table.update_COL_table()
            print("Adjusting for COL")
            adj_factor = col_table.calc_COL_adjustment(
                city=col_adj_city, rent=col_with_rent
            )
            salaries_no_outliers *= adj_factor

        print("Creating Visuals")
        salaries_no_outliers.plot.hist(
            alpha=0.5, title="Salary Distribution (Source: LinkedIn)"
        )

        if self.test_normality(flattened_salaries):
            a, mu, sigma = 0, salaries_no_outliers.mean(), salaries_no_outliers.std()
        else:
            a, mu, sigma = stats.skewnorm.fit(salaries_no_outliers)

        return salaries_no_outliers, common_title, a, mu, sigma, n
