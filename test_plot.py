import os
import pandas
import matplotlib.pyplot as plt

# Loading descriptions
current_path = os.getcwd()
results_dir = os.path.join(current_path, "data", "cge_results")

desc_df = pandas.read_csv(os.path.join(results_dir, "descriptions.csv"))
desc_dict = dict(zip(desc_df["name"], desc_df["description"]))

# Loading all parameters
csv_files = [f for f in os.listdir(results_dir) if f.endswith(".csv") and f != "descriptions.csv"]
dfs = {}

for filename in csv_files:
    name = filename.replace(".csv", "")
    df = pandas.read_csv(os.path.join(results_dir, filename))
    dfs[name] = df
    globals()[name] = df

    # Let's plot the parameters with 1 or 2 indices (for example, EV[t] or dXp[i, t])
    try:
        plt.figure(figsize=(8, 4))
        title = desc_dict.get(name, name)

        if "t" in df.columns and "value" in df.columns:
            if "sector" in df.columns or "i" in df.columns or "j" in df.columns or "h" in df.columns:
                # group by time
                df.groupby("t")["value"].mean().plot(marker='o')
                plt.ylabel("Mean Value")
            else:
                df.plot(x="t", y="value", title=title, marker='o', legend=False)
                plt.ylabel("Value")

            plt.title(title)
            plt.xlabel("Time")
            plt.tight_layout()
            # plt.savefig(f"cge_charts_labeled/{name}.png")
            plt.close()
    except Exception as e:
        print(f"⚠️ Error while plotting the graph for {name}: {e}")