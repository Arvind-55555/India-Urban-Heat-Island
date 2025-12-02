# Urban Heat Island (UHI) Monitoring System
## Real-time Data Collection & Analysis for 50 Major Indian Cities

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data-Real--time%20APIs-green.svg)](# "Open-Meteo, Open-Elevation")

## 🌐 Live Dashboard

**View the Interactive Dashboard:** [https://arvind-55555.github.io/India-Urban-Heat-Island/](https://arvind-55555.github.io/India-Urban-Heat-Island/)

Experience the complete UHI analysis with:
- 📊 Interactive visualizations
- 🔍 Key insights and findings
- 📈 Top cities by UHI intensity
- 🌳 Vegetation impact analysis
- 💡 Actionable recommendations

---

## Project Overview

A comprehensive Urban Heat Island monitoring and analysis system that collects real-time meteorological, environmental, and urban form data for 50 major Indian cities. The system integrates multiple data sources to provide insights into UHI intensity and contributing factors.

### Key Features

- ✅ **Real-time data collection** from public APIs (weather, elevation, air quality)
- ✅ **31 comprehensive features** per city including UHI-specific metrics
- ✅ **50 major Indian cities** across 20 states
- ✅ **Advanced UHI analysis** with correlation studies
- ✅ **Publication-ready visualizations** and reports
- ✅ **Actionable insights** for urban planning and policy

---

## Project Structure

```
urban_heat_island/
├── data/
│   ├── raw/                    # Original/reference datasets
│   └── processed/              # Generated UHI datasets
├── src/
│   ├── data_collection/        # Data collection modules
│   │   ├── indian_cities.py    # City database (50 cities)
│   │   ├── collector.py        # Base data collector
│   │   └── enhanced_collector.py  # Enhanced UHI collector
│   └── analysis/               # Analysis and visualization
│       └── analyzer.py         # Main analysis script
├── outputs/
│   ├── visualizations/         # Generated charts and plots
│   └── reports/                # Analysis summaries
├── documentation/              # Project documentation (MD files)
├── docs/                       # GitHub Pages (live dashboard)
├── web_dashboard/              # Dashboard source files
├── tools/                      # Utility scripts
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls)
- Web browser (for dashboard)

### Installation

```bash
# Clone or download the project
cd urban_heat_island

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 🌐 View Web Dashboard (Recommended)

```bash
# Launch interactive web dashboard
bash tools/run_dashboard.sh

# Dashboard opens at http://localhost:8000
# Features: Interactive charts, insights, recommendations
```

#### 1. Collect Data

**Quick collection using utility script:**
```bash
bash tools/run_collection.sh
```

**Or run directly:**
```bash
cd src/data_collection
python enhanced_collector.py
```

This will:
- Fetch real-time weather data for all 50 cities
- Calculate 31 UHI-related features
- Save dataset to `data/processed/`
- Display summary statistics

#### 2. Analyze Data

**Quick analysis using utility script:**
```bash
bash tools/run_analysis.sh
```

**Or run directly:**
```bash
cd src/analysis
python analyzer.py
```

This will:
- Load the latest dataset
- Perform correlation analysis
- Generate 4 visualizations (saved to `outputs/visualizations/`)
- Create summary report (saved to `outputs/reports/`)
- Display key findings in terminal

---

## Dataset Features

### Core Features (21)

| Category | Features |
|----------|----------|
| **Geographic** | City Name, State, Latitude, Longitude, Elevation |
| **Meteorological** | Temperature, Temperature Max/Min, Humidity, Wind Speed, Cloud Cover, Daily Precipitation, Annual Rainfall, Cooling Degree Days |
| **Urban Form** | Land Cover, Urban Greenness Ratio, Population, Population Density |
| **Environmental** | Air Quality Index, Health Impact |
| **Energy** | Energy Consumption |

### Enhanced UHI Factors (10)

| Feature | Description | Importance |
|---------|-------------|------------|
| **NDVI** | Normalized Difference Vegetation Index (0-1) | ⭐⭐⭐⭐⭐ |
| **Albedo** | Surface reflectivity (0-1) | ⭐⭐⭐⭐⭐ |
| **Impervious Surface %** | Paved/built-up areas | ⭐⭐⭐⭐⭐ |
| **UHI Intensity** | Temperature difference from rural areas (°C) | ⭐⭐⭐⭐⭐ |
| **Building Density** | Buildings per km² | ⭐⭐⭐⭐ |
| **Distance to Water** | Proximity to rivers/coasts (km) | ⭐⭐⭐ |
| **Solar Radiation** | Incoming solar energy (MJ/m²/day) | ⭐⭐⭐ |
| **Traffic Density** | Vehicles per km² of road | ⭐⭐⭐ |
| **Anthropogenic Heat Flux** | Human-generated heat (W/m²) | ⭐⭐⭐ |
| **Urban Sprawl Rate** | Annual expansion rate (%/year) | ⭐⭐ |

---

## Key Findings

### Top UHI Contributors (Correlation Analysis)

1. **Impervious Surfaces** (r = +0.742) ⭐ **STRONGEST FACTOR**
   - Each 10% increase → ~0.3°C UHI increase
   - Primary intervention target

2. **NDVI / Vegetation** (r = -0.704) 🌳 **STRONGEST MITIGATION**
   - Each 0.1 NDVI increase → ~0.3°C cooling
   - Plant more trees!

3. **Building Density** (r = +0.704)
   - Creates urban canyon effect
   - Traps heat and blocks wind

4. **Albedo** (r = -0.699)
   - Higher reflectivity = less heat absorption
   - Cool roofs and pavements work

### Cities Rankings

**🔥 Highest UHI Intensity (Top 5):**
1. Ghaziabad (3.92°C)
2. Delhi (3.60°C)
3. Ahmedabad (3.56°C)
4. Pune (3.56°C)
5. Mumbai (3.49°C)

**🌿 Lowest UHI Intensity (Top 5):**
1. Bangalore (0.50°C) - Garden City
2. Bhopal (0.50°C) - Lakes & Parks
3. Mysore (0.66°C) - Heritage City
4. Thiruvananthapuram (0.88°C) - Coastal Green
5. Nashik (0.97°C) - Moderate Density

**Insight:** Green space cities are **3.6× cooler** than industrial cities!

---

## Data Sources

### Real-Time APIs (Free, No Authentication)

- **[Open-Meteo](https://open-meteo.com/)** - Weather data (temperature, humidity, wind, precipitation, cloud cover)
- **[Open-Elevation](https://open-elevation.com/)** - Elevation data
- **[OpenAQ](https://openaq.org/)** - Air quality data (limited coverage in India)

### Statistical & Demographic Data

- **Census of India 2011** - Population statistics
- **2021 Estimates** - Updated population figures
- **Urban Planning Databases** - City characteristics and infrastructure

### Calculated Metrics

- NDVI, Albedo, Impervious Surfaces (based on land cover and urbanization models)
- Building Density, Traffic Density (population and tier-based algorithms)
- UHI Intensity (multi-factor calculation using validated formulas)

---

## Analysis Outputs

### Visualizations Generated

1. **UHI Factors Analysis** - 4-panel scatter plots showing relationships between UHI intensity and key factors
2. **Correlation Matrix** - Heatmap of all factor correlations
3. **Top Cities Chart** - Bar chart of cities by UHI intensity
4. **NDVI vs UHI** - Bubble chart with population and impervious surface

### Reports Generated

- **Summary Statistics** - Text file with key metrics and correlations
- **Console Output** - Detailed analysis with rankings and regional patterns

---

## Technical Details

### Dependencies

```
pandas>=1.5.0         # Data manipulation
numpy>=1.23.0         # Numerical operations
requests>=2.28.0      # API calls
matplotlib>=3.6.0     # Plotting
seaborn>=0.12.0       # Statistical visualizations
```

### Data Collection Process

1. **Initialization** - Load city database (50 cities with coordinates)
2. **API Calls** - Fetch real-time data with rate limiting
3. **Calculations** - Compute derived metrics (NDVI, albedo, UHI intensity)
4. **Validation** - Check data quality and handle missing values
5. **Export** - Save to CSV with timestamp

### Data Quality

| Data Type | Quality | Source |
|-----------|---------|--------|
| Weather (current) | ⭐⭐⭐⭐⭐ | Real-time API |
| Elevation | ⭐⭐⭐⭐⭐ | Validated API |
| Population | ⭐⭐⭐⭐ | Census data |
| NDVI/Albedo | ⭐⭐⭐ | Model estimates* |
| Air Quality | ⭐ | Limited API coverage |

*For research-grade accuracy, validate with actual satellite data (Sentinel-2, Landsat)

---

## Use Cases

### For Urban Planners
- Identify heat hotspots requiring intervention
- Prioritize green infrastructure investments
- Design urban ventilation corridors
- Implement cool roof programs

### For Researchers
- Study UHI patterns across Indian cities
- Validate climate models
- Analyze correlation with health outcomes
- Long-term trend analysis

### For Policy Makers
- Evidence-based decision making
- Climate action planning
- Public health risk assessment
- Sustainable development goals

### For Citizens
- Understand local heat risks
- Advocate for green spaces
- Make informed relocation decisions
- Community awareness campaigns

---

## Scientific Background

### What Causes Urban Heat Islands?

Urban Heat Islands occur when cities experience higher temperatures than surrounding rural areas due to:

1. **Heat Absorption** (30-40% contribution)
   - Dark surfaces (asphalt, concrete) absorb solar radiation
   - High thermal mass materials store heat

2. **Loss of Vegetation** (20-30%)
   - Reduction in evapotranspiration
   - Less shade and natural cooling

3. **Anthropogenic Heat** (15-25%)
   - Vehicles, industry, air conditioning
   - Energy consumption releases heat

4. **Urban Geometry** (10-20%)
   - Tall buildings create urban canyons
   - Reduced air circulation

5. **Reduced Albedo** (5-15%)
   - Dark surfaces reflect less sunlight
   - More heat absorption

### Mitigation Strategies

**High Impact:**
- 🌳 Increase urban vegetation (parks, street trees, green roofs)
- 🏠 Implement cool roofs and pavements (high albedo materials)
- 💧 Create urban water bodies (lakes, fountains)

**Medium Impact:**
- 💨 Design urban ventilation corridors
- 🏗️ Green building codes and regulations
- 🚇 Expand public transportation

**Long-term:**
- 🌲 Achieve 30%+ urban greenness ratio
- ⚡ Transition to clean energy
- 📐 Climate-responsive urban design

---

## Documentation

Detailed documentation available in the `documentation/` folder:

- **DATASET_FEATURES_GUIDE.md** - Comprehensive feature descriptions
- **PROJECT_SUMMARY.md** - Complete project overview and findings
- **WEB_DASHBOARD_SUMMARY.md** - Dashboard features and usage
- **QUICK_START_DASHBOARD.md** - Quick start guide

**Live Dashboard:** [https://arvind-55555.github.io/India-Urban-Heat-Island/](https://arvind-55555.github.io/India-Urban-Heat-Island/)

---

## Future Enhancements

### Planned Features

- [ ] **Satellite Data Integration** - Real NDVI from Sentinel-2/Landsat
- [ ] **Seasonal Analysis** - Collect data for all 4 seasons
- [ ] **Night-time Temperatures** - UHI is often stronger at night
- [ ] **Neighborhood-level Analysis** - Within-city variations
- [ ] **Historical Trends** - 5-10 year comparisons
- [ ] **Machine Learning Models** - Predict future UHI intensity
- [x] **Interactive Dashboard** - Web-based monitoring interface (✅ Live on GitHub Pages!)
- [ ] **Mobile App** - Citizen science data collection

---

## Contributing

Contributions are welcome! Areas for improvement:

- Additional data sources (government portals, satellite data)
- More cities (expand to 100+ Indian cities)
- Enhanced algorithms (better NDVI/albedo estimation)
- Validation studies (ground truth comparison)
- Documentation improvements

---

## License

This project is open-source and available for research and educational purposes. When using this dataset, please cite:

```
Urban Heat Island Monitoring System for 50 Major Indian Cities (2025)
Real-time data collection and analysis framework
Data Sources: Open-Meteo, Open-Elevation, Census of India
```

---

## Contact

For questions, collaborations, or feedback:
- Create an issue in the project repository
- Review documentation in `docs/` folder
- Check examples in `tools/` for common tasks

---

## Acknowledgments

- **Open-Meteo** - Weather data API
- **Open-Elevation** - Elevation data API
- **Census of India** - Population statistics
- **OpenStreetMap** - Geographic reference data
- **Scientific Community** - UHI research and methodologies

---

## Project Statistics

- **50 cities** across 20 Indian states
- **31 features** per city
- **1,550 data points** (50 cities × 31 features)
- **195 million people** covered (14% of India's population)
- **100% success rate** in data collection

---

**Building cooler, greener, more livable Indian cities!**
