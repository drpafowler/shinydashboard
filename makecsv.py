import pandas as pd
import h5py
# Define some constants
ground_truth = 'data/cGround_Truth_data_10trials_150stims_180000ms.hdf5'
submission = 'data/cNo_Inhibitory_Neurons_10trials_150stims_180000ms.hdf5'
for filename in [ground_truth, submission]:
    print(f"\nExamining file: {filename}")
    with h5py.File(filename, 'r') as f:
        print("Keys:", list(f.keys()))
        for key in f.keys():
            data_item = f[key]
            print(f"{key}: type={type(data_item)}", end='')
            if isinstance(data_item, h5py.Dataset):
                print(f", shape={data_item.shape}")
            else:
                print()

for filename in [ground_truth, submission]:
    print(f"\nExamining trial groups in file: {filename}")
    with h5py.File(filename, 'r') as f:
        for trial_name in f.keys():
            if 'trial' in trial_name.lower():
                trial_group = f[trial_name]
                if isinstance(trial_group, h5py.Group):
                    print(f"Keys in {trial_name} group:", list(trial_group.keys()))
                    for name, item in trial_group.items():
                        if isinstance(item, h5py.Dataset):
                            print(f"Dataset '{name}' in {trial_name} shape:", item.shape)
                        elif isinstance(item, h5py.Group):
                            print(f"'{name}' in {trial_name} is a group, not a dataset.")
                        else:
                            print(f"'{name}' in {trial_name} is not a group or dataset.")
                else:
                    print(f"{trial_name} is not a group, skipping.")

for fname, prefix in [(ground_truth, 'gt'), (submission, 'sub')]:
    with h5py.File(fname, 'r') as f:
        for trial_name in f.keys():
            if trial_name.startswith('trial_'):
                trial_group = f[trial_name]
                for name, item in trial_group.items():
                    if isinstance(item, h5py.Dataset):
                        data = item[()]
                        if data.ndim == 2:
                            columns = [f'neuron{i+1}' for i in range(data.shape[1])]
                            df = pd.DataFrame(data, columns=columns)
                        else:
                            df = pd.DataFrame(data)
                        # Rename columns
                        new_columns = ['time']
                        for i in range(1, (len(columns))//2 + 1):
                            new_columns.append(f'neuron{i}_spike')
                            new_columns.append(f'neuron{i}_mempot')
                        df.columns = new_columns[:df.shape[1]]
                        # Name dataframe according to file and trial
                        trial_idx = trial_name.split('_')[1]
                        globals()[f"{prefix}_trial{trial_idx}_df"] = df
# Save the DataFrames to CSV files
for prefix in ['gt', 'sub']:
    for i in range(0, 10):  # Assuming there are 10 trials
        df_name = f"{prefix}_trial{i}_df"
        if df_name in globals():
            df = globals()[df_name]
            csv_filename = f"data/{prefix}_trial{i}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Saved {df_name} to {csv_filename}")
        else:
            print(f"{df_name} does not exist.")