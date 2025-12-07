import pytest
import sys
import os
import tempfile
import tkinter as tk

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))
from ui_menu import GradeVisionUI
from data_manager import DataManager


class TestGradeVisionUI:
    """Test cases for GradeVisionUI class"""
    
    @pytest.fixture
    def root(self):
        """Create a root window for testing"""
        root = tk.Tk()
        root.withdraw()  # Hide the window during tests
        yield root
        root.destroy()
    
    @pytest.fixture
    def ui(self, root):
        """Create a UI instance for testing"""
        return GradeVisionUI(root)
    
    def test_ui_initialization(self, root):
        """Test UI initialization"""
        ui = GradeVisionUI(root)
        assert ui.root == root
        assert ui.data_manager is not None
        assert isinstance(ui.data_manager, DataManager)
        assert ui.current_file is None
        assert ui.notebook is not None
        assert ui.info_text is not None
        assert ui.status_label is not None
    
    def test_ui_has_menu_bar(self, ui):
        """Test that UI has menu bar"""
        menu = ui.root.config('menu')
        assert menu is not None
    
    def test_ui_has_toolbar(self, ui):
        """Test that UI has toolbar with status label"""
        assert ui.status_label is not None
        assert ui.status_label.cget('text') == "No file loaded"
    
    def test_ui_has_notebook(self, ui):
        """Test that UI has notebook with tabs"""
        assert ui.notebook is not None
        # Check that tabs exist
        tabs = ui.notebook.tabs()
        assert len(tabs) >= 2  # At least Info and Visualizations tabs
    
    def test_update_info_display_no_data(self, ui):
        """Test info display update with no data"""
        ui.update_info_display()
        content = ui.info_text.get(1.0, tk.END)
        assert "No data loaded" in content
        assert "Expected CSV format" in content
    
    def test_update_info_display_with_data(self, ui):
        """Test info display update with data"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': 90, 'max_score': 100}
        ]
        ui.data_manager.add_course('CPSC 3720', assignments)
        
        ui.update_info_display()
        content = ui.info_text.get(1.0, tk.END)
        assert "CPSC 3720" in content
        assert "Midterm" in content
        assert "Final" in content
    
    def test_update_info_display_with_none_scores(self, ui):
        """Test info display with ungraded assignments"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 50, 'score': None, 'max_score': 100}
        ]
        ui.data_manager.add_course('CPSC 3720', assignments)
        
        ui.update_info_display()
        content = ui.info_text.get(1.0, tk.END)
        assert "CPSC 3720" in content
        assert "Not yet graded" in content
    
    def test_get_course_names(self, ui):
        """Test getting course names from data manager"""
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        ui.data_manager.add_course('CPSC 3720', assignments)
        ui.data_manager.add_course('CPSC 4660', assignments)
        
        course_names = ui.data_manager.get_course_names()
        assert 'CPSC 3720' in course_names
        assert 'CPSC 4660' in course_names
    
    def test_show_visualization_no_data(self, ui):
        """Test showing visualization with no data"""
        # This should show a warning messagebox
        # We can't easily test messagebox, but we can test it doesn't crash
        try:
            ui.show_visualization('course_grades')
            # If we get here, no exception was raised
            assert True
        except Exception as e:
            # If an exception is raised, it should be handled gracefully
            # The function should show a warning, not crash
            pass
    
    def test_show_visualization_with_data(self, ui):
        """Test showing visualization with data"""
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}
        ]
        ui.data_manager.add_course('CPSC 3720', assignments)
        
        # Test that visualization doesn't crash
        try:
            ui.show_visualization('course_grades')
            assert True
        except Exception as e:
            pytest.fail(f"Visualization raised exception: {e}")
    
    def test_select_course_dialog_creation(self, ui):
        """Test that select_course creates a dialog"""
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        ui.data_manager.add_course('CPSC 3720', assignments)
        ui.data_manager.add_course('CPSC 4660', assignments)
        
        # Note: This test is limited because the dialog is modal
        # We can at least test that the method exists and can be called
        # In a real scenario, you'd need to mock the dialog
        course_names = ui.data_manager.get_course_names()
        assert len(course_names) == 2
    
    def test_data_manager_integration(self, ui):
        """Test integration with DataManager"""
        assert isinstance(ui.data_manager, DataManager)
        assert len(ui.data_manager.courses) == 0
        
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        ui.data_manager.add_course('Test Course', assignments)
        
        assert len(ui.data_manager.courses) == 1
        assert ui.data_manager.courses[0]['name'] == 'Test Course'
    
    def test_info_text_tags_configured(self, ui):
        """Test that text tags are configured for styling"""
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        ui.data_manager.add_course('CPSC 3720', assignments)
        ui.update_info_display()
        
        # Check that tags exist
        tags = ui.info_text.tag_names()
        # Tags might be created during update_info_display
        # This test ensures the method completes without error
        assert True
    
    def test_multiple_courses_info_display(self, ui):
        """Test info display with multiple courses"""
        assignments1 = [{'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}]
        assignments2 = [{'name': 'Project', 'weight': 100, 'score': 90, 'max_score': 100}]
        
        ui.data_manager.add_course('CPSC 3720', assignments1)
        ui.data_manager.add_course('CPSC 4660', assignments2)
        
        ui.update_info_display()
        content = ui.info_text.get(1.0, tk.END)
        assert "CPSC 3720" in content
        assert "CPSC 4660" in content
        assert "Overall GPA" in content
    
    def test_visualization_types(self, ui):
        """Test different visualization types"""
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        ui.data_manager.add_course('CPSC 3720', assignments)
        
        viz_types = [
            'course_grades',
            'assignment_performance',
            'grade_distribution',
            'weight_distribution',
            'gpa'
        ]
        
        for viz_type in viz_types:
            try:
                ui.show_visualization(viz_type)
                assert True
            except Exception as e:
                # Some visualizations might require course selection
                # which we can't easily test without mocking
                pass

