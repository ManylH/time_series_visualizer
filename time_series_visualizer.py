import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    "fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date"
)

# Clean data by filtering out days when page views were in the top 2.5% or bottom 2.5% of the dataset.
low = df["value"].quantile(0.025)
high = df["value"].quantile(0.975)
df = df[(df["value"] >= low) & (df["value"] <= high)]


def draw_line_plot():
    """Draws a line plot of daily page views.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The resulting figure object.
    """

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    """Draws a bar plot of average monthly page views grouped by year.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The resulting figure object.
    """

    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Group by year and month and get the mean
    df_bar_grouped = (
        df_bar.groupby(["year", "month"])["value"]
        .mean()
        .reset_index()
    )

    # Ensure correct month order
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df_bar_grouped["month"] = pd.Categorical(
        df_bar_grouped["month"], categories=month_order, ordered=True
    )
    df_bar_grouped = df_bar_grouped.sort_values(["year", "month"])

    # Pivot for plotting
    df_pivot = df_bar_grouped.pivot(index="year", columns="month", values="value")

    # Plot
    fig = df_pivot.plot(kind="bar", figsize=(12, 7)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.tight_layout()

    # Save image and return fig
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    """Draws two box plots: year-wise and month-wise.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The resulting figure object.
    """

    # Prepare data for box plots
    df_box = df.copy().reset_index()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Order months correctly
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x="year", y="value", data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    fig.tight_layout()

    # Save image and return fig
    fig.savefig("box_plot.png")
    return fig
