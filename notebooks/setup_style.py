"""
Setup script for matplotlib and seaborn styling
"""

import matplotlib.pyplot as plt
import seaborn as sns

def setup_style():
    """Set up the correct plotting style"""
    plt.style.use('seaborn-v0_8')  # Use the correct style name
    sns.set_palette('husl')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    
# If run directly
if __name__ == "__main__":
    setup_style()
