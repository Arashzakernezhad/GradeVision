import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))
from grade_calculator import GradeCalculator

class GradeVisualizer:
    @staticmethod
    def calculate_percentage(score, max_score):
        """Calculate percentage score"""
        if max_score == 0:
            return 0
        return (score / max_score) * 100
    
    @staticmethod
    def plot_course_grades(data_manager, figure=None):
        """Plot grades for all courses"""
        if figure is None:
            figure, ax = plt.subplots(figsize=(10, 6))
        else:
            ax = figure.gca()
            ax.clear()
        
        courses = data_manager.courses
        course_names = []
        course_grades = []
        
        for course in courses:
            grade = GradeCalculator.calculate_course_grade(course['assignments'])
            course_names.append(course['name'])
            course_grades.append(grade)
        
        if course_grades:
            colors = ['#2E86AB' if g >= 90 else '#A23B72' if g >= 80 else '#F18F01' if g >= 70 else '#C73E1D' for g in course_grades]
            bars = ax.bar(course_names, course_grades, color=colors, edgecolor='black', linewidth=1.5)
            ax.set_ylabel('Grade (%)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Course', fontsize=12, fontweight='bold')
            ax.set_title('Course Grades Overview', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylim(0, 100)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.axhline(y=90, color='green', linestyle='--', alpha=0.5, label='A (90%)')
            ax.axhline(y=80, color='blue', linestyle='--', alpha=0.5, label='B (80%)')
            ax.axhline(y=70, color='orange', linestyle='--', alpha=0.5, label='C (70%)')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom', fontweight='bold')
            
            ax.legend(loc='upper right')
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        figure.tight_layout()
        return figure
    
    @staticmethod
    def plot_assignment_performance(data_manager, course_name=None, figure=None):
        """Plot assignment performance for a specific course or all courses"""
        if figure is None:
            figure, ax = plt.subplots(figsize=(12, 6))
        else:
            ax = figure.gca()
            ax.clear()
        
        courses = data_manager.courses
        if course_name:
            courses = [c for c in courses if c['name'] == course_name]
        
        assignment_names = []
        percentages = []
        colors_list = []
        
        for course in courses:
            for assignment in course['assignments']:
                if assignment['score'] is not None:
                    percentage = GradeVisualizer.calculate_percentage(
                        assignment['score'], assignment['max_score']
                    )
                    assignment_names.append(f"{course['name']}\n{assignment['name']}")
                    percentages.append(percentage)
                    colors_list.append('#2E86AB' if percentage >= 90 else '#A23B72' if percentage >= 80 else '#F18F01' if percentage >= 70 else '#C73E1D')
        
        if percentages:
            bars = ax.bar(range(len(assignment_names)), percentages, color=colors_list, edgecolor='black', linewidth=1)
            ax.set_xticks(range(len(assignment_names)))
            ax.set_xticklabels(assignment_names, rotation=45, ha='right', fontsize=9)
            ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Assignments', fontsize=12, fontweight='bold')
            title = f'Assignment Performance - {course_name}' if course_name else 'All Assignments Performance'
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.set_ylim(0, 100)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Add value labels
            for i, (bar, pct) in enumerate(zip(bars, percentages)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{pct:.1f}%',
                       ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        figure.tight_layout()
        return figure
    
    @staticmethod
    def plot_grade_distribution(data_manager, figure=None):
        """Plot grade distribution histogram"""
        if figure is None:
            figure, ax = plt.subplots(figsize=(10, 6))
        else:
            ax = figure.gca()
            ax.clear()
        
        all_grades = []
        for course in data_manager.courses:
            for assignment in course['assignments']:
                if assignment['score'] is not None:
                    percentage = GradeVisualizer.calculate_percentage(
                        assignment['score'], assignment['max_score']
                    )
                    all_grades.append(percentage)
        
        if all_grades:
            bins = [0, 60, 70, 80, 90, 100]
            labels = ['F (<60)', 'D (60-69)', 'C (70-79)', 'B (80-89)', 'A (90-100)']
            colors = ['#C73E1D', '#F18F01', '#A23B72', '#2E86AB', '#06A77D']
            
            counts, edges, bars = ax.hist(all_grades, bins=bins, color=colors, edgecolor='black', linewidth=1.5, alpha=0.7)
            ax.set_xlabel('Grade Range (%)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Assignments', fontsize=12, fontweight='bold')
            ax.set_title('Grade Distribution', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks([30, 65, 75, 85, 95])
            ax.set_xticklabels(labels)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Add count labels on bars
            for bar, count in zip(bars, counts):
                if count > 0:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(count)}',
                           ha='center', va='bottom', fontweight='bold')
        
        figure.tight_layout()
        return figure
    
    @staticmethod
    def plot_weight_distribution(data_manager, course_name=None, figure=None):
        """Plot weight distribution for assignments"""
        if figure is None:
            figure, ax = plt.subplots(figsize=(10, 6))
        else:
            ax = figure.gca()
            ax.clear()
        
        courses = data_manager.courses
        if course_name:
            courses = [c for c in courses if c['name'] == course_name]
        
        assignment_labels = []
        weights = []
        
        for course in courses:
            for assignment in course['assignments']:
                assignment_labels.append(f"{course['name']}\n{assignment['name']}")
                weights.append(assignment['weight'])
        
        if weights:
            colors = plt.cm.viridis(np.linspace(0, 1, len(weights)))
            bars = ax.barh(range(len(assignment_labels)), weights, color=colors, edgecolor='black', linewidth=1)
            ax.set_yticks(range(len(assignment_labels)))
            ax.set_yticklabels(assignment_labels, fontsize=9)
            ax.set_xlabel('Weight (%)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Assignments', fontsize=12, fontweight='bold')
            title = f'Assignment Weight Distribution - {course_name}' if course_name else 'All Assignment Weights'
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Add value labels
            for i, (bar, weight) in enumerate(zip(bars, weights)):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{weight}%',
                       ha='left', va='center', fontweight='bold', fontsize=9)
        
        figure.tight_layout()
        return figure
    
    @staticmethod
    def plot_gpa_trend(data_manager, figure=None):
        """Plot GPA calculation"""
        if figure is None:
            figure, ax = plt.subplots(figsize=(8, 6))
        else:
            ax = figure.gca()
            ax.clear()
        
        gpa = GradeCalculator.calculate_gpa(data_manager.courses)
        
        # Create a simple bar chart for GPA
        ax.bar(['Overall GPA'], [gpa], color='#2E86AB', edgecolor='black', linewidth=2, width=0.5)
        ax.set_ylabel('GPA', fontsize=12, fontweight='bold')
        ax.set_title('Overall GPA', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 4.0)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add GPA reference lines
        ax.axhline(y=4.0, color='green', linestyle='--', alpha=0.5, label='4.0 (A)')
        ax.axhline(y=3.0, color='blue', linestyle='--', alpha=0.5, label='3.0 (B)')
        ax.axhline(y=2.0, color='orange', linestyle='--', alpha=0.5, label='2.0 (C)')
        
        # Add value label
        ax.text(0, gpa, f'{gpa:.2f}',
               ha='center', va='bottom', fontweight='bold', fontsize=16)
        
        ax.legend(loc='upper right')
        figure.tight_layout()
        return figure

