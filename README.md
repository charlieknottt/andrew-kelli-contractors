# PropertyScope - Drone Photo Analysis MVP

A real estate broker application that analyzes drone photos to predict renovation and maintenance costs using AI-powered image analysis.

## Features

- **Photo Upload**: Upload multiple drone photos with drag & drop interface
- **AI Analysis**: Computer vision-based property condition assessment
- **Cost Estimation**: Intelligent cost prediction for identified issues
- **Professional Reports**: Generate detailed PDF reports
- **Investment Analysis**: ROI calculations and payback period estimates
- **Modern UI**: Responsive, professional interface

## Analysis Categories

- **Roof Condition**: Shingles, damage, gutters, overall condition
- **Exterior Siding**: Paint, material condition, structural issues
- **Landscaping**: Lawn, vegetation, garden maintenance needs
- **Hardscaping**: Driveways, walkways, patios, outdoor structures

## Installation

1. **Clone or download the project**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Upload Photos**: Navigate to "Analyze Property" and upload drone photos
2. **Enter Property Address**: Provide property address for report identification
3. **Wait for Analysis**: The AI processes images (typically 2-3 minutes)
4. **Review Results**: View detailed analysis with cost breakdowns
5. **Download Report**: Generate and download professional PDF report

## Technical Stack

- **Backend**: Python Flask
- **Image Processing**: OpenCV, PIL
- **Report Generation**: ReportLab
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI Analysis**: Computer vision algorithms

## File Structure

```
real-estate-appraisal/
├── app.py                 # Main Flask application
├── property_analyzer.py   # AI analysis engine
├── report_generator.py    # PDF report generation
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── results.html
├── static/              # CSS, JS, images
│   ├── css/style.css
│   └── js/main.js
├── uploads/             # Temporary photo storage
└── reports/             # Generated PDF reports
```

## API Endpoints

- `GET /` - Home page
- `GET /upload` - Photo upload page
- `POST /upload` - Process uploaded photos
- `GET /generate_report/<session_id>` - Download PDF report
- `POST /api/analyze` - REST API for photo analysis

## Cost Estimation Ranges

| Category | Min Cost | Max Cost | Typical |
|----------|----------|----------|---------|
| Roof | $5,000 | $25,000 | $12,000 |
| Siding | $8,000 | $15,000 | $11,000 |
| Landscaping | $2,000 | $10,000 | $5,000 |
| Hardscaping | $3,000 | $8,000 | $5,500 |

## Sample Analysis Output

The system identifies issues like:
- Missing or damaged roof shingles
- Exterior paint weathering
- Landscaping maintenance needs
- Driveway/walkway repairs
- Gutter system issues
- Window and trim condition

## Investment Metrics

- **ROI Calculation**: Based on improvement costs vs. property value increase
- **Payback Period**: Time to recover investment through appreciation/rental income
- **Condition Score**: 1-10 rating of overall property condition
- **Timeline Estimates**: Project completion timeframes

## Limitations

- Analysis is based on visual assessment only
- Costs are estimates based on national averages
- Professional inspections recommended for major issues
- Regional cost variations not fully accounted for
- Weather and seasonal factors may affect accuracy

## Future Enhancements

- Integration with real estate MLS data
- Machine learning model training on actual repair costs
- Integration with contractor networks
- Mobile app development
- Advanced damage detection algorithms
- Historical property analysis

## Support

This is an MVP demonstration. For production use, consider:
- Professional image analysis models
- Regional cost databases
- Contractor marketplace integration
- Advanced reporting features
- Multi-user authentication system

## License

This project is for demonstration purposes. Commercial use requires appropriate licensing for all dependencies and AI models.