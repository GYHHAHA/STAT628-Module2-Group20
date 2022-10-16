import pandas as pd


if __name__ == "__main__":

    df = pd.read_csv("../data/BodyFat.csv")
    # Drop the samples with negative bodyfat by Siri density
    siri_bodyfat = 495 / df.DENSITY - 450
    negative_id = df[siri_bodyfat < 0].IDNO
    df = df[~df.IDNO.isin(negative_id)]
    # Compute the error between Siri fat and actual fat
    siri_bodyfat = 495 / df.DENSITY - 450
    err = siri_bodyfat - df.BODYFAT
    # Use 3 sigma criterion to find the abnormal samples
    mean_err = err.mean()
    std_err = 3 * err.std()
    err_id = df[(err > mean_err + std_err) | (err < mean_err - std_err)].IDNO
    # Use the density to impute the body fat
    df.loc[err_id, "BODYFAT"] = (495 / df.loc[err_id, "DENSITY"] - 450).round(1)
    # Reset index and save data
    df = df.drop(["IDNO", "DENSITY"], axis=1).reset_index(drop=True)
    df.to_csv("../data/cleaned_data.csv", index=False)
