# Import data from shared.py
from shared import app_dir
import plotly.express as px
from shared import (
    app_dir,
    gt_trial0_df, gt_trial1_df, gt_trial2_df, gt_trial3_df, gt_trial4_df, gt_trial5_df, gt_trial6_df, gt_trial7_df, gt_trial8_df, gt_trial9_df,
    sub_trial0_df, sub_trial1_df, sub_trial2_df, sub_trial3_df, sub_trial4_df, sub_trial5_df, sub_trial6_df, sub_trial7_df, sub_trial8_df, sub_trial9_df
)
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ui.page_opts(title="Submission File Explorer", fillable=True)
ui.h1("Submission File Explorer", style="text-align: center;")


# --- Sidebar for Display Controls ---
with ui.sidebar(title=ui.h2("Display Controls"), width="400px"):
    # Input for selecting the type of plot (now only Raster as per request)
    ui.input_select("plot", "Plot Type", ["Raster", "Peri Time Stimulus"], selected="Raster")

    # Input for selection of ground truth or submission data
    ui.input_select("data_type", "Data Type", ["Ground Truth", "Submission"], selected="Ground Truth")

    # Input for selection of Trial (using radio buttons as before)
    ui.input_radio_buttons("trial", "Trial", ["Trial 0", "Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9"], selected="Trial 0")

    # Input for selection of Neuron ID (now using checkboxes for multiple selection)
    all_neuron_ids = ["neuron1_spike", "neuron2_spike", "neuron3_spike", "neuron4_spike", "neuron5_spike"]
    ui.input_checkbox_group("selected_neurons", "Select Neurons", all_neuron_ids, selected=["neuron5_spike"])

    
    with ui.panel_conditional("input.plot == 'Peri Time Stimulus'"):
        # Input for selecting the bin size for histograms
        ui.input_slider("bins", "Number of Bins", min=1, max=100, value=30)
        ui.input_slider("time_window", "Time Window (ms)", min=0, max=180000, value=[100, 180000], step=100)





with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Visualisation")

        @render.plot
        def spike_plots():
            # Check if the selected plot type is Raster
            if input.plot() == "Raster":
                df = filtered_df()
                
                # Get the list of selected neurons from the input
                selected_neurons = input.selected_neurons()
                
                if not selected_neurons:
                    # Display a message if no neurons are selected
                    plt.figure(figsize=(10, 2))
                    plt.text(0.5, 0.5, "Please select at least one neuron.", 
                             horizontalalignment='center', verticalalignment='center', 
                             transform=plt.gca().transAxes, color='red')
                    return plt.gcf()

                all_spike_times = []
                neuron_labels = []
                
                # Iterate through selected neurons to collect their spike times
                for i, neuron_id in enumerate(selected_neurons):
                    if 'time' in df.columns and neuron_id in df.columns:
                        # Extract time values where the neuron spiked (value is 1)
                        spike_times_for_neuron = df[df[neuron_id] == 1]['time'].values
                        all_spike_times.append(spike_times_for_neuron)
                        neuron_labels.append(neuron_id)
                    else:
                        # Handle cases where a selected neuron column or 'time' is missing
                        plt.figure(figsize=(10, 2))
                        plt.text(0.5, 0.5, f"Error: '{neuron_id}' or 'time' column not found in data.", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=plt.gca().transAxes, color='red')
                        return plt.gcf()

                # Create the event plot (raster plot)
                # Adjust figure height based on the number of selected neurons for better visibility
                fig_height = max(2, len(selected_neurons) * 0.8) # Minimum height of 2, then 0.8 per neuron
                plt.figure(figsize=(10, fig_height))
                
                # lineoffsets will place each neuron's spikes on a different y-level
                # The y-axis labels will correspond to the neuron_labels
                plt.eventplot(
                    all_spike_times, 
                    colors='black', 
                    lineoffsets=range(len(selected_neurons)),
                    linelengths=0.8  # Change this value (e.g., 0.7 or 0.9) to adjust the gap size
                )
                plt.xlabel("Time")
                plt.yticks(range(len(selected_neurons)), neuron_labels) # Set y-axis ticks and labels
                plt.ylabel("Neuron ID")
                plt.title(f"Spike Raster Plot ({input.data_type()} - {input.trial()})")
                plt.grid(axis='x', linestyle='--', alpha=0.7) # Add a grid for readability
                plt.tight_layout() # Adjust layout to prevent labels from overlapping
                return plt.gcf()

            # Handle the "Peri Time Stimulus" plot type
            elif input.plot() == "Peri Time Stimulus":
                df = filtered_df()
                selected_neurons = input.selected_neurons()
                bins = input.bins()
                time_window = input.time_window()

                if not selected_neurons:
                    plt.figure(figsize=(10, 2))
                    plt.text(0.5, 0.5, "Please select at least one neuron.",
                             horizontalalignment='center', verticalalignment='center',
                             transform=plt.gca().transAxes, color='red')
                    return plt.gcf()

                start_time, end_time = time_window
                plt.figure(figsize=(10, 4))

                for neuron_id in selected_neurons:
                    if 'time' in df.columns and neuron_id in df.columns:
                        spike_times = df[(df[neuron_id] == 1) & (df['time'] >= start_time) & (df['time'] <= end_time)]['time'].values
                        plt.hist(spike_times, bins=bins, alpha=0.5, label=neuron_id)
                    else:
                        plt.text(0.5, 0.5, f"Error: '{neuron_id}' or 'time' column not found in data.",
                                 horizontalalignment='center', verticalalignment='center',
                                 transform=plt.gca().transAxes, color='red')
                        return plt.gcf()

                plt.xlabel("Time (ms)")
                plt.ylabel("Spike Count")
                plt.title(f"Peri Stimulus Time Histogram ({input.data_type()} - {input.trial()})")
                plt.legend()
                plt.tight_layout()


                return plt.gcf()



# Include custom CSS styles
# ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
 
    trial_idx = int(input.trial().split()[-1])  # Extract trial number from "Trial X"
    if input.data_type() == "Ground Truth":
        gt_dfs = [
            gt_trial0_df, gt_trial1_df, gt_trial2_df, gt_trial3_df, gt_trial4_df,
            gt_trial5_df, gt_trial6_df, gt_trial7_df, gt_trial8_df, gt_trial9_df
        ]
        return gt_dfs[trial_idx]
    else:  # input.data_type() == "Submission"
        sub_dfs = [
            sub_trial0_df, sub_trial1_df, sub_trial2_df, sub_trial3_df, sub_trial4_df,
            sub_trial5_df, sub_trial6_df, sub_trial7_df, sub_trial8_df, sub_trial9_df
        ]
        return sub_dfs[trial_idx]