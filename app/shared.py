from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent.parent
csv_files = (app_dir / "data").glob("*.csv")
for f in csv_files:
    df_name = f"{f.stem}_df"
    globals()[df_name] = pd.read_csv(f)