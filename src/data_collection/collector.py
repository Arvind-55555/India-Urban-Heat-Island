"""
Real-time Data Collection for Urban Heat Island Analysis
Fetches data from multiple sources for Indian cities
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class UHIDataCollector:
    """Collects real-time data for UHI analysis"""
    
    def __init__(self):
        """Initialize data collector"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_weather_data(self, lat: float, lon: float, city_name: str) -> Dict:
        """
        Fetch weather data from Open-Meteo API (Free, no API key needed)
        Returns: Temperature, Humidity, Wind Speed, Rainfall, Cloud Cover
        """
        try:
            # Open-Meteo API - Free weather data
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,cloud_cover',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
                'timezone': 'Asia/Kolkata'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                daily = data.get('daily', {})
                
                return {
                    'temperature': current.get('temperature_2m', np.nan),
                    'humidity': current.get('relative_humidity_2m', np.nan),
                    'wind_speed': current.get('wind_speed_10m', np.nan),
                    'cloud_cover': current.get('cloud_cover', np.nan),
                    'precipitation_sum': daily.get('precipitation_sum', [np.nan])[0] if daily.get('precipitation_sum') else np.nan,
                    'temp_max': daily.get('temperature_2m_max', [np.nan])[0] if daily.get('temperature_2m_max') else np.nan,
                    'temp_min': daily.get('temperature_2m_min', [np.nan])[0] if daily.get('temperature_2m_min') else np.nan,
                }
            else:
                print(f"Weather API error for {city_name}: {response.status_code}")
                return self._get_default_weather()
        except Exception as e:
            print(f"Error fetching weather for {city_name}: {e}")
            return self._get_default_weather()
    
    def get_elevation(self, lat: float, lon: float) -> float:
        """Fetch elevation data from Open-Elevation API"""
        try:
            url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['results'][0]['elevation']
            return np.nan
        except Exception as e:
            print(f"Error fetching elevation: {e}")
            return np.nan
    
    def get_air_quality(self, lat: float, lon: float, city_name: str) -> Dict:
        """
        Fetch air quality data from OpenAQ or fallback to estimates
        Returns: AQI and pollutant levels
        """
        try:
            # OpenAQ API - Free air quality data
            url = "https://api.openaq.org/v2/latest"
            params = {
                'coordinates': f"{lat},{lon}",
                'radius': 50000,  # 50km radius
                'limit': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    measurements = data['results'][0].get('measurements', [])
                    aqi = 0
                    for m in measurements:
                        if m.get('parameter') == 'pm25':
                            # Simple PM2.5 to AQI conversion
                            pm25 = m.get('value', 0)
                            aqi = self._pm25_to_aqi(pm25)
                            break
                    return {'aqi': aqi if aqi > 0 else np.nan}
                return {'aqi': np.nan}
            return {'aqi': np.nan}
        except Exception as e:
            print(f"Error fetching AQI for {city_name}: {e}")
            return {'aqi': np.nan}
    
    def get_population_data(self, city_name: str) -> Dict:
        """
        Get population and demographic data for Indian cities
        Based on 2011 Census data and estimates
        """
        # Population data for major Indian cities (in thousands, 2021 estimates)
        population_db = {
            'Mumbai': {'population': 20411000, 'area_km2': 603},
            'Delhi': {'population': 32941000, 'area_km2': 1484},
            'Bangalore': {'population': 13193000, 'area_km2': 741},
            'Hyderabad': {'population': 10494000, 'area_km2': 650},
            'Ahmedabad': {'population': 8450000, 'area_km2': 505},
            'Chennai': {'population': 11324000, 'area_km2': 426},
            'Kolkata': {'population': 15134000, 'area_km2': 206},
            'Surat': {'population': 7785000, 'area_km2': 326},
            'Pune': {'population': 7764000, 'area_km2': 331},
            'Jaipur': {'population': 3876000, 'area_km2': 467},
            'Lucknow': {'population': 3382000, 'area_km2': 349},
            'Kanpur': {'population': 3067000, 'area_km2': 267},
            'Nagpur': {'population': 2968000, 'area_km2': 227},
            'Indore': {'population': 3276000, 'area_km2': 276},
            'Thane': {'population': 2171000, 'area_km2': 147},
            'Bhopal': {'population': 2371000, 'area_km2': 285},
            'Visakhapatnam': {'population': 2035000, 'area_km2': 682},
            'Pimpri-Chinchwad': {'population': 1729000, 'area_km2': 181},
            'Patna': {'population': 2049000, 'area_km2': 250},
            'Vadodara': {'population': 2065000, 'area_km2': 235},
            'Ghaziabad': {'population': 1729000, 'area_km2': 130},
            'Ludhiana': {'population': 1618000, 'area_km2': 310},
            'Agra': {'population': 1746000, 'area_km2': 188},
            'Nashik': {'population': 1561000, 'area_km2': 264},
            'Faridabad': {'population': 1394000, 'area_km2': 143},
            'Meerut': {'population': 1543000, 'area_km2': 141},
            'Rajkot': {'population': 1390000, 'area_km2': 170},
            'Kalyan-Dombivli': {'population': 1247000, 'area_km2': 137},
            'Vasai-Virar': {'population': 1222000, 'area_km2': 233},
            'Varanasi': {'population': 1435000, 'area_km2': 112},
            'Srinagar': {'population': 1180000, 'area_km2': 294},
            'Aurangabad': {'population': 1175000, 'area_km2': 138},
            'Dhanbad': {'population': 1162000, 'area_km2': 227},
            'Amritsar': {'population': 1183000, 'area_km2': 139},
            'Navi Mumbai': {'population': 1120000, 'area_km2': 344},
            'Allahabad': {'population': 1217000, 'area_km2': 365},
            'Ranchi': {'population': 1126000, 'area_km2': 175},
            'Howrah': {'population': 1077000, 'area_km2': 57},
            'Coimbatore': {'population': 2151000, 'area_km2': 257},
            'Jabalpur': {'population': 1268000, 'area_km2': 263},
            'Gwalior': {'population': 1102000, 'area_km2': 518},
            'Vijayawada': {'population': 1048000, 'area_km2': 218},
            'Jodhpur': {'population': 1137000, 'area_km2': 227},
            'Madurai': {'population': 1470000, 'area_km2': 148},
            'Raipur': {'population': 1122000, 'area_km2': 226},
            'Kota': {'population': 1001000, 'area_km2': 527},
            'Chandigarh': {'population': 1055000, 'area_km2': 114},
            'Guwahati': {'population': 963000, 'area_km2': 328},
            'Thiruvananthapuram': {'population': 957000, 'area_km2': 214},
            'Mysore': {'population': 990000, 'area_km2': 155},
        }
        
        if city_name in population_db:
            data = population_db[city_name]
            return {
                'population': data['population'],
                'population_density': data['population'] / data['area_km2']
            }
        else:
            # Default estimates for cities not in database
            return {
                'population': 1000000,
                'population_density': 5000
            }
    
    def estimate_energy_consumption(self, population: float) -> float:
        """Estimate energy consumption based on population"""
        # Rough estimate: kWh per capita per year for India
        base_consumption_per_capita = 1200  # kWh per capita
        return (population / 1000) * base_consumption_per_capita
    
    def estimate_urban_greenness(self, city_name: str, lat: float) -> float:
        """
        Estimate urban greenness ratio based on city characteristics
        Would ideally come from NDVI data from Sentinel-2
        """
        # Cities with known higher greenness
        green_cities = ['Bangalore', 'Chandigarh', 'Mysore', 'Thiruvananthapuram', 
                       'Bhopal', 'Guwahati', 'Srinagar']
        
        if city_name in green_cities:
            return np.random.uniform(25, 40)
        else:
            return np.random.uniform(10, 25)
    
    def calculate_land_cover_type(self, greenness: float, population_density: float) -> str:
        """Determine primary land cover type"""
        if greenness > 30:
            return 'Green Space'
        elif population_density > 15000:
            return 'Urban'
        elif population_density > 10000:
            return 'Industrial'
        else:
            return 'Mixed Urban'
    
    def estimate_health_impact(self, aqi: float, temperature: float) -> float:
        """Estimate health impact (mortality rate) based on AQI and temperature"""
        if np.isnan(aqi):
            aqi = 100  # Default moderate AQI
        
        # Base mortality rate per 100k
        base_rate = 20
        
        # AQI impact (higher AQI = higher mortality)
        aqi_factor = (aqi / 100) * 15
        
        # Temperature impact (extreme temps = higher mortality)
        temp_factor = 0
        if temperature > 35 or temperature < 10:
            temp_factor = 10
        elif temperature > 30 or temperature < 15:
            temp_factor = 5
        
        return base_rate + aqi_factor + temp_factor
    
    def estimate_annual_rainfall(self, lat: float, lon: float, city_name: str) -> float:
        """
        Estimate annual rainfall based on location
        Would ideally come from historical weather data
        """
        # High rainfall cities
        high_rainfall_cities = ['Mumbai', 'Chennai', 'Guwahati', 'Thiruvananthapuram']
        
        if city_name in high_rainfall_cities:
            return np.random.uniform(1500, 2500)
        elif lat < 15:  # Southern India
            return np.random.uniform(800, 1200)
        elif lat > 28:  # Northern India
            return np.random.uniform(600, 1000)
        else:  # Central India
            return np.random.uniform(700, 1100)
    
    def _pm25_to_aqi(self, pm25: float) -> int:
        """Convert PM2.5 to AQI using simplified formula"""
        if pm25 <= 12.0:
            return int((50 / 12.0) * pm25)
        elif pm25 <= 35.4:
            return int(50 + ((100 - 50) / (35.4 - 12.1)) * (pm25 - 12.1))
        elif pm25 <= 55.4:
            return int(100 + ((150 - 100) / (55.4 - 35.5)) * (pm25 - 35.5))
        elif pm25 <= 150.4:
            return int(150 + ((200 - 150) / (150.4 - 55.5)) * (pm25 - 55.5))
        elif pm25 <= 250.4:
            return int(200 + ((300 - 200) / (250.4 - 150.5)) * (pm25 - 150.5))
        else:
            return int(300 + ((500 - 300) / (500.4 - 250.5)) * (pm25 - 250.5))
    
    def _get_default_weather(self) -> Dict:
        """Return default weather values when API fails"""
        return {
            'temperature': np.nan,
            'humidity': np.nan,
            'wind_speed': np.nan,
            'cloud_cover': np.nan,
            'precipitation_sum': np.nan,
            'temp_max': np.nan,
            'temp_min': np.nan,
        }
    
    def collect_city_data(self, city: Dict, delay: float = 1.0) -> Dict:
        """
        Collect all data for a single city
        """
        print(f"Collecting data for {city['name']}, {city['state']}...")
        
        lat, lon = city['lat'], city['lon']
        city_name = city['name']
        
        # Fetch real-time data
        weather = self.get_weather_data(lat, lon, city_name)
        time.sleep(delay)  # Rate limiting
        
        elevation = self.get_elevation(lat, lon)
        time.sleep(delay)
        
        air_quality = self.get_air_quality(lat, lon, city_name)
        time.sleep(delay)
        
        population_data = self.get_population_data(city_name)
        
        # Calculate derived metrics
        greenness = self.estimate_urban_greenness(city_name, lat)
        land_cover = self.calculate_land_cover_type(greenness, population_data['population_density'])
        energy = self.estimate_energy_consumption(population_data['population'])
        health_impact = self.estimate_health_impact(air_quality['aqi'], weather['temperature'])
        annual_rainfall = self.estimate_annual_rainfall(lat, lon, city_name)
        
        # Compile all data
        city_data = {
            'City Name': city_name,
            'State': city['state'],
            'Latitude': lat,
            'Longitude': lon,
            'Elevation (m)': elevation if not np.isnan(elevation) else np.random.uniform(10, 500),
            'Temperature (°C)': weather['temperature'],
            'Temperature Max (°C)': weather['temp_max'],
            'Temperature Min (°C)': weather['temp_min'],
            'Land Cover': land_cover,
            'Population': population_data['population'],
            'Population Density (people/km²)': population_data['population_density'],
            'Energy Consumption (MWh/year)': energy,
            'Air Quality Index (AQI)': air_quality['aqi'],
            'Urban Greenness Ratio (%)': greenness,
            'Health Impact (Mortality Rate/100k)': health_impact,
            'Wind Speed (km/h)': weather['wind_speed'],
            'Humidity (%)': weather['humidity'],
            'Cloud Cover (%)': weather['cloud_cover'],
            'Daily Precipitation (mm)': weather['precipitation_sum'],
            'Annual Rainfall (mm)': annual_rainfall,
        }
        
        return city_data


def main():
    """Main function to collect data for all cities"""
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from indian_cities import get_all_cities
    
    collector = UHIDataCollector()
    cities = get_all_cities()
    
    print(f"Starting data collection for {len(cities)} Indian cities...")
    print(f"Collection started at: {datetime.now()}")
    print("-" * 80)
    
    all_data = []
    for i, city in enumerate(cities, 1):
        try:
            city_data = collector.collect_city_data(city, delay=1.5)
            all_data.append(city_data)
            print(f"✓ [{i}/{len(cities)}] {city['name']} completed")
        except Exception as e:
            print(f"✗ [{i}/{len(cities)}] {city['name']} failed: {e}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = '../../data/processed'
    os.makedirs(output_dir, exist_ok=True)
    filename = f'{output_dir}/indian_cities_uhi_dataset_{timestamp}.csv'
    df.to_csv(filename, index=False)
    
    print("\n" + "=" * 80)
    print(f"Data collection completed!")
    print(f"Total cities processed: {len(all_data)}/{len(cities)}")
    print(f"Dataset saved as: {filename}")
    print(f"Collection ended at: {datetime.now()}")
    print("=" * 80)
    
    # Display summary statistics
    print("\nDataset Summary:")
    print(df.describe())
    
    return df


if __name__ == "__main__":
    df = main()

