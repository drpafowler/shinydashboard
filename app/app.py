# Import data from shared.py
from shared import app_dir, gt_trial0_df, sub_trial0_df, gt_trial1_df, sub_trial1_df
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ui.page_opts(title="Submission File Explorer", fillable=True)
ui.h1("Submission File Explorer", style="text-align: center;")


with ui.sidebar(title=ui.h2("Display Controls"), width="400px"):
    # Input for selecting the type of plot
    ui.input_select("plot", "Plot Type", ["Raster"], selected="Raster") # add more plot types as needed

    # Input for selection of ground truth or submission data
    ui.input_select("data_type", "Data Type", ["Ground Truth", "Submission"], selected="Ground Truth")


    # Input for selection of Trial
    ui.input_radio_buttons("trial", "Trial", ["Trial 0", "Trial 1"], selected="Trial 0")

    # Input for selection of Neuron ID
    ui.input_radio_buttons("neuron_id", "Neuron ID", ["neuron1_spike", "neuron2_spike", "neuron3_spike", "neuron4_spike", "neuron5_spike"], selected="neuron5_spike")

    # Input for selecting yaxis variable
    ui.input_select("yaxis", "Y-axis Variable", ["spike_count", "membrane_potential"], selected="spike_count")
    
    with ui.panel_conditional("input.plot == 'Membrane Potential'"):
        # Assuming 'time' or similar numeric column for x-axis for membrane potential
        ui.input_select("xaxis", "X-axis Variable", ["time", "other_numeric_col"], selected="time") 
        ui.input_numeric("bins", "Number of Bins", value=30)
        # Assuming some categorical column for hue, or 'None' if no hue
        ui.input_select("hue_control", "Hue Variable", ["None", "some_categorical_col"], selected="None")




with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Visualisation")

        @render.plot
        def spike_plots():
            # Check if the selected plot type is Raster
            if input.plot() == "Raster":
                df = filtered_df()
                
                # Find the 'time' values where the selected neuron's spike column equals 1
                if 'time' in df.columns and input.neuron_id() in df.columns:
                    spike_times = df[df[input.neuron_id()] == 1]['time'].values
                else:
                    plt.figure(figsize=(10, 2))
                    plt.text(0.5, 0.5, "Error: 'time' or selected neuron column not found.", 
                             horizontalalignment='center', verticalalignment='center', 
                             transform=plt.gca().transAxes, color='red')
                    return plt.gcf()

                # Create the event plot (raster plot)
                plt.figure(figsize=(10, 2))
                # lineoffsets=1 places all spikes on a single horizontal line at y=1
                plt.eventplot(spike_times, colors='black', lineoffsets=1) 
                plt.xlabel("Time")
                plt.ylabel("Spikes") # Label for the single line of spikes
                plt.title(f"Spike Raster Plot: {input.neuron_id()} ({input.data_type()} - {input.trial()})")
                return plt.gcf()

            # Handle the "Membrane Potential" plot type
            elif input.plot() == "Membrane Potential":
                df = filtered_df()

                # from your dataframes in shared.py that contain membrane potential data.
                if input.xaxis() not in df.columns:
                    plt.figure(figsize=(10, 5))
                    plt.text(0.5, 0.5, f"Error: X-axis variable '{input.xaxis()}' not found.", 
                             horizontalalignment='center', verticalalignment='center', 
                             transform=plt.gca().transAxes, color='red')
                    return plt.gcf()

                hue_col = input.hue_control() if input.hue_control() != "None" else None
                if hue_col and hue_col not in df.columns:
                     plt.figure(figsize=(10, 5))
                     plt.text(0.5, 0.5, f"Error: Hue variable '{input.hue_control()}' not found.", 
                              horizontalalignment='center', verticalalignment='center', 
                              transform=plt.gca().transAxes, color='red')
                     return plt.gcf()

                # Example for a histogram, adjust as per your 'Membrane Potential' visualization needs
                plt.figure(figsize=(10, 5))
                sns.histplot(
                    data=df,
                    x=input.xaxis(),
                    bins=input.bins(),
                    hue=hue_col,
                    kde=True,
                    multiple="stack",
                )
                plt.title(f"Membrane Potential: {input.xaxis()} ({input.data_type()} - {input.trial()})")
                return plt.gcf()



# Include custom CSS styles
# ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    if input.data_type() == "Ground Truth":
        if input.trial() == "Trial 0":
            return gt_trial0_df
        else: # input.trial() == "Trial 1"
            return gt_trial1_df
    else: # input.data_type() == "Submission"
        if input.trial() == "Trial 0":
            return sub_trial0_df
        else: # input.trial() == "Trial 1"
            return sub_trial1_df