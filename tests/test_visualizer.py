import pytest
import sys
import os
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from visualizer import GradeVisualizer
from data_manager import DataManager
from grade_calculator import GradeCalculator


class TestGradeVisualizer:
    """Test cases for GradeVisualizer class"""
    
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        assert GradeVisualizer.calculate_percentage(85, 100) == 85.0
        assert GradeVisualizer.calculate_percentage(90, 100) == 90.0
        assert GradeVisualizer.calculate_percentage(75, 100) == 75.0
    
    def test_calculate_percentage_zero_max_score(self):
        """Test percentage calculation with zero max_score"""
        assert GradeVisualizer.calculate_percentage(85, 0) == 0
    
    def test_calculate_percentage_fractional(self):
        """Test percentage calculation with fractional scores"""
        assert abs(GradeVisualizer.calculate_percentage(87.5, 100) - 87.5) < 0.01
        assert abs(GradeVisualizer.calculate_percentage(42.5, 50) - 85.0) < 0.01
    
    def test_plot_course_grades_basic(self):
        """Test plotting course grades with basic data"""
        dm = DataManager()
        assignments1 = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 100, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_course_grades(dm, fig)
        
        assert result is not None
        assert result == fig
        plt.close(fig)
    
    def test_plot_course_grades_empty(self):
        """Test plotting course grades with empty data"""
        dm = DataManager()
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_course_grades(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_course_grades_with_none_scores(self):
        """Test plotting course grades with ungraded assignments"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': None, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_course_grades(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_assignment_performance_single_course(self):
        """Test plotting assignment performance for single course"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        fig = plt.Figure(figsize=(12, 6))
        result = GradeVisualizer.plot_assignment_performance(dm, 'CPSC 3720', fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_assignment_performance_all_courses(self):
        """Test plotting assignment performance for all courses"""
        dm = DataManager()
        assignments1 = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 100, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        fig = plt.Figure(figsize=(12, 6))
        result = GradeVisualizer.plot_assignment_performance(dm, None, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_assignment_performance_empty(self):
        """Test plotting assignment performance with empty data"""
        dm = DataManager()
        fig = plt.Figure(figsize=(12, 6))
        result = GradeVisualizer.plot_assignment_performance(dm, None, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_assignment_performance_with_none_scores(self):
        """Test plotting assignment performance with ungraded assignments"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': None, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        fig = plt.Figure(figsize=(12, 6))
        result = GradeVisualizer.plot_assignment_performance(dm, 'CPSC 3720', fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_grade_distribution(self):
        """Test plotting grade distribution"""
        dm = DataManager()
        assignments1 = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 100, 'score': 75, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_grade_distribution(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_grade_distribution_empty(self):
        """Test plotting grade distribution with empty data"""
        dm = DataManager()
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_grade_distribution(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_weight_distribution_single_course(self):
        """Test plotting weight distribution for single course"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 30, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 70, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_weight_distribution(dm, 'CPSC 3720', fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_weight_distribution_all_courses(self):
        """Test plotting weight distribution for all courses"""
        dm = DataManager()
        assignments1 = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 100, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_weight_distribution(dm, None, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_weight_distribution_empty(self):
        """Test plotting weight distribution with empty data"""
        dm = DataManager()
        fig = plt.Figure(figsize=(10, 6))
        result = GradeVisualizer.plot_weight_distribution(dm, None, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_gpa_trend(self):
        """Test plotting GPA trend"""
        dm = DataManager()
        assignments1 = [
            {'name': 'Midterm', 'weight': 50, 'score': 90, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 100, 'score': 80, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        fig = plt.Figure(figsize=(8, 6))
        result = GradeVisualizer.plot_gpa_trend(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_gpa_trend_empty(self):
        """Test plotting GPA trend with empty data"""
        dm = DataManager()
        fig = plt.Figure(figsize=(8, 6))
        result = GradeVisualizer.plot_gpa_trend(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_plot_gpa_trend_single_course(self):
        """Test plotting GPA trend with single course"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 95, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        fig = plt.Figure(figsize=(8, 6))
        result = GradeVisualizer.plot_gpa_trend(dm, fig)
        
        assert result is not None
        plt.close(fig)
    
    def test_all_plots_with_real_data(self):
        """Test all plot functions with realistic data"""
        dm = DataManager()
        assignments1 = [
            {'name': 'HW1', 'weight': 10, 'score': 90, 'max_score': 100},
            {'name': 'HW2', 'weight': 10, 'score': 85, 'max_score': 100},
            {'name': 'Midterm', 'weight': 30, 'score': 80, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 95, 'max_score': 100}
        ]
        assignments2 = [
            {'name': 'Project', 'weight': 50, 'score': 88, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 75, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments1)
        dm.add_course('CPSC 4660', assignments2)
        
        # Test all visualization functions
        fig1 = plt.Figure(figsize=(10, 6))
        GradeVisualizer.plot_course_grades(dm, fig1)
        plt.close(fig1)
        
        fig2 = plt.Figure(figsize=(12, 6))
        GradeVisualizer.plot_assignment_performance(dm, None, fig2)
        plt.close(fig2)
        
        fig3 = plt.Figure(figsize=(10, 6))
        GradeVisualizer.plot_grade_distribution(dm, fig3)
        plt.close(fig3)
        
        fig4 = plt.Figure(figsize=(10, 6))
        GradeVisualizer.plot_weight_distribution(dm, None, fig4)
        plt.close(fig4)
        
        fig5 = plt.Figure(figsize=(8, 6))
        GradeVisualizer.plot_gpa_trend(dm, fig5)
        plt.close(fig5)
        
        # If we get here without exceptions, all plots work
        assert True

