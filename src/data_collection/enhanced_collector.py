"""
Enhanced UHI Data Collector with Additional Factors
Includes NDVI estimates, albedo, impervious surfaces, and other UHI-specific metrics
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
from typing import Dict, List
import math
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(__file__))

class EnhancedUHICollector:
    """Enhanced collector with additional UHI factors"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def calculate_distance_to_water(self, lat: float, lon: float, city_name: str) -> float:
        """
        Calculate approximate distance to nearest major water body (km)
        Based on known locations of rivers/coasts for Indian cities
        """
        # Coastal cities (distance = 0-5 km)
        coastal_cities = {
            'Mumbai': 2, 'Chennai': 3, 'Visakhapatnam': 1, 'Thiruvananthapuram': 5,
            'Surat': 8, 'Kolkata': 15
        }
        
        # River cities (distance = 1-10 km)
        river_cities = {
            'Delhi': 5, 'Ahmedabad': 8, 'Pune': 12, 'Hyderabad': 7,
            'Varanasi': 2, 'Allahabad': 1, 'Patna': 3, 'Kanpur': 4,
            'Lucknow': 6, 'Agra': 3, 'Srinagar': 1, 'Guwahati': 2
        }
        
        if city_name in coastal_cities:
            return coastal_cities[city_name]
        elif city_name in river_cities:
            return river_cities[city_name]
        else:
            # Estimate based on geography
            return np.random.uniform(15, 50)
    
    def estimate_ndvi(self, lat: float, lon: float, city_name: str, greenness_ratio: float) -> float:
        """
        Estimate NDVI (Normalized Difference Vegetation Index)
        Range: -1 to 1 (typically 0.2-0.8 for vegetation)
        Would ideally come from Sentinel-2 or Landsat data
        """
        # NDVI correlates with urban greenness
        # Urban areas: 0.1-0.3, Moderate vegetation: 0.3-0.5, Dense vegetation: 0.5-0.8
        
        base_ndvi = (greenness_ratio / 100) * 0.6  # Scale to NDVI range
        
        # Add seasonal variation based on latitude
        if lat < 15:  # Southern India - tropical
            seasonal_factor = np.random.uniform(-0.05, 0.1)
        elif lat > 28:  # Northern India - more seasonal
            seasonal_factor = np.random.uniform(-0.15, 0.05)
        else:  # Central India
            seasonal_factor = np.random.uniform(-0.1, 0.05)
        
        ndvi = base_ndvi + seasonal_factor
        return max(0.05, min(0.85, ndvi))  # Clamp between realistic values
    
    def estimate_albedo(self, land_cover: str, ndvi: float) -> float:
        """
        Estimate surface albedo (reflectivity)
        Range: 0-1 (0 = absorbs all light, 1 = reflects all light)
        Urban areas typically have lower albedo (0.10-0.20)
        Green spaces have moderate albedo (0.20-0.30)
        """
        # Base albedo by land cover type
        albedo_map = {
            'Urban': np.random.uniform(0.12, 0.18),
            'Industrial': np.random.uniform(0.10, 0.15),
            'Green Space': np.random.uniform(0.20, 0.30),
            'Mixed Urban': np.random.uniform(0.15, 0.22),
            'Water': np.random.uniform(0.05, 0.10)
        }
        
        base_albedo = albedo_map.get(land_cover, 0.15)
        
        # Adjust based on NDVI (more vegetation = higher albedo)
        ndvi_adjustment = (ndvi - 0.3) * 0.1
        
        return max(0.05, min(0.40, base_albedo + ndvi_adjustment))
    
    def estimate_impervious_surface(self, population_density: float, land_cover: str) -> float:
        """
        Estimate percentage of impervious surfaces (concrete, asphalt, buildings)
        Critical factor for UHI effect
        """
        if land_cover == 'Urban':
            base_impervious = 70
        elif land_cover == 'Industrial':
            base_impervious = 75
        elif land_cover == 'Green Space':
            base_impervious = 30
        elif land_cover == 'Mixed Urban':
            base_impervious = 55
        else:
            base_impervious = 45
        
        # Adjust based on population density
        if population_density > 20000:
            density_factor = 15
        elif population_density > 10000:
            density_factor = 10
        elif population_density > 5000:
            density_factor = 5
        else:
            density_factor = 0
        
        impervious = base_impervious + density_factor + np.random.uniform(-5, 5)
        return max(20, min(90, impervious))
    
    def estimate_building_density(self, population_density: float, impervious_surface: float) -> float:
        """
        Estimate building density (buildings per km²)
        Contributes to urban canyon effect
        """
        # Higher population and impervious surfaces = more buildings
        base_density = (population_density / 1000) * 0.5
        impervious_factor = (impervious_surface / 100) * 2000
        
        building_density = base_density + impervious_factor + np.random.uniform(-200, 200)
        return max(100, min(8000, building_density))
    
    def estimate_solar_radiation(self, lat: float, cloud_cover: float) -> float:
        """
        Estimate daily solar radiation (MJ/m²/day)
        Major factor in UHI intensity
        """
        # Base solar radiation by latitude
        # Lower latitude (closer to equator) = higher radiation
        base_radiation = 20 - (abs(lat) / 10) * 2
        
        # Cloud cover reduces radiation
        if not np.isnan(cloud_cover):
            cloud_factor = (1 - (cloud_cover / 100)) * 5
        else:
            cloud_factor = 2
        
        radiation = base_radiation + cloud_factor + np.random.uniform(-2, 2)
        return max(10, min(30, radiation))
    
    def estimate_traffic_density(self, population: float, tier: int, population_density: float) -> float:
        """
        Estimate traffic density (vehicles per km² of road)
        Source of anthropogenic heat
        Based on population, city tier, and urbanization level
        """
        # Vehicle ownership rate varies by city tier and urbanization
        # Tier 1 cities have higher vehicle ownership
        if tier == 1:
            vehicle_ownership_rate = 0.25  # vehicles per person
        else:
            vehicle_ownership_rate = 0.15  # vehicles per person
        
        # Adjust for population density (more dense = more vehicles)
        if population_density > 20000:
            vehicle_ownership_rate *= 1.3
        elif population_density > 10000:
            vehicle_ownership_rate *= 1.1
        
        total_vehicles = population * vehicle_ownership_rate
        
        # Estimate road area (roughly 10-15% of urban area)
        urban_area = population / 5000  # rough estimate in km²
        road_area = urban_area * 0.12
        
        if road_area > 0:
            traffic_density = total_vehicles / road_area
        else:
            traffic_density = 1000
        
        return max(100, min(10000, traffic_density))
    
    def estimate_anthropogenic_heat(self, energy_consumption: float, population: float, 
                                    traffic_density: float) -> float:
        """
        Estimate anthropogenic heat flux (W/m²)
        Heat released from human activities
        """
        # Energy consumption component
        energy_heat = (energy_consumption / 1000000) * 10  # Convert to heat flux
        
        # Traffic component
        traffic_heat = (traffic_density / 1000) * 5
        
        # Population density component (body heat, small appliances)
        population_heat = (population / 1000000) * 8
        
        total_heat = energy_heat + traffic_heat + population_heat
        return max(5, min(200, total_heat))
    
    def estimate_urban_sprawl_rate(self, population: float, tier: int) -> float:
        """
        Estimate annual urban sprawl rate (%)
        Indicates how fast city is expanding
        """
        # Tier 1 cities (metros) grow faster
        if tier == 1:
            base_rate = np.random.uniform(3, 8)
        else:
            base_rate = np.random.uniform(2, 5)
        
        # Larger cities grow faster (more opportunities)
        if population > 5000000:
            size_factor = 2
        elif population > 2000000:
            size_factor = 1
        else:
            size_factor = 0
        
        sprawl_rate = base_rate + size_factor + np.random.uniform(-1, 1)
        return max(1, min(12, sprawl_rate))
    
    def calculate_uhi_intensity(self, temperature: float, ndvi: float, albedo: float,
                                impervious_surface: float, wind_speed: float) -> float:
        """
        Calculate estimated UHI intensity (°C difference from rural areas)
        Based on multiple factors
        """
        # Base UHI from temperature
        base_uhi = 2.0
        
        # Impervious surface factor (more impervious = stronger UHI)
        impervious_factor = (impervious_surface / 100) * 3
        
        # Vegetation factor (more vegetation = weaker UHI)
        vegetation_factor = -(ndvi * 5)
        
        # Albedo factor (lower albedo = stronger UHI)
        albedo_factor = -(albedo - 0.15) * 5
        
        # Wind speed factor (higher wind = weaker UHI)
        if not np.isnan(wind_speed):
            wind_factor = -(wind_speed / 10) * 1.5
        else:
            wind_factor = 0
        
        uhi_intensity = base_uhi + impervious_factor + vegetation_factor + albedo_factor + wind_factor
        
        return max(0.5, min(10, uhi_intensity))
    
    def estimate_cooling_degree_days(self, temp_max: float, temp_min: float) -> float:
        """
        Calculate cooling degree days (CDD)
        Indicates cooling energy demand
        """
        if not np.isnan(temp_max) and not np.isnan(temp_min):
            avg_temp = (temp_max + temp_min) / 2
            base_temp = 18  # Base temperature for cooling (°C)
            
            if avg_temp > base_temp:
                return avg_temp - base_temp
        return 0


