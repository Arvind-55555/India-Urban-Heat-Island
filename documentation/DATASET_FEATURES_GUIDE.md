# Urban Heat Island Dataset - Feature Guide

## Quick Reference for All 32 Features

### 🌍 Geographic Features (5)

| Feature | Unit | Description | Range | Source |
|---------|------|-------------|-------|--------|
| **City Name** | - | Name of the city | - | Database |
| **State** | - | Indian state | - | Database |
| **Latitude** | degrees | North (+) / South (-) | -90 to +90 | Database |
| **Longitude** | degrees | East (+) / West (-) | -180 to +180 | Database |
| **Elevation** | meters | Height above sea level | 0 to 5000+ | Open-Elevation API |

---

### 🌡️ Meteorological Features (9)

| Feature | Unit | Description | Impact on UHI | Source |
|---------|------|-------------|---------------|--------|
| **Temperature** | °C | Current air temperature | Direct indicator | Open-Meteo API |
| **Temperature Max** | °C | Daily maximum | Heat stress metric | Open-Meteo API |
| **Temperature Min** | °C | Daily minimum | Cooling relief | Open-Meteo API |
| **Humidity** | % | Relative humidity (0-100) | Higher = feels hotter | Open-Meteo API |
| **Wind Speed** | km/h | Current wind speed | Higher = cooling | Open-Meteo API |
| **Cloud Cover** | % | Sky coverage (0-100) | Reduces solar radiation | Open-Meteo API |
| **Daily Precipitation** | mm | Recent rainfall | Cooling effect | Open-Meteo API |
| **Annual Rainfall** | mm | Yearly average | Climate indicator | Estimated |
| **Cooling Degree Days** | days | Energy demand for cooling | Higher = more AC needed | Calculated |

---

### 🏙️ Urban Form Features (8)

| Feature | Unit | Description | Impact on UHI | Source |
|---------|------|-------------|---------------|--------|
| **Land Cover** | category | Primary land use type | Urban/Industrial = higher UHI | Classified |
| **NDVI** | 0-1 scale | Vegetation health index | Higher = cooler (r=-0.70) | Estimated |
| **Urban Greenness Ratio** | % | Percentage of green space | Higher = cooler (r=-0.66) | Estimated |
| **Albedo** | 0-1 scale | Surface reflectivity | Higher = cooler (r=-0.70) | Calculated |
| **Impervious Surface** | % | Concrete/asphalt coverage | **Strongest UHI driver (r=+0.74)** | Estimated |
| **Building Density** | buildings/km² | Structures per unit area | Higher = heat trapped (r=+0.70) | Calculated |
| **Distance to Water** | km | Proximity to river/coast | Closer = cooling benefit | Database |
| **Urban Sprawl Rate** | %/year | Annual expansion rate | Rapid growth = UHI risk | Estimated |

---

### 👥 Socioeconomic Features (5)

| Feature | Unit | Description | Relevance to UHI | Source |
|---------|------|-------------|------------------|--------|
| **Population** | people | Total city population | Scale of impact | Census 2011/2021 |
| **Population Density** | people/km² | Crowding metric | Higher = more heat (r=+0.27) | Calculated |
| **GDP per Capita** | USD | Economic prosperity | Affects energy use | State data |
| **Energy Consumption** | MWh/year | Annual energy use | Heat generation | Calculated |
| **Traffic Density** | vehicles/km² | Vehicle concentration | Anthropogenic heat | Estimated |

---

### 🌞 Heat & Radiation Features (3)

| Feature | Unit | Description | Impact on UHI | Source |
|---------|------|-------------|---------------|--------|
| **Solar Radiation** | MJ/m²/day | Incoming solar energy | Heat input | Calculated |
| **Anthropogenic Heat Flux** | W/m² | Human-generated heat | From traffic, industry, AC | Calculated |
| **UHI Intensity** | °C | Temp difference from rural | **PRIMARY OUTPUT** | Multi-factor model |

---

### 🏥 Environmental Health Features (2)

| Feature | Unit | Description | Health Significance | Source |
|---------|------|-------------|---------------------|--------|
| **Air Quality Index** | 0-500 | Pollution level | Higher = health risk | OpenAQ API* |
| **Health Impact** | deaths/100k | Mortality rate estimate | Heat + pollution effect | Calculated |

*Note: AQI data largely unavailable for Indian cities via API

---

## 🎯 Key Feature Relationships

### Strongest UHI Contributors (Positive Correlation)

1. **Impervious Surface** (r = +0.742) ⭐⭐⭐⭐⭐
   - Most important factor
   - Each 10% increase → ~0.3°C UHI increase
   - Target for intervention

2. **Building Density** (r = +0.704) ⭐⭐⭐⭐⭐
   - Creates urban canyon effect
   - Traps heat and blocks wind
   - Regulate in new developments

3. **Population Density** (r = +0.270) ⭐⭐
   - Moderate effect
   - Indirect through energy use
   - Consider in planning

### Strongest UHI Mitigators (Negative Correlation)

1. **NDVI / Vegetation** (r = -0.704) 🌳🌳🌳🌳🌳
   - Most effective natural cooling
   - Each 0.1 NDVI increase → ~0.3°C cooler
   - **Plant more trees!**

2. **Albedo** (r = -0.699) ☀️☀️☀️☀️☀️
   - High reflectivity = less heat absorption
   - Cool roofs and pavements work
   - Cost-effective intervention

3. **Urban Greenness** (r = -0.657) 🌿🌿🌿🌿🌿
   - Correlated with NDVI
   - Parks and gardens provide relief
   - Target: >30% greenness ratio

4. **Wind Speed** (r = -0.543) 💨💨💨💨
   - Natural ventilation
   - Design cities for wind flow
   - Avoid blocking corridors

