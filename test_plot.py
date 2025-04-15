import os
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

current_path = os.getcwd()
results_dir = os.path.join(current_path, "data", "cge_results")
chart_dir = os.path.join(current_path, "data", "cge_charts_seaborn")
os.makedirs(chart_dir, exist_ok=True)

# Loading descriptions.csv
desc_dict = {}
desc_path = os.path.join(results_dir, "descriptions.csv")
if os.path.exists(desc_path):
    desc_df = pandas.read_csv(desc_path)
    desc_dict = dict(zip(desc_df["name"], desc_df["description"]))

# Loading all parameters
csv_files = [f for f in os.listdir(results_dir) if f.endswith(".csv") and f != "descriptions.csv"]

for filename in csv_files:
    name = filename.replace(".csv", "")
    df = pandas.read_csv(os.path.join(results_dir, filename))

    try:
        title = desc_dict.get(name, name)
        plt.figure(figsize=(10, 5))

        # 1. Only t and value - simple line
        if set(df.columns) == {"t", "value"}:
            sns.lineplot(data=df, x="t", y="value", marker='o')
            plt.title(title)
            plt.ylabel("Value")

        # 2. One additional index (eg i or j or h)
        elif "t" in df.columns and "value" in df.columns and len(df.columns) == 3:
            dim = [col for col in df.columns if col not in {"t", "value"}][0]
            sns.lineplot(data=df, x="t", y="value", hue=dim, style=dim, markers=True, dashes=False)
            plt.title(title)
            plt.ylabel("Value")
            plt.legend(title=dim, bbox_to_anchor=(1.05, 1), loc="upper left")

        # 3. Two additional indices (e.g. h, j, t)
        elif "t" in df.columns and "value" in df.columns and len(df.columns) == 4:
            dims = [col for col in df.columns if col not in {"t", "value"}]
            df["group"] = df[dims[0]].astype(str) + " | " + df[dims[1]].astype(str)
            sns.lineplot(data=df, x="t", y="value", hue="group", style="group", markers=True, dashes=False)
            plt.title(title)
            plt.ylabel("Value")
            plt.legend(title=",".join(dims), bbox_to_anchor=(1.05, 1), loc="upper left")

        plt.xlabel("Time")
        plt.tight_layout()
        # plt.savefig(os.path.join(chart_dir, f"{name}_seaborn.png"))
        # plt.close()

    except Exception as e:
        print(f"⚠️ Ошибка при построении графика для {name}: {e}")