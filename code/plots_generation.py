import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def scatter_plot_for_density_and_fat(df):
    sns.set_theme(style="darkgrid")
    sns.relplot(data=df, x="BODYFAT", y="DENSITY")
    plt.ylabel("Density", size=15)
    plt.xlabel("Body Fat", size=15)
    siri_density = 495 / (df.BODYFAT + 450)
    err = siri_density - df.DENSITY
    mean_err = err.mean()
    std_err = 3 * err.std()
    err_ids = df[(err > mean_err + std_err) | (err < mean_err - std_err)].IDNO
    err_df = df[df.IDNO.isin(err_ids)]
    plt.plot(
        err_df.BODYFAT,
        err_df.DENSITY,
        'o',
        markerfacecolor='none',
        markeredgecolor="r",
        markersize=15
    )
    for err_id in err_ids:
        x = df.loc[df.IDNO==err_id, "BODYFAT"].iloc[0]
        y = df.loc[df.IDNO==err_id, "DENSITY"].iloc[0]
        plt.annotate(f"ID: {err_id}", (x+2, y-0.005))
    plt.title("Scatter Plot for Body Fat and Density", size=15)
    plt.tight_layout()
    plt.savefig("../image/scatter_plot_for_density_and_fat.png", dpi=100)
    return err_ids

def hist_plot_for_error(df, err_ids):
    plt.cla()
    siri_bodyfat = 495 / df.DENSITY - 450
    err = siri_bodyfat - df.BODYFAT
    ax = sns.histplot(err, kde=False, stat="density", label="samples")
    ax.set_title("Hist Plot for Errors", size=15)
    for err_id in err_ids:
        x = err.loc[df.IDNO==err_id].iloc[0]
        plt.annotate(f"ID: {err_id}", (x-1, 0.03))
    plt.ylabel("Density for Errors", size=15)
    plt.xlabel("Errors", size=15)
    plt.tight_layout()
    plt.savefig("../image/hist_plot_for_errors", dpi=100)

if __name__ == "__main__":

    df = pd.read_csv("../data/BodyFat.csv")
    # drop negative body fat
    siri_bodyfat = 495 / df.DENSITY - 450
    negative_id = df[siri_bodyfat < 0].IDNO
    df = df[~df.IDNO.isin(negative_id)]

    err_ids = scatter_plot_for_density_and_fat(df)
    hist_plot_for_error(df, err_ids)
