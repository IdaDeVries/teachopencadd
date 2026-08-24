from pathlib import Path
import pandas as pd
import nbformat
from nbclient import NotebookClient

results = []

for nb_path in sorted(Path("talktorials").glob("*/talktorial.ipynb")):
    print(f"Testing {nb_path}")

    try:
        nb = nbformat.read(nb_path, as_version=4)

        client = NotebookClient(
            nb,
            timeout=120,  # maximum 120 seconds per cell
            kernel_name="python3",
        )

        client.execute()

        results.append(
            {
                "Notebook": nb_path.parent.name,
                "Status": "PASS",
                "Error": "",
            }
        )

    except Exception as e:
        results.append(
            {
                "Notebook": nb_path.parent.name,
                "Status": "FAIL",
                "Error": f"{type(e).__name__}: {e}",
            }
        )

# Reporting
report = pd.DataFrame(results)
print("summary:\n", report)
report.to_csv("talktorial_status.csv", index=False)
print("Report saved as talktorial_status.csv")