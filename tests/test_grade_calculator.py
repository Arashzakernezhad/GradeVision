import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grade_calculator import GradeCalculator


class TestGradeCalculator:
    """Test cases for GradeCalculator class"""
    
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        assert GradeCalculator._calculate_percentage(85, 100) == 85.0
        assert GradeCalculator._calculate_percentage(90, 100) == 90.0
        assert GradeCalculator._calculate_percentage(75, 100) == 75.0
    
    def test_calculate_percentage_zero_max_score(self):
        """Test percentage calculation with zero max_score"""
        assert GradeCalculator._calculate_percentage(85, 0) == 0
    
    def test_calculate_percentage_fractional(self):
        """Test percentage calculation with fractional scores"""
        assert abs(GradeCalculator._calculate_percentage(87.5, 100) - 87.5) < 0.01
        assert abs(GradeCalculator._calculate_percentage(42.5, 50) - 85.0) < 0.01
    
    def test_calculate_course_grade_simple(self):
        """Test course grade calculation with simple assignments"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 80, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
        ]
        grade = GradeCalculator.calculate_course_grade(assignments)
        # (80 * 0.5) + (90 * 0.5) = 40 + 45 = 85
        assert abs(grade - 85.0) < 0.01
    
    def test_calculate_course_grade_unequal_weights(self):
        """Test course grade with unequal weights"""
        assignments = [
            {'name': 'Midterm', 'weight': 30, 'score': 80, 'max_score': 100},
            {'name': 'Final', 'weight': 70, 'score': 90, 'max_score': 100}
        ]
        grade = GradeCalculator.calculate_course_grade(assignments)
        # (80 * 0.3) + (90 * 0.7) = 24 + 63 = 87
        assert abs(grade - 87.0) < 0.01
    
    def test_calculate_course_grade_with_none_score(self):
        """Test course grade calculation with ungraded assignments"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 80, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': None, 'max_score': 100}
        ]
        grade = GradeCalculator.calculate_course_grade(assignments)
        # Only Midterm counts: 80 * 0.5 / 0.5 = 80
        assert abs(grade - 80.0) < 0.01
    
    def test_calculate_course_grade_all_none_scores(self):
        """Test course grade when all scores are None"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': None, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': None, 'max_score': 100}
        ]
        grade = GradeCalculator.calculate_course_grade(assignments)
        assert grade == 0
    
    def test_calculate_course_grade_empty_assignments(self):
        """Test course grade with empty assignments list"""
        assignments = []
        grade = GradeCalculator.calculate_course_grade(assignments)
        assert grade == 0
    
    def test_calculate_course_grade_multiple_assignments(self):
        """Test course grade with multiple assignments"""
        assignments = [
            {'name': 'HW1', 'weight': 10, 'score': 90, 'max_score': 100},
            {'name': 'HW2', 'weight': 10, 'score': 85, 'max_score': 100},
            {'name': 'Midterm', 'weight': 30, 'score': 80, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 95, 'max_score': 100}
        ]
        grade = GradeCalculator.calculate_course_grade(assignments)
        # (90*0.1) + (85*0.1) + (80*0.3) + (95*0.5) = 9 + 8.5 + 24 + 47.5 = 89
        assert abs(grade - 89.0) < 0.01
    
    def test_grade_to_points_4_0(self):
        """Test grade to points conversion for A (4.0)"""
        assert GradeCalculator._grade_to_points(95) == 4.0
        assert GradeCalculator._grade_to_points(90) == 4.0
        assert GradeCalculator._grade_to_points(100) == 4.0
    
    def test_grade_to_points_3_7(self):
        """Test grade to points conversion for A- (3.7)"""
        assert GradeCalculator._grade_to_points(89) == 3.7
        assert GradeCalculator._grade_to_points(85) == 3.7
    
    def test_grade_to_points_3_3(self):
        """Test grade to points conversion for B+ (3.3)"""
        assert GradeCalculator._grade_to_points(84) == 3.3
        assert GradeCalculator._grade_to_points(80) == 3.3
    
    def test_grade_to_points_3_0(self):
        """Test grade to points conversion for B (3.0)"""
        assert GradeCalculator._grade_to_points(79) == 3.0
        assert GradeCalculator._grade_to_points(75) == 3.0
    
    def test_grade_to_points_2_7(self):
        """Test grade to points conversion for B- (2.7)"""
        assert GradeCalculator._grade_to_points(74) == 2.7
        assert GradeCalculator._grade_to_points(70) == 2.7
    
    def test_grade_to_points_2_3(self):
        """Test grade to points conversion for C+ (2.3)"""
        assert GradeCalculator._grade_to_points(69) == 2.3
        assert GradeCalculator._grade_to_points(65) == 2.3
    
    def test_grade_to_points_2_0(self):
        """Test grade to points conversion for C (2.0)"""
        assert GradeCalculator._grade_to_points(64) == 2.0
        assert GradeCalculator._grade_to_points(60) == 2.0
    
    def test_grade_to_points_1_7(self):
        """Test grade to points conversion for C- (1.7)"""
        assert GradeCalculator._grade_to_points(59) == 1.7
        assert GradeCalculator._grade_to_points(55) == 1.7
    
    def test_grade_to_points_1_0(self):
        """Test grade to points conversion for D (1.0)"""
        assert GradeCalculator._grade_to_points(54) == 1.0
        assert GradeCalculator._grade_to_points(50) == 1.0
    
    def test_grade_to_points_0_0(self):
        """Test grade to points conversion for F (0.0)"""
        assert GradeCalculator._grade_to_points(49) == 0.0
        assert GradeCalculator._grade_to_points(0) == 0.0
    
    def test_calculate_gpa_single_course(self):
        """Test GPA calculation with single course"""
        courses = [
            {
                'name': 'CPSC 3720',
                'assignments': [
                    {'name': 'Midterm', 'weight': 50, 'score': 90, 'max_score': 100},
                    {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
                ]
            }
        ]
        gpa = GradeCalculator.calculate_gpa(courses)
        # 90% = 4.0 GPA
        assert abs(gpa - 4.0) < 0.01
    
    def test_calculate_gpa_multiple_courses(self):
        """Test GPA calculation with multiple courses"""
        courses = [
            {
                'name': 'CPSC 3720',
                'assignments': [
                    {'name': 'Midterm', 'weight': 50, 'score': 90, 'max_score': 100},
                    {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
                ]
            },
            {
                'name': 'CPSC 4660',
                'assignments': [
                    {'name': 'Project', 'weight': 100, 'score': 80, 'max_score': 100}
                ]
            }
        ]
        gpa = GradeCalculator.calculate_gpa(courses)
        # Course 1: 90% = 4.0, Course 2: 80% = 3.3
        # Average: (4.0 + 3.3) / 2 = 3.65
        assert abs(gpa - 3.65) < 0.01
    
    def test_calculate_gpa_empty_courses(self):
        """Test GPA calculation with empty courses list"""
        courses = []
        gpa = GradeCalculator.calculate_gpa(courses)
        assert gpa == 0
    
    def test_calculate_gpa_with_negative_grade(self):
        """Test GPA calculation with negative grade (should be excluded)"""
        courses = [
            {
                'name': 'CPSC 3720',
                'assignments': [
                    {'name': 'Midterm', 'weight': 50, 'score': 90, 'max_score': 100}
                ]
            },
            {
                'name': 'CPSC 4660',
                'assignments': [
                    {'name': 'Project', 'weight': 100, 'score': None, 'max_score': 100}
                ]
            }
        ]
        gpa = GradeCalculator.calculate_gpa(courses)
        # Only first course counts (90% = 4.0)
        assert abs(gpa - 4.0) < 0.01
    
    def test_predict_final_grade(self):
        """Test predicting final grade"""
        current_assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 80, 'max_score': 100}
        ]
        future_score = 90
        future_weight = 50
        
        predicted = GradeCalculator.predict_final_grade(
            current_assignments, future_score, future_weight
        )
        # Current: 80 * 0.5 = 40, Future: 90 * 0.5 = 45, Total = 85
        assert abs(predicted - 85.0) < 0.01
    
    def test_predict_final_grade_complex(self):
        """Test predicting final grade with multiple current assignments"""
        current_assignments = [
            {'name': 'HW1', 'weight': 20, 'score': 90, 'max_score': 100},
            {'name': 'HW2', 'weight': 20, 'score': 85, 'max_score': 100},
            {'name': 'Midterm', 'weight': 30, 'score': 80, 'max_score': 100}
        ]
        future_score = 95
        future_weight = 30
        
        predicted = GradeCalculator.predict_final_grade(
            current_assignments, future_score, future_weight
        )
        # Current: (90*0.2) + (85*0.2) + (80*0.3) = 18 + 17 + 24 = 59
        # Future: 95 * 0.3 = 28.5
        # Total: 59 + 28.5 = 87.5
        assert abs(predicted - 87.5) < 0.01
    
    def test_predict_final_grade_with_none_scores(self):
        """Test predicting final grade with ungraded assignments"""
        current_assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 80, 'max_score': 100},
            {'name': 'HW', 'weight': 20, 'score': None, 'max_score': 100}
        ]
        future_score = 90
        future_weight = 30
        
        predicted = GradeCalculator.predict_final_grade(
            current_assignments, future_score, future_weight
        )
        # Current: 80 * 0.5 = 40, Future: 90 * 0.3 = 27, Total = 67
        assert abs(predicted - 67.0) < 0.01

