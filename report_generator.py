from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#007bff'),
            alignment=1  # Center alignment
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#007bff'),
            borderWidth=1,
            borderColor=colors.HexColor('#007bff'),
            borderPadding=5
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#333333')
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#555555')
        )
        
        # Issue text style
        self.issue_style = ParagraphStyle(
            'IssueStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            leftIndent=20,
            textColor=colors.HexColor('#444444')
        )
    
    def generate_report(self, analysis_results, session_id):
        """Generate a comprehensive PDF report"""
        report_filename = f'reports/property_analysis_{session_id}.pdf'
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            report_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the story (content)
        story = []
        
        # Title Page
        story.extend(self._create_title_page(analysis_results))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Detailed Analysis
        story.extend(self._create_detailed_analysis(analysis_results))
        story.append(PageBreak())
        
        # Cost Breakdown
        story.extend(self._create_cost_breakdown(analysis_results))
        story.append(PageBreak())
        
        # Investment Analysis
        story.extend(self._create_investment_analysis(analysis_results))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(analysis_results))
        
        # Build the PDF
        doc.build(story)
        
        return report_filename
    
    def _create_title_page(self, results):
        """Create the title page"""
        story = []
        
        # Main title
        story.append(Paragraph("Andrew and Kelli Contractors", self.title_style))
        story.append(Paragraph("Drone Photo Analysis Report", self.title_style))
        story.append(Spacer(1, 50))
        
        # Property information
        property_address = results.get('property_address', 'Property Analysis')
        story.append(Paragraph(f"<b>Property:</b> {property_address}", self.header_style))
        story.append(Spacer(1, 20))
        
        # Report details
        report_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"<b>Report Date:</b> {report_date}", self.body_style))
        story.append(Paragraph(f"<b>Images Analyzed:</b> {results['images_analyzed']}", self.body_style))
        story.append(Paragraph(f"<b>Session ID:</b> {results['session_id']}", self.body_style))
        story.append(Spacer(1, 30))
        
        # Key metrics summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Estimated Cost', f"${results['total_estimated_cost']:,.0f}"],
            ['Issues Identified', f"{len(results['issues_found'])}"],
            ['Property Condition Score', f"{results['overall_condition_score']}/10"],
            ['Estimated Timeline', f"{results['estimated_timeline_weeks']} weeks"],
            ['Potential Value Increase', f"${results['potential_value_increase']:,.0f}"],
            ['Estimated ROI', f"{results['roi_percentage']}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 50))
        
        # Disclaimer
        disclaimer = """
        <b>DISCLAIMER:</b> This report is generated using AI-powered image analysis and provides estimates 
        based on visual assessment of drone photographs. Actual costs may vary significantly based on local 
        market conditions, material choices, and detailed on-site inspections. This report is intended for 
        initial assessment purposes only and should be supplemented with professional inspections and contractor 
        quotes for accurate cost estimates.
        """
        story.append(Paragraph(disclaimer, self.body_style))
        
        return story
    
    def _create_executive_summary(self, results):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.header_style))
        story.append(Spacer(1, 12))
        
        # Overall assessment
        condition_assessment = self._get_condition_assessment(results['overall_condition_score'])
        summary_text = f"""
        <b>Property Condition:</b> {condition_assessment}<br/><br/>
        
        Our AI-powered analysis of {results['images_analyzed']} drone photographs has identified 
        {len(results['issues_found'])} potential areas requiring attention. The estimated total 
        cost for addressing all identified issues is <b>${results['total_estimated_cost']:,.0f}</b>.
        <br/><br/>
        
        The analysis indicates a potential property value increase of 
        <b>${results['potential_value_increase']:,.0f}</b> upon completion of recommended improvements, 
        representing an estimated ROI of <b>{results['roi_percentage']}%</b>.
        <br/><br/>
        
        <b>Timeline:</b> The estimated completion timeline for all improvements is 
        {results['estimated_timeline_weeks']} weeks, depending on contractor availability and weather conditions.
        """
        
        story.append(Paragraph(summary_text, self.body_style))
        story.append(Spacer(1, 20))
        
        # Priority issues
        high_priority_issues = [issue for issue in results['issues_found'] if issue['severity'] == 'high']
        if high_priority_issues:
            story.append(Paragraph("High Priority Issues", self.subheader_style))
            for issue in high_priority_issues:
                issue_text = f"• {issue['description']} (Est. Cost: ${issue['estimated_cost']:,.0f})"
                story.append(Paragraph(issue_text, self.issue_style))
            story.append(Spacer(1, 12))
        
        return story
    
    def _create_detailed_analysis(self, results):
        """Create detailed analysis section"""
        story = []
        
        story.append(Paragraph("Detailed Analysis", self.header_style))
        story.append(Spacer(1, 12))
        
        # Analysis by category
        categories = {
            'roof': 'Roof Condition',
            'siding': 'Exterior Siding',
            'landscaping': 'Landscaping',
            'hardscaping': 'Hardscaping'
        }
        
        for category, title in categories.items():
            issues = results['issues_by_category'].get(category, [])
            if issues:
                story.append(Paragraph(title, self.subheader_style))
                
                # Create table for issues in this category
                table_data = [['Issue Description', 'Severity', 'Estimated Cost', 'Confidence']]
                
                for issue in issues:
                    severity_color = self._get_severity_color(issue['severity'])
                    table_data.append([
                        issue['description'],
                        issue['severity'].title(),
                        f"${issue['estimated_cost']:,.0f}",
                        f"{int(issue['confidence'] * 100)}%"
                    ])
                
                issue_table = Table(table_data, colWidths=[3*inch, 0.8*inch, 1*inch, 0.8*inch])
                issue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (2, 1), (3, -1), 'CENTER')
                ]))
                
                story.append(issue_table)
                story.append(Spacer(1, 15))
                
                # Add recommendations for this category
                story.append(Paragraph(f"<b>{title} Recommendations:</b>", self.body_style))
                for issue in issues:
                    if issue.get('recommendation'):
                        rec_text = f"• {issue['recommendation']}"
                        story.append(Paragraph(rec_text, self.issue_style))
                story.append(Spacer(1, 20))
        
        return story
    
    def _create_cost_breakdown(self, results):
        """Create cost breakdown section"""
        story = []
        
        story.append(Paragraph("Cost Breakdown", self.header_style))
        story.append(Spacer(1, 12))
        
        # Cost breakdown table
        cost_data = [['Category', 'Estimated Cost', 'Percentage of Total']]
        total_cost = results['total_estimated_cost']
        
        for category, cost in results['cost_breakdown'].items():
            if cost > 0:
                percentage = (cost / total_cost) * 100 if total_cost > 0 else 0
                cost_data.append([
                    category.title().replace('_', ' '),
                    f"${cost:,.0f}",
                    f"{percentage:.1f}%"
                ])
        
        # Add total row
        cost_data.append(['TOTAL', f"${total_cost:,.0f}", '100.0%'])
        
        cost_table = Table(cost_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (2, -1), 'CENTER')
        ]))
        
        story.append(cost_table)
        story.append(Spacer(1, 20))
        
        # Cost estimation notes
        notes = """
        <b>Cost Estimation Notes:</b><br/>
        • Costs are estimated based on national averages and may vary by location<br/>
        • Labor costs can vary significantly based on local market conditions<br/>
        • Material costs are subject to market fluctuations<br/>
        • Some improvements may qualify for tax credits or rebates<br/>
        • Professional quotes are recommended for accurate pricing
        """
        story.append(Paragraph(notes, self.body_style))
        
        return story
    
    def _create_investment_analysis(self, results):
        """Create investment analysis section"""
        story = []
        
        story.append(Paragraph("Investment Analysis", self.header_style))
        story.append(Spacer(1, 12))
        
        # Investment metrics table
        investment_data = [
            ['Metric', 'Value', 'Notes'],
            ['Total Investment', f"${results['total_estimated_cost']:,.0f}", 'Cost of all improvements'],
            ['Potential Value Increase', f"${results['potential_value_increase']:,.0f}", 'Estimated property value gain'],
            ['Return on Investment', f"{results['roi_percentage']}%", 'Based on value increase'],
            ['Payback Period', f"{results['payback_years']} years", 'Time to recover investment'],
            ['Property Condition Score', f"{results['overall_condition_score']}/10", 'Current condition rating']
        ]
        
        investment_table = Table(investment_data, colWidths=[1.8*inch, 1.5*inch, 2.2*inch])
        investment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (1, -1), 'CENTER')
        ]))
        
        story.append(investment_table)
        story.append(Spacer(1, 20))
        
        # Investment recommendation
        roi = results['roi_percentage']
        if roi > 20:
            recommendation = "EXCELLENT INVESTMENT OPPORTUNITY"
            color = colors.HexColor('#28a745')
        elif roi > 10:
            recommendation = "GOOD INVESTMENT POTENTIAL"
            color = colors.HexColor('#ffc107')
        else:
            recommendation = "CONSIDER CAREFULLY"
            color = colors.HexColor('#dc3545')
        
        rec_style = ParagraphStyle(
            'RecommendationStyle',
            parent=self.body_style,
            fontSize=14,
            textColor=color,
            alignment=1,
            spaceAfter=10
        )
        
        story.append(Paragraph(f"<b>{recommendation}</b>", rec_style))
        
        # Detailed analysis
        analysis_text = f"""
        Based on the analysis, this property shows {"strong" if roi > 15 else "moderate" if roi > 8 else "limited"} 
        investment potential. The estimated improvements could increase the property value by 
        ${results['potential_value_increase']:,.0f}, representing a {roi}% return on the 
        ${results['total_estimated_cost']:,.0f} investment.
        """
        story.append(Paragraph(analysis_text, self.body_style))
        
        return story
    
    def _create_recommendations(self, results):
        """Create recommendations section"""
        story = []
        
        story.append(Paragraph("Recommendations", self.header_style))
        story.append(Spacer(1, 12))
        
        # Priority-based recommendations
        high_issues = [i for i in results['issues_found'] if i['severity'] == 'high']
        medium_issues = [i for i in results['issues_found'] if i['severity'] == 'medium']
        low_issues = [i for i in results['issues_found'] if i['severity'] == 'low']
        
        if high_issues:
            story.append(Paragraph("Immediate Action Required (High Priority)", self.subheader_style))
            for issue in high_issues:
                text = f"• {issue['description']} - Est. Cost: ${issue['estimated_cost']:,.0f}"
                story.append(Paragraph(text, self.issue_style))
            story.append(Spacer(1, 12))
        
        if medium_issues:
            story.append(Paragraph("Plan Within 6 Months (Medium Priority)", self.subheader_style))
            for issue in medium_issues:
                text = f"• {issue['description']} - Est. Cost: ${issue['estimated_cost']:,.0f}"
                story.append(Paragraph(text, self.issue_style))
            story.append(Spacer(1, 12))
        
        if low_issues:
            story.append(Paragraph("Regular Maintenance (Low Priority)", self.subheader_style))
            for issue in low_issues:
                text = f"• {issue['description']} - Est. Cost: ${issue['estimated_cost']:,.0f}"
                story.append(Paragraph(text, self.issue_style))
            story.append(Spacer(1, 12))
        
        # General recommendations
        general_recs = """
        <b>General Recommendations:</b><br/><br/>
        
        1. <b>Professional Inspections:</b> Schedule detailed inspections for high-priority items<br/>
        2. <b>Multiple Quotes:</b> Obtain quotes from multiple licensed contractors<br/>
        3. <b>Permits:</b> Verify permit requirements for major improvements<br/>
        4. <b>Insurance:</b> Check if improvements affect insurance coverage<br/>
        5. <b>Market Analysis:</b> Research local market conditions before major investments<br/>
        6. <b>Phased Approach:</b> Consider completing work in phases to spread costs<br/>
        7. <b>Energy Efficiency:</b> Explore energy-efficient options that may qualify for rebates
        """
        
        story.append(Paragraph(general_recs, self.body_style))
        story.append(Spacer(1, 20))
        
        # Footer
        footer_text = """
        <b>Andrew and Kelli Contractors</b> - This report was generated using AI-powered drone photo analysis. 
        For questions about this report or to schedule additional analysis, please contact your 
        real estate professional.
        """
        story.append(Paragraph(footer_text, self.body_style))
        
        return story
    
    def _get_condition_assessment(self, score):
        """Get condition assessment based on score"""
        if score >= 8:
            return "Excellent Condition"
        elif score >= 6:
            return "Good Condition"
        elif score >= 4:
            return "Fair Condition - Some Issues Identified"
        else:
            return "Poor Condition - Significant Issues Identified"
    
    def _get_severity_color(self, severity):
        """Get color based on severity"""
        colors_map = {
            'high': colors.red,
            'medium': colors.orange,
            'low': colors.green
        }
        return colors_map.get(severity, colors.black)