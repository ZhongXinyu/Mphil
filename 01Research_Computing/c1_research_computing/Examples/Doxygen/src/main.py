"""!@mainpage
@section intro_sec Introduction
This is the introduction.

@section install_sec Installation
This is the installation.

@section example_sec Example
This is the example.

@author J.Fergusson
@date 08/11/2023

@file main.py
@brief Main script for Examples/Doxygen/src.
@details This script imports the fraction_tools module from Examples/Doxygen/src/package1 and uses it to add two fractions.
@package package1
"""

from package1 import fraction_tools as ft


fraction1 = (1,2)
fraction2 = (1,3)

print("The sum of",fraction1,"and",fraction2,"is",ft.add(fraction1,fraction2))