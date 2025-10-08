import matplotlib.pyplot as plt

def bivariate_plot(df, var1, var2):
    """
    Function to plot two variables on the same plot for bivariate analysis.
    
    Parameters:
    var1 (str): The first variable name (column) from daily_df.
    var2 (str): The second variable name (column) from daily_df.
    """
    
    plt.figure(figsize=(15, 6))  # Set figure size
    
    # Plot both variables
    plt.plot(df.index, df[var1], label=var1, color="blue", linewidth=2)
    plt.plot(df.index, df[var2], label=var2, color="red", linewidth=2)

    # Improve readability
    plt.title(f"Bivariate Analysis: {var1} vs {var2} Over Time", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.show()
