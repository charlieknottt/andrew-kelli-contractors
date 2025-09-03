import cv2
import numpy as np
from PIL import Image, ImageEnhance
import random
import math
from datetime import datetime

class PropertyAnalyzer:
    def __init__(self):
        self.cost_ranges = {
            'roof': {'min': 5000, 'max': 25000, 'default': 12000},
            'siding': {'min': 8000, 'max': 15000, 'default': 11000},
            'landscaping': {'min': 2000, 'max': 10000, 'default': 5000},
            'hardscaping': {'min': 3000, 'max': 8000, 'default': 5500},
            'windows': {'min': 2000, 'max': 12000, 'default': 6000},
            'gutters': {'min': 1000, 'max': 3000, 'default': 1800}
        }
        
    def analyze_property(self, image_paths):
        """Main analysis function that processes all uploaded images"""
        analysis_results = {
            'images_analyzed': len(image_paths),
            'issues_found': [],
            'issues_by_category': {
                'roof': [],
                'siding': [],
                'landscaping': [],
                'hardscaping': []
            },
            'cost_breakdown': {
                'roof': 0,
                'siding': 0,
                'landscaping': 0,
                'hardscaping': 0,
                'windows': 0,
                'gutters': 0
            },
            'total_estimated_cost': 0,
            'overall_condition_score': 0,
            'estimated_timeline_weeks': 0,
            'potential_value_increase': 0,
            'roi_percentage': 0,
            'payback_years': 0
        }
        
        all_issues = []
        
        # Analyze each image
        for image_path in image_paths:
            image_issues = self._analyze_single_image(image_path)
            all_issues.extend(image_issues)
        
        # Process and categorize issues
        categorized_issues = self._categorize_issues(all_issues)
        analysis_results['issues_by_category'] = categorized_issues
        analysis_results['issues_found'] = all_issues
        
        # Calculate costs
        cost_breakdown = self._calculate_costs(categorized_issues)
        analysis_results['cost_breakdown'] = cost_breakdown
        analysis_results['total_estimated_cost'] = sum(cost_breakdown.values())
        
        # Calculate other metrics
        analysis_results['overall_condition_score'] = self._calculate_condition_score(all_issues)
        analysis_results['estimated_timeline_weeks'] = self._estimate_timeline(all_issues)
        analysis_results['potential_value_increase'] = self._estimate_value_increase(analysis_results['total_estimated_cost'])
        analysis_results['roi_percentage'] = self._calculate_roi(analysis_results['total_estimated_cost'], analysis_results['potential_value_increase'])
        analysis_results['payback_years'] = self._calculate_payback_period(analysis_results['roi_percentage'])
        
        return analysis_results
    
    def _analyze_single_image(self, image_path):
        """Analyze a single image and detect issues"""
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return []
                
            # Convert to RGB for PIL
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            
            # Enhance image for better analysis
            enhanced_img = self._enhance_image(pil_img)
            
            # Convert back to OpenCV format
            enhanced_cv = cv2.cvtColor(np.array(enhanced_img), cv2.COLOR_RGB2BGR)
            
            # Analyze different aspects of the property
            issues = []
            issues.extend(self._analyze_roof_condition(enhanced_cv))
            issues.extend(self._analyze_siding_condition(enhanced_cv))
            issues.extend(self._analyze_landscaping(enhanced_cv))
            issues.extend(self._analyze_hardscaping(enhanced_cv))
            
            return issues
            
        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            return []
    
    def _enhance_image(self, pil_img):
        """Enhance image quality for better analysis"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_img)
        enhanced = enhancer.enhance(1.2)
        
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        return enhanced
    
    def _analyze_roof_condition(self, img):
        """Analyze roof condition using computer vision techniques"""
        issues = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Edge detection to find roof lines and potential damage
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours (potential damaged areas)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Simulate roof analysis based on image characteristics
        height, width = img.shape[:2]
        
        # Simulate various roof issues based on image analysis
        roof_issues = self._simulate_roof_issues(gray, width, height)
        issues.extend(roof_issues)
        
        return issues
    
    def _simulate_roof_issues(self, gray_img, width, height):
        """Simulate realistic roof issue detection"""
        issues = []
        
        # Calculate image statistics for realistic simulation
        mean_intensity = np.mean(gray_img)
        std_intensity = np.std(gray_img)
        
        # Simulate different roof conditions based on image characteristics
        if mean_intensity < 100:  # Darker areas might indicate damage
            issues.append({
                'category': 'roof',
                'description': 'Potential roof damage detected in darker areas',
                'severity': 'high',
                'confidence': 0.75,
                'estimated_cost': random.randint(8000, 15000),
                'cost_range': {'min': 8000, 'max': 15000},
                'recommendation': 'Professional roof inspection recommended'
            })
        
        if std_intensity > 50:  # High variation might indicate wear
            issues.append({
                'category': 'roof',
                'description': 'Uneven roof surface indicating potential wear',
                'severity': 'medium',
                'confidence': 0.65,
                'estimated_cost': random.randint(3000, 8000),
                'cost_range': {'min': 3000, 'max': 8000},
                'recommendation': 'Monitor condition and plan for maintenance'
            })
        
        # Randomly add common roof issues for demonstration
        common_issues = [
            {
                'description': 'Missing or damaged shingles observed',
                'severity': 'high',
                'cost_range': {'min': 5000, 'max': 12000}
            },
            {
                'description': 'Gutter system needs attention',
                'severity': 'medium',
                'cost_range': {'min': 1500, 'max': 3500}
            },
            {
                'description': 'Roof aging showing wear patterns',
                'severity': 'low',
                'cost_range': {'min': 2000, 'max': 6000}
            }
        ]
        
        # Add 1-2 random issues for demonstration
        for _ in range(random.randint(1, 2)):
            issue = random.choice(common_issues)
            cost = random.randint(issue['cost_range']['min'], issue['cost_range']['max'])
            issues.append({
                'category': 'roof',
                'description': issue['description'],
                'severity': issue['severity'],
                'confidence': random.uniform(0.6, 0.9),
                'estimated_cost': cost,
                'cost_range': issue['cost_range'],
                'recommendation': self._get_recommendation(issue['severity'])
            })
        
        return issues
    
    def _analyze_siding_condition(self, img):
        """Analyze exterior siding condition"""
        issues = []
        
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Simulate siding analysis
        siding_issues = [
            {
                'description': 'Exterior paint showing signs of weathering',
                'severity': 'medium',
                'cost_range': {'min': 4000, 'max': 8000}
            },
            {
                'description': 'Siding material needs maintenance',
                'severity': 'low',
                'cost_range': {'min': 2000, 'max': 5000}
            },
            {
                'description': 'Window trim requires attention',
                'severity': 'medium',
                'cost_range': {'min': 1500, 'max': 3000}
            }
        ]
        
        # Add siding issues based on analysis
        if random.random() > 0.3:  # 70% chance of finding siding issues
            issue = random.choice(siding_issues)
            cost = random.randint(issue['cost_range']['min'], issue['cost_range']['max'])
            issues.append({
                'category': 'siding',
                'description': issue['description'],
                'severity': issue['severity'],
                'confidence': random.uniform(0.5, 0.8),
                'estimated_cost': cost,
                'cost_range': issue['cost_range'],
                'recommendation': self._get_recommendation(issue['severity'])
            })
        
        return issues
    
    def _analyze_landscaping(self, img):
        """Analyze landscaping condition"""
        issues = []
        
        # Convert to HSV for vegetation analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Create mask for green areas (vegetation)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_percentage = np.sum(green_mask > 0) / (green_mask.shape[0] * green_mask.shape[1])
        
        landscaping_issues = [
            {
                'description': 'Lawn maintenance and reseeding needed',
                'severity': 'medium',
                'cost_range': {'min': 1500, 'max': 4000}
            },
            {
                'description': 'Overgrown vegetation requires trimming',
                'severity': 'low',
                'cost_range': {'min': 800, 'max': 2000}
            },
            {
                'description': 'Garden beds need landscaping attention',
                'severity': 'medium',
                'cost_range': {'min': 2000, 'max': 5000}
            }
        ]
        
        # Determine landscaping issues based on green coverage
        if green_percentage < 0.1:  # Low vegetation
            issue = {
                'description': 'Limited landscaping - property needs significant garden development',
                'severity': 'medium',
                'cost_range': {'min': 3000, 'max': 8000}
            }
        elif green_percentage > 0.4:  # High vegetation
            issue = {
                'description': 'Overgrown landscaping requires professional maintenance',
                'severity': 'low',
                'cost_range': {'min': 1000, 'max': 3000}
            }
        else:
            issue = random.choice(landscaping_issues)
        
        cost = random.randint(issue['cost_range']['min'], issue['cost_range']['max'])
        issues.append({
            'category': 'landscaping',
            'description': issue['description'],
            'severity': issue['severity'],
            'confidence': random.uniform(0.6, 0.85),
            'estimated_cost': cost,
            'cost_range': issue['cost_range'],
            'recommendation': self._get_recommendation(issue['severity'])
        })
        
        return issues
    
    def _analyze_hardscaping(self, img):
        """Analyze hardscaping elements (driveways, walkways, etc.)"""
        issues = []
        
        # Convert to grayscale for hardscape analysis
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        hardscaping_issues = [
            {
                'description': 'Driveway surface showing cracks and wear',
                'severity': 'medium',
                'cost_range': {'min': 2500, 'max': 6000}
            },
            {
                'description': 'Walkway maintenance required',
                'severity': 'low',
                'cost_range': {'min': 1000, 'max': 3000}
            },
            {
                'description': 'Patio or deck needs refurbishment',
                'severity': 'medium',
                'cost_range': {'min': 3000, 'max': 7000}
            }
        ]
        
        # Add hardscaping issues randomly
        if random.random() > 0.4:  # 60% chance
            issue = random.choice(hardscaping_issues)
            cost = random.randint(issue['cost_range']['min'], issue['cost_range']['max'])
            issues.append({
                'category': 'hardscaping',
                'description': issue['description'],
                'severity': issue['severity'],
                'confidence': random.uniform(0.55, 0.8),
                'estimated_cost': cost,
                'cost_range': issue['cost_range'],
                'recommendation': self._get_recommendation(issue['severity'])
            })
        
        return issues
    
    def _categorize_issues(self, all_issues):
        """Categorize issues by type"""
        categorized = {
            'roof': [],
            'siding': [],
            'landscaping': [],
            'hardscaping': []
        }
        
        for issue in all_issues:
            category = issue.get('category', 'other')
            if category in categorized:
                categorized[category].append(issue)
        
        return categorized
    
    def _calculate_costs(self, categorized_issues):
        """Calculate total costs by category"""
        cost_breakdown = {
            'roof': 0,
            'siding': 0,
            'landscaping': 0,
            'hardscaping': 0,
            'windows': 0,
            'gutters': 0
        }
        
        for category, issues in categorized_issues.items():
            total_cost = sum(issue['estimated_cost'] for issue in issues)
            if category in cost_breakdown:
                cost_breakdown[category] = total_cost
        
        return cost_breakdown
    
    def _calculate_condition_score(self, all_issues):
        """Calculate overall property condition score (1-10)"""
        if not all_issues:
            return 8  # Good condition if no issues found
        
        # Calculate score based on severity and number of issues
        severity_weights = {'high': 3, 'medium': 2, 'low': 1}
        total_severity = sum(severity_weights.get(issue['severity'], 1) for issue in all_issues)
        
        # Scale to 1-10 (higher is better)
        max_possible_severity = len(all_issues) * 3
        if max_possible_severity > 0:
            severity_ratio = total_severity / max_possible_severity
            score = max(1, 10 - (severity_ratio * 6))  # Scale to 1-10 range
        else:
            score = 8
        
        return round(score, 1)
    
    def _estimate_timeline(self, all_issues):
        """Estimate timeline in weeks for all repairs"""
        if not all_issues:
            return 0
        
        # Base timeline by severity
        timeline_by_severity = {'high': 3, 'medium': 2, 'low': 1}
        total_weeks = 0
        
        for issue in all_issues:
            weeks = timeline_by_severity.get(issue['severity'], 1)
            total_weeks += weeks
        
        # Add some overlap consideration (reduce by 20%)
        total_weeks = max(1, int(total_weeks * 0.8))
        
        return total_weeks
    
    def _estimate_value_increase(self, total_cost):
        """Estimate property value increase from improvements"""
        # Typical ROI for property improvements is 60-80% of investment
        roi_multiplier = random.uniform(0.65, 0.85)
        return int(total_cost * roi_multiplier)
    
    def _calculate_roi(self, investment, value_increase):
        """Calculate ROI percentage"""
        if investment > 0:
            roi = (value_increase / investment) * 100
            return round(roi, 1)
        return 0
    
    def _calculate_payback_period(self, roi_percentage):
        """Calculate payback period in years"""
        if roi_percentage > 0:
            # Assuming annual appreciation/rental increase
            annual_return = max(3, roi_percentage / 5)  # Conservative estimate
            payback = 100 / annual_return
            return round(payback, 1)
        return 0
    
    def _get_recommendation(self, severity):
        """Get recommendation based on issue severity"""
        recommendations = {
            'high': 'Immediate attention required - schedule professional assessment',
            'medium': 'Plan for repair within next 6 months',
            'low': 'Monitor condition and include in regular maintenance schedule'
        }
        return recommendations.get(severity, 'Professional assessment recommended')