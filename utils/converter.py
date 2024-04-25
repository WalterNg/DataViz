import pandas as pd


def convert2datetime(data: pd.DataFrame, datetime_var: list):
    df_date = data.copy()
    err_date = None
    # Try to convert this var into datetime object
    if len(datetime_var) > 0:
        for var in datetime_var:
            try:
                df_date[var] = pd.to_datetime(df_date[var], infer_datetime_format=True)
            
            except Exception:
                err_date = "Cannot convert this variable into datetime object."

    return df_date, err_date


def str2int(s):
    return int(s)