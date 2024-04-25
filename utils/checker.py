import pandas as pd


def is_csv(filename: str):
    return filename.endswith('csv')

def is_excel(filename: str):
    return filename.endswith('sheet')
