import pandas as pd


def convert2datetime(data, datetime_var):
    err_date = None
    df_date = data.copy()
    if len(datetime_var) > 0:

        # Try to convert this var into datetime object
        for var in datetime_var:
            try:
                df_date[var] = pd.to_datetime(df_date[var])
            
            # If fail, it means that this var is unconvertable into datetime object
            # Which means it carrying only year or month or day

            # In case of year and day, because they are already numbers --> sorted by lineplot() function
            # In case of month, we need to do it explicitly

            except Exception:
                month_order_full = ['January','February','March','April','May','June','July','August','September','October','November','December']
                month_order_abbre = ['Jan','Feb','March','April','May','Jun','July','Aug','Sept','Oct','Nov','Dec']
                try:
                    df_date = df_date.set_index(var).loc[month_order_abbre]
                    df_date = df_date.reset_index()
                except Exception:
                    try:
                        df_date = df_date.set_index(var).loc[month_order_full]
                        df_date = df_date.reset_index()
                    except Exception:
                        err_date = "Cannot convert this variable into datetime object."

    return df_date, err_date