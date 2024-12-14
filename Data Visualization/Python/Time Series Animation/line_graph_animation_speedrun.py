import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.dates import DateFormatter

def prepare_data(df):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close'] = df['Close/Last'].str.replace('$', '').astype(float)
    df['High'] = df['High'].str.replace('$', '').astype(float)
    df['Low'] = df['Low'].str.replace('$', '').astype(float)
    return df.sort_values('Date')

def create_multi_stock_animation(amd_df, nvidia_df, intel_df):
    # Prepare the data
    amd_data = prepare_data(amd_df)
    nvidia_data = prepare_data(nvidia_df)
    intel_data = prepare_data(intel_df)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Find overall min and max dates and prices
    min_date = min(amd_data['Date'].min(), nvidia_data['Date'].min(), intel_data['Date'].min())
    max_date = max(amd_data['Date'].max(), nvidia_data['Date'].max(), intel_data['Date'].max())
    
    min_price = min(
        amd_data['Low'].min(),
        nvidia_data['Low'].min(),
        intel_data['Low'].min()
    ) * 0.95
    
    max_price = max(
        amd_data['High'].max(),
        nvidia_data['High'].max(),
        intel_data['High'].max()
    ) * 1.05
    
    # Set the x and y axis limits
    ax.set_xlim(min_date, max_date)
    ax.set_ylim(min_price, max_price)
    
    # Create empty lines with different colors
    amd_line, = ax.plot([], [], lw=2, color='#ED1C24', label='AMD')
    nvidia_line, = ax.plot([], [], lw=2, color='#76B900', label='NVIDIA')
    intel_line, = ax.plot([], [], lw=2, color='#0071C5', label='Intel')
    
    # Create text objects for prices with background boxes
    amd_text = ax.text(0, 0, '', color='white', fontweight='bold',
                      bbox=dict(facecolor='#ED1C24', alpha=0.7, edgecolor='none', pad=3))
    nvidia_text = ax.text(0, 0, '', color='white', fontweight='bold',
                         bbox=dict(facecolor='#76B900', alpha=0.7, edgecolor='none', pad=3))
    intel_text = ax.text(0, 0, '', color='white', fontweight='bold',
                        bbox=dict(facecolor='#0071C5', alpha=0.7, edgecolor='none', pad=3))
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Add title and labels
    ax.set_title('Semiconductor Stock Prices Comparison', pad=15)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    
    # Format dates on x-axis
    date_formatter = DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_formatter)
    plt.xticks(rotation=45)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.subplots_adjust(bottom=0.2)
    
    def animate(frame):
        # Update AMD data
        amd_x = amd_data['Date'].iloc[:frame]
        amd_y = amd_data['Close'].iloc[:frame]
        amd_line.set_data(amd_x, amd_y)
        
        # Update NVIDIA data
        nvidia_x = nvidia_data['Date'].iloc[:frame]
        nvidia_y = nvidia_data['Close'].iloc[:frame]
        nvidia_line.set_data(nvidia_x, nvidia_y)
        
        # Update Intel data
        intel_x = intel_data['Date'].iloc[:frame]
        intel_y = intel_data['Close'].iloc[:frame]
        intel_line.set_data(intel_x, intel_y)
        
        # Update price labels if we have data
        if len(amd_y) > 0:
            amd_text.set_position((amd_x.iloc[-1], amd_y.iloc[-1]))
            amd_text.set_text(f'AMD ${amd_y.iloc[-1]:.2f}')
            
        if len(nvidia_y) > 0:
            nvidia_text.set_position((nvidia_x.iloc[-1], nvidia_y.iloc[-1]))
            nvidia_text.set_text(f'NVIDIA ${nvidia_y.iloc[-1]:.2f}')
            
        if len(intel_y) > 0:
            intel_text.set_position((intel_x.iloc[-1], intel_y.iloc[-1]))
            intel_text.set_text(f'INTEL ${intel_y.iloc[-1]:.2f}')
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, 
        animate,
        frames=max(len(amd_data), len(nvidia_data), len(intel_data)),
        interval=5,
        repeat=False,
        blit=False
    )
    
    return anim, fig

# Load the data
amd_df = pd.read_csv('amd.csv')
nvidia_df = pd.read_csv('nvidia.csv')
intel_df = pd.read_csv('intel.csv')

# Create and display the animation
anim, fig = create_multi_stock_animation(amd_df, nvidia_df, intel_df)

anim.save('animation.mp4', 'ffmpeg', fps=60)
# anim.save('animation.gif', writer='imagemagick', fps=60)

plt.show()