def collect_enhanced_data(base_collector, enhanced_collector, city: Dict) -> Dict:
    """
    Collect both base and enhanced UHI data for a city
    """
    from collector import UHIDataCollector
    
    # Get base data
    base_data = base_collector.collect_city_data(city, delay=1.5)
    
    # Calculate enhanced features
    lat, lon = city['lat'], city['lon']
    city_name = city['name']
    tier = city['tier']
    
    # Extract base values
    greenness = base_data['Urban Greenness Ratio (%)']
    land_cover = base_data['Land Cover']
    population_density = base_data['Population Density (people/km²)']
    population = base_data['Population']
    energy = base_data['Energy Consumption (MWh/year)']
    wind_speed = base_data['Wind Speed (km/h)']
    temperature = base_data['Temperature (°C)']
    cloud_cover = base_data['Cloud Cover (%)']
    temp_max = base_data['Temperature Max (°C)']
    temp_min = base_data['Temperature Min (°C)']
    
    # Calculate enhanced metrics
    distance_to_water = enhanced_collector.calculate_distance_to_water(lat, lon, city_name)
    ndvi = enhanced_collector.estimate_ndvi(lat, lon, city_name, greenness)
    albedo = enhanced_collector.estimate_albedo(land_cover, ndvi)
    impervious_surface = enhanced_collector.estimate_impervious_surface(population_density, land_cover)
    building_density = enhanced_collector.estimate_building_density(population_density, impervious_surface)
    solar_radiation = enhanced_collector.estimate_solar_radiation(lat, cloud_cover)
    traffic_density = enhanced_collector.estimate_traffic_density(population, tier, population_density)
    anthropogenic_heat = enhanced_collector.estimate_anthropogenic_heat(energy, population, traffic_density)
    sprawl_rate = enhanced_collector.estimate_urban_sprawl_rate(population, tier)
    uhi_intensity = enhanced_collector.calculate_uhi_intensity(temperature, ndvi, albedo, 
                                                                impervious_surface, wind_speed)
    cooling_dd = enhanced_collector.estimate_cooling_degree_days(temp_max, temp_min)
    
    # Add enhanced features to base data
    enhanced_data = base_data.copy()
    enhanced_data.update({
        'NDVI': round(ndvi, 3),
        'Albedo': round(albedo, 3),
        'Impervious Surface (%)': round(impervious_surface, 1),
        'Building Density (buildings/km²)': round(building_density, 0),
        'Distance to Water (km)': round(distance_to_water, 1),
        'Solar Radiation (MJ/m²/day)': round(solar_radiation, 1),
        'Traffic Density (vehicles/km² road)': round(traffic_density, 0),
        'Anthropogenic Heat Flux (W/m²)': round(anthropogenic_heat, 1),
        'Urban Sprawl Rate (%/year)': round(sprawl_rate, 1),
        'UHI Intensity (°C)': round(uhi_intensity, 2),
        'Cooling Degree Days': round(cooling_dd, 1),
    })
    
    return enhanced_data


