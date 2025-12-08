# GradeVision Test Suite

This directory contains comprehensive test cases for the GradeVision application.

## Test Files

- `test_data_manager.py` - Tests for DataManager class (CSV loading, saving, course management)
- `test_grade_calculator.py` - Tests for GradeCalculator class (grade calculations, GPA, predictions)
- `test_visualizer.py` - Tests for GradeVisualizer class (visualization functions)
- `test_ui_menu.py` - Tests for GradeVisionUI class (UI components and integration)

## Test Coverage

### DataManager Tests
- Initialization
- Adding courses
- Saving to CSV
- Loading from CSV
- Handling missing files
- Handling None/null scores
- Getting course names and data
- Round-trip save/load integrity

### GradeCalculator Tests
- Percentage calculations
- Course grade calculations (simple, complex, with None scores)
- Grade to GPA points conversion (all grade ranges)
- Overall GPA calculation
- Final grade prediction
- Edge cases (empty data, zero scores, etc.)

### GradeVisualizer Tests
- Percentage calculations
- All visualization plot functions
- Handling empty data
- Handling None scores
- Multiple courses scenarios

### UI Tests
- UI initialization
- Menu and toolbar creation
- Info display updates
- Visualization display
- Data manager integration
- Multiple courses handling

## Test Data

The tests use temporary files and in-memory data structures. No permanent test data files are required.

## Notes

- UI tests use `root.withdraw()` to hide windows during testing
- Visualization tests verify that plots can be created without errors
- Some UI interactions (like file dialogs) are difficult to test automatically and may require manual testing

