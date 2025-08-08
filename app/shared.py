# shared.py
from pathlib import Path
import pandas as pd

# This assumes the 'data' directory is a subdirectory of where shared.py resides.
# When exporting with shinylive, ensure your 'data' folder is inside your app's main folder.
_data_dir = Path(__file__).parent / "data"

# Dictionary to temporarily hold all dataframes during loading
_all_dfs_loaded = {}

# List of all expected trial names and data types
_trial_indices = range(10)
_data_prefixes = ["gt", "sub"]

# Load all dataframes explicitly
for prefix in _data_prefixes:
    for i in _trial_indices:
        df_name = f"{prefix}_trial{i}_df"
        file_path = _data_dir / f"{prefix}_trial{i}.csv"
        try:
            _all_dfs_loaded[df_name] = pd.read_csv(file_path)
        except FileNotFoundError:
            _all_dfs_loaded[df_name] = pd.DataFrame() # Provide an empty DataFrame as a fallback
            print(f"Warning: {file_path} not found. Using empty DataFrame for {df_name}.")

# Now, assign the loaded DataFrames to module-level variables
# This makes them directly importable by app.py
gt_trial0_df = _all_dfs_loaded['gt_trial0_df']
gt_trial1_df = _all_dfs_loaded['gt_trial1_df']
gt_trial2_df = _all_dfs_loaded['gt_trial2_df']
gt_trial3_df = _all_dfs_loaded['gt_trial3_df']
gt_trial4_df = _all_dfs_loaded['gt_trial4_df']
gt_trial5_df = _all_dfs_loaded['gt_trial5_df']
gt_trial6_df = _all_dfs_loaded['gt_trial6_df']
gt_trial7_df = _all_dfs_loaded['gt_trial7_df']
gt_trial8_df = _all_dfs_loaded['gt_trial8_df']
gt_trial9_df = _all_dfs_loaded['gt_trial9_df']

sub_trial0_df = _all_dfs_loaded['sub_trial0_df']
sub_trial1_df = _all_dfs_loaded['sub_trial1_df']
sub_trial2_df = _all_dfs_loaded['sub_trial2_df']
sub_trial3_df = _all_dfs_loaded['sub_trial3_df']
sub_trial4_df = _all_dfs_loaded['sub_trial4_df']
sub_trial5_df = _all_dfs_loaded['sub_trial5_df']
sub_trial6_df = _all_dfs_loaded['sub_trial6_df']
sub_trial7_df = _all_dfs_loaded['sub_trial7_df']
sub_trial8_df = _all_dfs_loaded['sub_trial8_df']
sub_trial9_df = _all_dfs_loaded['sub_trial9_df']

# You can still expose app_dir if needed, but it's not used for DF loading in this approach.
app_dir = Path(__file__).parent