---

## 📊 Data Quality Indicators

### High Confidence (Real-time/Validated)
✅ Geographic coordinates  
✅ Elevation  
✅ Current weather (temp, humidity, wind)  
✅ Population (census-based)  

### Medium Confidence (Statistical Estimates)
⚠️ Annual rainfall  
⚠️ GDP per capita  
⚠️ Energy consumption  
⚠️ Traffic density  

### Model-Based (Calculated)
🔄 NDVI (should validate with satellite)  
🔄 Albedo (surface-type based)  
🔄 Impervious surface (urbanization model)  
🔄 UHI intensity (multi-factor equation)  
🔄 Anthropogenic heat (energy-based model)  

### Low Coverage
❌ Air Quality Index (API limited for India)  

---

## 🔬 Feature Importance for Research

### Urban Planning Studies
**Primary**: Impervious Surface, Building Density, Land Cover  
**Secondary**: Population Density, Urban Sprawl Rate  
**Control Variables**: Latitude, Elevation, Distance to Water  

### Environmental Studies
**Primary**: NDVI, UHI Intensity, Temperature  
**Secondary**: Albedo, Solar Radiation, Wind Speed  
**Control Variables**: Cloud Cover, Rainfall  

### Public Health Research
**Primary**: UHI Intensity, AQI, Health Impact  
**Secondary**: Temperature Max, Cooling Degree Days  
**Control Variables**: Population Density, GDP  

### Climate Science
**Primary**: Temperature, UHI Intensity, NDVI  
**Secondary**: Solar Radiation, Albedo, Cloud Cover  
**Temporal**: Seasonal variations (requires time-series)  

---

## 💻 Using Features in Analysis

### Regression Analysis
```python
# Predict UHI Intensity
features = [
    'Impervious Surface (%)',
    'NDVI',
    'Building Density (buildings/km²)',
    'Wind Speed (km/h)',
    'Population Density (people/km²)'
]
target = 'UHI Intensity (°C)'
```

### Clustering Analysis
```python
# Group similar cities
features = [
    'UHI Intensity (°C)',
    'NDVI',
    'Impervious Surface (%)',
    'Population Density (people/km²)',
    'Urban Greenness Ratio (%)'
]
```

### Comparative Analysis
```python
# Compare regions
groupby_features = ['State', 'Land Cover', 'Region']
aggregate_features = [
    'UHI Intensity (°C)',
    'Temperature (°C)',
    'NDVI',
    'Impervious Surface (%)'
]
```

---

## 🎨 Visualization Recommendations

### Scatter Plots
- **X-axis**: NDVI, Impervious Surface %, Population Density  
- **Y-axis**: UHI Intensity  
- **Color**: Temperature or Albedo  
- **Size**: Population  

### Heatmaps
- Correlation matrix of all numeric features  
- Geographic heatmap (if plotting on map)  

### Bar Charts
- Top/Bottom cities by UHI Intensity  
- Regional comparisons  
- Land cover type analysis  

### Time Series (if collecting multiple times)
- Temperature trends  
- UHI intensity changes  
- NDVI seasonal variations  

---

## 🔄 Feature Engineering Suggestions

### Derived Features You Could Add

1. **Temperature Range** = Temp Max - Temp Min
   - Indicates thermal variability

2. **Heat Index** = f(Temperature, Humidity)
   - Perceived temperature

3. **Green-to-Impervious Ratio** = Greenness / Impervious
   - Balance metric

4. **Urbanization Index** = (Impervious + Building Density) / 2
   - Composite metric

5. **Cooling Potential** = (NDVI × Albedo) / Impervious
   - Mitigation capacity

---

## 📈 Benchmarking Values

### UHI Intensity Classification
- **Very Low**: < 1.0°C (Excellent)
- **Low**: 1.0-2.0°C (Good)
- **Moderate**: 2.0-3.0°C (Needs attention)
- **High**: 3.0-4.0°C (Urgent action needed)
- **Very High**: > 4.0°C (Critical)

### NDVI Classification
- **Very Low**: < 0.1 (Barren/Urban)
- **Low**: 0.1-0.2 (Sparse vegetation)
- **Moderate**: 0.2-0.3 (Moderate vegetation)
- **High**: 0.3-0.5 (Dense vegetation)
- **Very High**: > 0.5 (Forest)

### Impervious Surface Classification
- **Low**: < 40% (Rural/Garden city)
- **Moderate**: 40-60% (Suburban)
- **High**: 60-80% (Urban)
- **Very High**: > 80% (Dense urban/Industrial)

---

## 🎓 Further Reading

### Understanding the Features

**NDVI**: Remote Sensing of Environment journal  
**UHI**: EPA Urban Heat Island resources  
**Albedo**: Climate change and urban materials  
**Anthropogenic Heat**: Urban energy balance studies  

### Validation Sources

**Satellite Data**: Sentinel-2 (ESA), Landsat (USGS)  
**Ground Truth**: Local weather stations  
**Population**: Census of India  
**Land Use**: ISRO Bhuvan, NRSC products  

---

## ✅ Data Validation Checklist

Before using this dataset, verify:

- [ ] Temperature values are reasonable (10-45°C for India)
- [ ] NDVI is between 0-1
- [ ] Albedo is between 0-1
- [ ] Percentages are 0-100
- [ ] No negative populations or densities
- [ ] Coordinates are within India (8-37°N, 68-97°E)
- [ ] UHI intensity is positive and < 10°C

---

**Last Updated**: December 2, 2025  
**Dataset Version**: 1.0  
**Feature Count**: 32

*This guide should be read alongside the main README.md and PROJECT_SUMMARY.md*

