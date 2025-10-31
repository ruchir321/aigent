# Aircraft Specifications Analysis with Google Gemini API

This project demonstrates the implementation of tool calling and structured output generation using the Google Gemini API. The system successfully identifies aircraft types and extracts their specifications from online sources, storing the data in a structured CSV format for better analysis and presentation.

## Project Overview

The system utilizes:
- Google Gemini API for natural language processing and information extraction
- Tool calling capabilities for structured data handling
- CSV output for organized data storage

## Aircraft Specifications Database

Below is the collected data showing specifications for various military aircraft:

| Aircraft Name | Crew | Length (m) | Wingspan (m) | Height (m) | Max Speed (km/h) | Range (km) | Service Ceiling (m) | G-Limit | Thrust/Weight |
|--------------|------|------------|--------------|------------|-----------------|------------|-------------------|---------|--------------|
| F-15 Eagle | 1 | 19.43 | 13.05 | 5.63 | 2,655 | 5,550 | 19,812 | 9.0 | 1.55 |
| Su-57 Felon | 1 | 20.1 | 14.1 | 4.6 | 2,135 | 4,500 | 20,000 | 9.0 | 0.87 |
| MiG-29K | 1 | 17.3 | 11.99 | 4.4 | 2,200 | 3,000 | 17,500 | 8.0 | 0.97 |
| Su-30MKI | 2 | 21.94 | 14.7 | 6.36 | 2,120 | 8,000 | 17,300 | 9.0 | 0.96 |
| F-14 Tomcat | 2 | 19.1 | 19.55 | 4.88 | 2,485 | 2,960 | 15,200 | 6.5 | 0.73 |
| MiG-21 | 1 | 14.5 | 7.15 | 4.13 | 2,175 | 1,670 | 19,000 | 8.5 | 0.79 |
| HAL Tejas | 1 | 13.2 | 8.2 | 4.4 | 1,975 | 3,200 | 16,500 | 9.0 | 1.07 |
| Rafale | 2 | 15.3 | 10.9 | 5.3 | 2,470 | 3,700 | 15,240 | 9.0 | 1.13 |

## Implementation Details

The project uses:
- Gemini API for natural language understanding and generation
- Custom tools for data extraction and processing
- Structured output formatting for consistent data representation
- CSV file storage for easy data management and analysis

## Features
- Automated aircraft identification
- Specification extraction from reliable sources
- Structured data output in CSV format
- Clean data presentation in markdown tables
