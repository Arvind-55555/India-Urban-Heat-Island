"""
Analysis and Visualization Script for Urban Heat Island Dataset
Generates insights, correlations, and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
import glob
warnings.filterwarnings('ignore')

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_latest_dataset():
    """Load the most recent UHI dataset"""
    data_dir = '../../data/processed'
    files = glob.glob(f'{data_dir}/*uhi_dataset*.csv')
    if not files:
        print("No dataset found! Please run enhanced_collector.py first.")
        return None
    
    latest = max(files)
    print(f"Loading dataset: {latest}")
    df = pd.read_csv(latest)
    return df

def basic_statistics(df):
    """Display basic statistics"""
    print("\n" + "="*80)
    print("DATASET OVERVIEW")
    print("="*80)
    print(f"Total Cities: {len(df)}")
    print(f"Total Features: {len(df.columns)}")
    print(f"\nStates Covered: {df['State'].nunique()}")
    print(f"States: {', '.join(sorted(df['State'].unique()))}")
    
    print("\n" + "="*80)
    print("KEY METRICS SUMMARY")
    print("="*80)
    
    metrics = {
        'Temperature Range': (df['Temperature (°C)'].min(), df['Temperature (°C)'].max()),
        'UHI Intensity Range': (df['UHI Intensity (°C)'].min(), df['UHI Intensity (°C)'].max()),
        'Average NDVI': df['NDVI'].mean(),
        'Average Impervious Surface': df['Impervious Surface (%)'].mean(),
        'Average Urban Greenness': df['Urban Greenness Ratio (%)'].mean(),
        'Total Population': df['Population'].sum(),
    }
    
    for key, value in metrics.items():
        if isinstance(value, tuple):
            print(f"{key}: {value[0]:.2f}°C - {value[1]:.2f}°C")
        elif isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value:,}")

def correlation_analysis(df):
    """Analyze correlations with UHI intensity"""
    print("\n" + "="*80)
    print("CORRELATION WITH UHI INTENSITY")
    print("="*80)
    
    # Select numeric columns relevant to UHI
    uhi_factors = [
        'Temperature (°C)',
        'Impervious Surface (%)',
        'NDVI',
        'Albedo',
        'Urban Greenness Ratio (%)',
        'Population Density (people/km²)',
        'Building Density (buildings/km²)',
        'Anthropogenic Heat Flux (W/m²)',
        'Wind Speed (km/h)',
        'Distance to Water (km)',
        'Solar Radiation (MJ/m²/day)',
        'Humidity (%)',
    ]
    
    correlations = []
    for factor in uhi_factors:
        if factor in df.columns:
            corr = df['UHI Intensity (°C)'].corr(df[factor])
            correlations.append((factor, corr))
    
    # Sort by absolute correlation
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print("\nTop Factors Contributing to UHI Intensity:")
    print("-" * 80)
    for i, (factor, corr) in enumerate(correlations[:10], 1):
        direction = "↑ Positive" if corr > 0 else "↓ Negative"
        print(f"{i:2d}. {factor:45s} | r = {corr:+.3f} ({direction})")

def regional_analysis(df):
    """Analyze UHI by regions"""
    print("\n" + "="*80)
    print("REGIONAL ANALYSIS")
    print("="*80)
    
    # Group by latitude regions
    df['Region'] = pd.cut(df['Latitude'], 
                          bins=[0, 15, 23, 28, 90],
                          labels=['South (<15°N)', 'Central (15-23°N)', 
                                 'North-Central (23-28°N)', 'North (>28°N)'])
    
    regional_stats = df.groupby('Region').agg({
        'UHI Intensity (°C)': ['mean', 'std', 'min', 'max'],
        'Temperature (°C)': 'mean',
        'NDVI': 'mean',
        'Impervious Surface (%)': 'mean',
        'City Name': 'count'
    }).round(2)
    
    print("\nRegional UHI Statistics:")
    print(regional_stats)

def top_bottom_cities(df):
    """Display top and bottom cities by various metrics"""
    print("\n" + "="*80)
    print("RANKING ANALYSIS")
    print("="*80)
    
    # Top 10 UHI intensity cities
    print("\n🔥 TOP 10 CITIES - HIGHEST UHI INTENSITY:")
    print("-" * 80)
    top_uhi = df.nlargest(10, 'UHI Intensity (°C)')[
        ['City Name', 'State', 'UHI Intensity (°C)', 'Temperature (°C)', 
         'Impervious Surface (%)', 'NDVI']
    ]
    for i, row in enumerate(top_uhi.itertuples(), 1):
        print(f"{i:2d}. {row[1]:20s} ({row[2]:20s}) - UHI: {row[3]:.2f}°C, "
              f"Temp: {row[4]:.1f}°C, Impervious: {row[5]:.1f}%")
    
    # Bottom 10 UHI intensity cities (most livable)
    print("\n🌿 TOP 10 CITIES - LOWEST UHI INTENSITY (Most Livable):")
    print("-" * 80)
    bottom_uhi = df.nsmallest(10, 'UHI Intensity (°C)')[
        ['City Name', 'State', 'UHI Intensity (°C)', 'Temperature (°C)', 
         'NDVI', 'Urban Greenness Ratio (%)']
    ]
    for i, row in enumerate(bottom_uhi.itertuples(), 1):
        print(f"{i:2d}. {row[1]:20s} ({row[2]:20s}) - UHI: {row[3]:.2f}°C, "
              f"NDVI: {row[5]:.3f}, Greenness: {row[6]:.1f}%")
    
    # Highest NDVI cities
    print("\n🌳 TOP 10 CITIES - HIGHEST VEGETATION (NDVI):")
    print("-" * 80)
    top_ndvi = df.nlargest(10, 'NDVI')[
        ['City Name', 'State', 'NDVI', 'Urban Greenness Ratio (%)', 'UHI Intensity (°C)']
    ]
    for i, row in enumerate(top_ndvi.itertuples(), 1):
        print(f"{i:2d}. {row[1]:20s} ({row[2]:20s}) - NDVI: {row[3]:.3f}, "
              f"Greenness: {row[4]:.1f}%, UHI: {row[5]:.2f}°C")

def land_cover_analysis(df):
    """Analyze by land cover type"""
    print("\n" + "="*80)
    print("LAND COVER ANALYSIS")
    print("="*80)
    
    lc_stats = df.groupby('Land Cover').agg({
        'City Name': 'count',
        'UHI Intensity (°C)': 'mean',
        'NDVI': 'mean',
        'Impervious Surface (%)': 'mean',
        'Temperature (°C)': 'mean'
    }).round(2)
    
    lc_stats.columns = ['Count', 'Avg UHI (°C)', 'Avg NDVI', 'Avg Impervious (%)', 'Avg Temp (°C)']
    print(lc_stats)

def create_visualizations(df):
    """Create and save visualizations"""
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = '../../outputs/visualizations'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. UHI Intensity vs Key Factors
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Urban Heat Island Intensity vs Key Contributing Factors', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: UHI vs Impervious Surface
    axes[0, 0].scatter(df['Impervious Surface (%)'], df['UHI Intensity (°C)'], 
                      c=df['Temperature (°C)'], cmap='YlOrRd', s=100, alpha=0.6)
    axes[0, 0].set_xlabel('Impervious Surface (%)', fontsize=12)
    axes[0, 0].set_ylabel('UHI Intensity (°C)', fontsize=12)
    axes[0, 0].set_title('Effect of Impervious Surfaces')
    
    # Plot 2: UHI vs NDVI
    axes[0, 1].scatter(df['NDVI'], df['UHI Intensity (°C)'], 
                      c=df['Urban Greenness Ratio (%)'], cmap='RdYlGn', s=100, alpha=0.6)
    axes[0, 1].set_xlabel('NDVI (Vegetation Index)', fontsize=12)
    axes[0, 1].set_ylabel('UHI Intensity (°C)', fontsize=12)
    axes[0, 1].set_title('Effect of Vegetation')
    
    # Plot 3: UHI vs Population Density
    axes[1, 0].scatter(df['Population Density (people/km²)'], df['UHI Intensity (°C)'], 
                      s=100, alpha=0.6, c='coral')
    axes[1, 0].set_xlabel('Population Density (people/km²)', fontsize=12)
    axes[1, 0].set_ylabel('UHI Intensity (°C)', fontsize=12)
    axes[1, 0].set_title('Effect of Population Density')
    
    # Plot 4: UHI vs Distance to Water
    axes[1, 1].scatter(df['Distance to Water (km)'], df['UHI Intensity (°C)'], 
                      s=100, alpha=0.6, c='skyblue')
    axes[1, 1].set_xlabel('Distance to Water Bodies (km)', fontsize=12)
    axes[1, 1].set_ylabel('UHI Intensity (°C)', fontsize=12)
    axes[1, 1].set_title('Effect of Water Proximity')
    
    plt.tight_layout()
    filename1 = f'{output_dir}/uhi_factors_analysis_{timestamp}.png'
    plt.savefig(filename1, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename1}")
    plt.close()
    
    # 2. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(14, 10))
    
    correlation_cols = [
        'UHI Intensity (°C)', 'Temperature (°C)', 'Impervious Surface (%)',
        'NDVI', 'Urban Greenness Ratio (%)', 'Population Density (people/km²)',
        'Anthropogenic Heat Flux (W/m²)', 'Wind Speed (km/h)', 
        'Distance to Water (km)', 'Albedo', 'Building Density (buildings/km²)'
    ]
    
    existing_cols = [col for col in correlation_cols if col in df.columns]
    corr_matrix = df[existing_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, ax=ax,
                cbar_kws={'label': 'Correlation Coefficient'})
    ax.set_title('Correlation Matrix - UHI Factors', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    filename2 = f'{output_dir}/uhi_correlation_matrix_{timestamp}.png'
    plt.savefig(filename2, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename2}")
    plt.close()
    
    # 3. Top 15 Cities by UHI Intensity
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top15 = df.nlargest(15, 'UHI Intensity (°C)').sort_values('UHI Intensity (°C)')
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(top15)))
    
    bars = ax.barh(top15['City Name'], top15['UHI Intensity (°C)'], color=colors)
    ax.set_xlabel('UHI Intensity (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('City', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Cities by Urban Heat Island Intensity', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}°C', ha='left', va='center', fontsize=9, 
                fontweight='bold', color='darkred')
    
    plt.tight_layout()
    filename3 = f'{output_dir}/top_cities_uhi_{timestamp}.png'
    plt.savefig(filename3, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename3}")
    plt.close()
    
    # 4. NDVI vs UHI with city labels
    fig, ax = plt.subplots(figsize=(14, 10))
    
    scatter = ax.scatter(df['NDVI'], df['UHI Intensity (°C)'], 
                        s=df['Population']/10000, 
                        c=df['Impervious Surface (%)'],
                        cmap='RdYlGn_r', alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Label top UHI cities
    top_cities = df.nlargest(10, 'UHI Intensity (°C)')
    for _, city in top_cities.iterrows():
        ax.annotate(city['City Name'], 
                   (city['NDVI'], city['UHI Intensity (°C)']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, alpha=0.7)
    
    ax.set_xlabel('NDVI (Vegetation Index)', fontsize=12, fontweight='bold')
    ax.set_ylabel('UHI Intensity (°C)', fontsize=12, fontweight='bold')
    ax.set_title('NDVI vs UHI Intensity\n(Bubble size = Population, Color = Impervious Surface %)', 
                fontsize=14, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Impervious Surface (%)', fontsize=11)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    filename4 = f'{output_dir}/ndvi_vs_uhi_{timestamp}.png'
    plt.savefig(filename4, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename4}")
    plt.close()
    
    print(f"\n✓ All visualizations saved successfully!")

def export_summary(df):
    """Export summary statistics to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = '../../outputs/reports'
    os.makedirs(output_dir, exist_ok=True)
    filename = f'{output_dir}/uhi_analysis_summary_{timestamp}.txt'
    
    with open(filename, 'w') as f:
        f.write("="*80 + "\n")
        f.write("URBAN HEAT ISLAND ANALYSIS SUMMARY\n")
        f.write("50 Major Indian Cities\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("KEY FINDINGS:\n")
        f.write("-"*80 + "\n")
        f.write(f"1. Average UHI Intensity: {df['UHI Intensity (°C)'].mean():.2f}°C\n")
        f.write(f"2. Highest UHI: {df['City Name'].iloc[df['UHI Intensity (°C)'].idxmax()]} "
                f"({df['UHI Intensity (°C)'].max():.2f}°C)\n")
        f.write(f"3. Lowest UHI: {df['City Name'].iloc[df['UHI Intensity (°C)'].idxmin()]} "
                f"({df['UHI Intensity (°C)'].min():.2f}°C)\n")
        f.write(f"4. Average Impervious Surface: {df['Impervious Surface (%)'].mean():.1f}%\n")
        f.write(f"5. Average NDVI: {df['NDVI'].mean():.3f}\n")
        f.write(f"6. Average Urban Greenness: {df['Urban Greenness Ratio (%)'].mean():.1f}%\n\n")
        
        f.write("CORRELATION WITH UHI INTENSITY:\n")
        f.write("-"*80 + "\n")
        factors = ['Impervious Surface (%)', 'NDVI', 'Population Density (people/km²)',
                  'Anthropogenic Heat Flux (W/m²)', 'Wind Speed (km/h)']
        for factor in factors:
            if factor in df.columns:
                corr = df['UHI Intensity (°C)'].corr(df[factor])
                f.write(f"{factor:45s}: {corr:+.3f}\n")
    
    print(f"\n✓ Summary exported to: {filename}")

def main():
    """Main analysis function"""
    print("\n" + "="*80)
    print("URBAN HEAT ISLAND DATA ANALYSIS")
    print("="*80)
    
    # Load data
    df = load_latest_dataset()
    if df is None:
        return
    
    # Run analyses
    basic_statistics(df)
    correlation_analysis(df)
    regional_analysis(df)
    land_cover_analysis(df)
    top_bottom_cities(df)
    
    # Create visualizations
    try:
        create_visualizations(df)
    except Exception as e:
        print(f"Warning: Visualization creation failed: {e}")
        print("Make sure matplotlib and seaborn are installed: pip install matplotlib seaborn")
    
    # Export summary
    export_summary(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nFiles generated:")
    print("  • Correlation heatmap")
    print("  • UHI factors scatter plots")
    print("  • Top cities bar chart")
    print("  • NDVI vs UHI bubble chart")
    print("  • Summary statistics text file")
    print("\nRecommended next steps:")
    print("  1. Review visualizations for patterns")
    print("  2. Identify cities requiring UHI mitigation")
    print("  3. Develop targeted green infrastructure strategies")
    print("  4. Monitor seasonal changes with repeated data collection")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

