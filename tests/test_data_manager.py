import pytest
import pandas as pd
import os
import tempfile
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_manager import DataManager


class TestDataManager:
    """Test cases for DataManager class"""
    
    def test_init(self):
        """Test DataManager initialization"""
        dm = DataManager()
        assert dm.courses == []
    
    def test_add_course(self):
        """Test adding a course"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 30, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 70, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        assert len(dm.courses) == 1
        assert dm.courses[0]['name'] == 'CPSC 3720'
        assert len(dm.courses[0]['assignments']) == 2
        assert dm.courses[0]['assignments'][0]['name'] == 'Midterm'
    
    def test_add_multiple_courses(self):
        """Test adding multiple courses"""
        dm = DataManager()
        assignments1 = [{'name': 'Midterm', 'weight': 50, 'score': 80, 'max_score': 100}]
        assignments2 = [{'name': 'Project', 'weight': 50, 'score': 90, 'max_score': 100}]
        
        dm.add_course('Course 1', assignments1)
        dm.add_course('Course 2', assignments2)
        
        assert len(dm.courses) == 2
        assert dm.courses[0]['name'] == 'Course 1'
        assert dm.courses[1]['name'] == 'Course 2'
    
    def test_save_to_csv(self):
        """Test saving data to CSV file"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 30, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 70, 'score': 90, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
        
        try:
            dm.save_to_csv(temp_filename)
            
            # Verify file exists
            assert os.path.exists(temp_filename)
            
            # Verify file contents
            df = pd.read_csv(temp_filename)
            assert len(df) == 2
            assert 'course' in df.columns
            assert 'assignment' in df.columns
            assert 'weight' in df.columns
            assert 'score' in df.columns
            assert 'max_score' in df.columns
            assert df['course'].iloc[0] == 'CPSC 3720'
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_load_from_csv(self):
        """Test loading data from CSV file"""
        dm = DataManager()
        
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
            f.write('course,assignment,weight,score,max_score\n')
            f.write('CPSC 3720,Midterm,30,85,100\n')
            f.write('CPSC 3720,Final,70,90,100\n')
            f.write('CPSC 4660,Project,50,80,100\n')
        
        try:
            result = dm.load_from_csv(temp_filename)
            
            assert result is True
            assert len(dm.courses) == 2
            assert dm.courses[0]['name'] == 'CPSC 3720'
            assert dm.courses[1]['name'] == 'CPSC 4660'
            assert len(dm.courses[0]['assignments']) == 2
            assert len(dm.courses[1]['assignments']) == 1
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_load_from_csv_nonexistent(self):
        """Test loading from non-existent file"""
        dm = DataManager()
        result = dm.load_from_csv('nonexistent_file.csv')
        assert result is False
        assert len(dm.courses) == 0
    
    def test_load_from_csv_with_none_scores(self):
        """Test loading CSV with None/null scores"""
        dm = DataManager()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
            f.write('course,assignment,weight,score,max_score\n')
            f.write('CPSC 3720,Midterm,30,85,100\n')
            f.write('CPSC 3720,Final,70,,100\n')  # Missing score
            f.write('CPSC 3720,Project,20,None,100\n')  # None as string
        
        try:
            result = dm.load_from_csv(temp_filename)
            assert result is True
            assert len(dm.courses) == 1
            # Check that None scores are handled
            assignments = dm.courses[0]['assignments']
            assert len(assignments) == 3
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_get_course_names(self):
        """Test getting course names"""
        dm = DataManager()
        assignments = [{'name': 'Test', 'weight': 100, 'score': 80, 'max_score': 100}]
        
        dm.add_course('CPSC 3720', assignments)
        dm.add_course('CPSC 4660', assignments)
        dm.add_course('SOCI 1000', assignments)
        
        course_names = dm.get_course_names()
        assert len(course_names) == 3
        assert 'CPSC 3720' in course_names
        assert 'CPSC 4660' in course_names
        assert 'SOCI 1000' in course_names
    
    def test_get_course_names_empty(self):
        """Test getting course names when no courses exist"""
        dm = DataManager()
        course_names = dm.get_course_names()
        assert course_names == []
    
    def test_get_course_data(self):
        """Test getting course data by name"""
        dm = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 50, 'score': 85, 'max_score': 100}
        ]
        dm.add_course('CPSC 3720', assignments)
        
        course_data = dm.get_course_data('CPSC 3720')
        assert course_data is not None
        assert course_data['name'] == 'CPSC 3720'
        assert len(course_data['assignments']) == 1
    
    def test_get_course_data_nonexistent(self):
        """Test getting course data for non-existent course"""
        dm = DataManager()
        course_data = dm.get_course_data('Nonexistent Course')
        assert course_data is None
    
    def test_save_and_load_roundtrip(self):
        """Test saving and loading data maintains integrity"""
        dm1 = DataManager()
        assignments = [
            {'name': 'Midterm', 'weight': 30, 'score': 85, 'max_score': 100},
            {'name': 'Final', 'weight': 70, 'score': 90, 'max_score': 100}
        ]
        dm1.add_course('CPSC 3720', assignments)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
        
        try:
            dm1.save_to_csv(temp_filename)
            
            dm2 = DataManager()
            dm2.load_from_csv(temp_filename)
            
            assert len(dm2.courses) == len(dm1.courses)
            assert dm2.courses[0]['name'] == dm1.courses[0]['name']
            assert len(dm2.courses[0]['assignments']) == len(dm1.courses[0]['assignments'])
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

