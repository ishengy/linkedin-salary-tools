#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 02:17:06 2022

@author: isheng
"""

import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup


class col_adjustments:
    """
    Class that contains functions used to obtain the latest Cost of Living indicies from Numbeo.
    """

    def __init__(self):
        """
        Constructor that grabs the most recently scraped Numbeo Cost of Living table
        and all cities with an index.
        """
        self.bls_state_salary = pd.read_csv("data/numbeo_col.csv")
        self.cities = self.bls_state_salary.City.unique()

    def update_COL_table(self):
        """
        Function used to scrape Numbeo's current Cost of Living Index table.

        Parameters:
            None

        Returns:
            msg (string): status message as to whether or not table was updated
        """
        table_url = "https://www.numbeo.com/cost-of-living/rankings_current.jsp"
        response = requests.get(table_url)
        status_code = response.status_code

        if status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            col_table = soup.find("table", {"class": "stripe"})
            df = pd.read_html(str(col_table))[0].drop(columns="Rank")
            df["order"] = np.where(df.City == "New York, NY, United States", 1, 0)
            df = df.sort_values(["order"], ascending=False)
            df.to_csv("data/numbeo_col.csv", index=False)
            msg = "COL Table Updated"
        else:
            msg = "COL Table Not Updated."

        return msg

    def calc_COL_adjustment(self, city, rent=True):
        """
        Obtained the Cost of Living Index.

        Parameters:
            city (string): city to adjust to
            rent (boolean): use the CoL With Rent Index instead of the normal CoL (True)

        Returns:
            col_city_index (float): Cost of Living Index
        """
        city_row = self.bls_state_salary[self.bls_state_salary.City == city]
        if rent:
            col = "Cost of Living Plus Rent Index"
        else:
            col = "Cost of Living Index"

        col_city_index = city_row[col].values[0] / 100

        return col_city_index
