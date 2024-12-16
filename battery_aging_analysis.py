import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

# Load the dataset
df = pd.read_csv(r'H:\task 3\cleaned_dataset\metadata.csv')

def preprocess_battery_data(dataframe):
    """
    Preprocess the battery dataset to extract resistance parameters
    
    Parameters:
    dataframe (pandas.DataFrame): Raw battery dataset
    
    Returns:
    pandas.DataFrame: Processed dataframe with resistance parameters
    """
    # Filter for impedance measurements
    impedance_data = dataframe[dataframe['type'] == 'impedance'].copy()
    
    # Reset index to create a cycle representation
    impedance_data = impedance_data.reset_index(drop=True)
    impedance_data['cycle'] = range(len(impedance_data))
    
    # Rename columns for clarity
    impedance_data = impedance_data.rename(columns={
        'Re': 'Battery_impedance',
        'Rct': 'Charge_transfer_resistance'
    })
    
    return impedance_data

def visualize_battery_aging(dataframe):
    """
    Create interactive Plotly visualizations for battery aging parameters
    
    Parameters:
    dataframe (pandas.DataFrame): Preprocessed battery aging data
    
    Returns:
    None (saves HTML files with interactive plots)
    """
    # Prepare data
    processed_df = preprocess_battery_data(dataframe)
    
    # Remove rows with NaN values in resistance columns
    processed_df = processed_df.dropna(subset=['Battery_impedance', 'Charge_transfer_resistance'])
    
    # Plot 1: Battery Impedance (Re) vs Cycle Number
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=processed_df['cycle'], 
        y=processed_df['Battery_impedance'], 
        mode='lines+markers',
        name='Estimated Electrolyte Resistance (Re)',
        line=dict(color='blue')
    ))
    fig1.update_layout(
        title='Battery Electrolyte Resistance (Re) During Aging',
        xaxis_title='Cycle Number',
        yaxis_title='Resistance (Ohms)',
        template='plotly_white'
    )
    pio.write_html(fig1, file='battery_impedance_vs_cycles.html')

    # Plot 2: Charge Transfer Resistance (Rct) vs Cycle Number
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=processed_df['cycle'], 
        y=processed_df['Charge_transfer_resistance'], 
        mode='lines+markers',
        name='Estimated Charge Transfer Resistance (Rct)',
        line=dict(color='red')
    ))
    fig2.update_layout(
        title='Charge Transfer Resistance (Rct) During Aging',
        xaxis_title='Cycle Number',
        yaxis_title='Resistance (Ohms)',
        template='plotly_white'
    )
    pio.write_html(fig2, file='charge_transfer_resistance_vs_cycles.html')

    # Plot 3: Combined Resistance Parameters
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=processed_df['cycle'], 
        y=processed_df['Battery_impedance'], 
        mode='lines+markers',
        name='Electrolyte Resistance (Re)',
        line=dict(color='blue')
    ))
    fig3.add_trace(go.Scatter(
        x=processed_df['cycle'], 
        y=processed_df['Charge_transfer_resistance'], 
        mode='lines+markers',
        name='Charge Transfer Resistance (Rct)',
        line=dict(color='red')
    ))
    fig3.update_layout(
        title='Battery Resistance Parameters During Aging',
        xaxis_title='Cycle Number',
        yaxis_title='Resistance (Ohms)',
        template='plotly_white'
    )
    pio.write_html(fig3, file='combined_resistance_vs_cycles.html')

    print("Visualization files have been saved.")
    
    # Print some statistics
    print("\nDataset Statistics:")
    print(processed_df[['Battery_impedance', 'Charge_transfer_resistance']].describe())

# Run the visualization
visualize_battery_aging(df)