def main():
    """Main function to collect enhanced UHI data"""
    from indian_cities import get_all_cities
    from collector import UHIDataCollector
    
    base_collector = UHIDataCollector()
    enhanced_collector = EnhancedUHICollector()
    cities = get_all_cities()
    
    print("=" * 80)
    print("ENHANCED URBAN HEAT ISLAND DATA COLLECTION")
    print("50 Major Indian Cities")
    print("=" * 80)
    print(f"\nCollection started at: {datetime.now()}")
    print(f"Total cities to process: {len(cities)}")
    print("\nAdditional UHI Factors Included:")
    print("  • NDVI (Normalized Difference Vegetation Index)")
    print("  • Albedo (Surface Reflectivity)")
    print("  • Impervious Surface Percentage")
    print("  • Building Density")
    print("  • Distance to Water Bodies")
    print("  • Solar Radiation")
    print("  • Traffic Density")
    print("  • Anthropogenic Heat Flux")
    print("  • Urban Sprawl Rate")
    print("  • UHI Intensity Estimate")
    print("  • Cooling Degree Days")
    print("\n" + "=" * 80 + "\n")
    
    all_data = []
    successful = 0
    failed = 0
    
    for i, city in enumerate(cities, 1):
        try:
            print(f"[{i}/{len(cities)}] Processing {city['name']}, {city['state']}...")
            enhanced_data = collect_enhanced_data(base_collector, enhanced_collector, city)
            all_data.append(enhanced_data)
            successful += 1
            print(f"    ✓ Completed - UHI Intensity: {enhanced_data['UHI Intensity (°C)']}°C, "
                  f"NDVI: {enhanced_data['NDVI']}")
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            failed += 1
            continue
        
        time.sleep(0.5)  # Small delay between cities
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Reorder columns for better readability
    column_order = [
        'City Name', 'State', 'Latitude', 'Longitude', 'Elevation (m)',
        'Temperature (°C)', 'Temperature Max (°C)', 'Temperature Min (°C)',
        'UHI Intensity (°C)', 'Humidity (%)', 'Wind Speed (km/h)', 'Cloud Cover (%)',
        'Daily Precipitation (mm)', 'Annual Rainfall (mm)', 'Cooling Degree Days',
        'Land Cover', 'NDVI', 'Urban Greenness Ratio (%)', 'Albedo',
        'Impervious Surface (%)', 'Building Density (buildings/km²)',
        'Distance to Water (km)', 'Solar Radiation (MJ/m²/day)',
        'Population', 'Population Density (people/km²)',
        'Energy Consumption (MWh/year)', 'Traffic Density (vehicles/km² road)',
        'Anthropogenic Heat Flux (W/m²)', 'Urban Sprawl Rate (%/year)',
        'Air Quality Index (AQI)', 'Health Impact (Mortality Rate/100k)'
    ]
    
    # Reorder if all columns exist
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = '../../data/processed'
    os.makedirs(output_dir, exist_ok=True)
    filename = f'{output_dir}/uhi_dataset_{timestamp}.csv'
    df.to_csv(filename, index=False)
    
    # Print results
    print("\n" + "=" * 80)
    print("DATA COLLECTION COMPLETED!")
    print("=" * 80)
    print(f"Successful: {successful}/{len(cities)} cities")
    print(f"Failed: {failed}/{len(cities)} cities")
    print(f"Dataset saved as: {filename}")
    print(f"Collection ended at: {datetime.now()}")
    print("=" * 80)
    
    # Display summary statistics
    print("\n" + "=" * 80)
    print("DATASET SUMMARY STATISTICS")
    print("=" * 80)
    
    print("\n1. Urban Heat Island Metrics:")
    uhi_cols = ['Temperature (°C)', 'UHI Intensity (°C)', 'Anthropogenic Heat Flux (W/m²)',
                'Cooling Degree Days']
    existing_uhi_cols = [col for col in uhi_cols if col in df.columns]
    if existing_uhi_cols:
        print(df[existing_uhi_cols].describe())
    
    print("\n2. Urban Form Metrics:")
    urban_cols = ['Impervious Surface (%)', 'Building Density (buildings/km²)', 
                  'NDVI', 'Albedo', 'Urban Greenness Ratio (%)']
    existing_urban_cols = [col for col in urban_cols if col in df.columns]
    if existing_urban_cols:
        print(df[existing_urban_cols].describe())
    
    # Top 10 cities by UHI intensity
    if 'UHI Intensity (°C)' in df.columns:
        print("\n" + "=" * 80)
        print("TOP 10 CITIES BY UHI INTENSITY")
        print("=" * 80)
        top_uhi = df.nlargest(10, 'UHI Intensity (°C)')[['City Name', 'State', 'UHI Intensity (°C)', 
                                                          'Temperature (°C)', 'Impervious Surface (%)']]
        print(top_uhi.to_string(index=False))
    
    return df


if __name__ == "__main__":
    df = main()

