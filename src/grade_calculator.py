class GradeCalculator:
    @staticmethod
    def _calculate_percentage(score, max_score):
        """Calculate percentage score with protection against zero division"""
        if max_score == 0:
            return 0
        return (score / max_score) * 100
    
    @staticmethod
    def calculate_course_grade(assignments):
        total_weight = 0
        weighted_score = 0
        
        for assignment in assignments:
            if assignment['score'] is not None:
                percentage = GradeCalculator._calculate_percentage(assignment['score'], assignment['max_score'])
                weighted_score += percentage * (assignment['weight'] / 100)
                total_weight += assignment['weight']
        
        if total_weight == 0:
            return 0
        
        return weighted_score / (total_weight / 100)
    
    @staticmethod
    def calculate_gpa(courses_data):
        total_grade_points = 0
        course_count = 0
        
        for course in courses_data:
            grade = GradeCalculator.calculate_course_grade(course['assignments'])
            if grade >= 0:
                grade_points = GradeCalculator._grade_to_points(grade)
                total_grade_points += grade_points
                course_count += 1
        
        return total_grade_points / course_count if course_count > 0 else 0
    
    @staticmethod
    def _grade_to_points(percentage):
        if percentage >= 90: return 4.0
        elif percentage >= 85: return 3.7
        elif percentage >= 80: return 3.3
        elif percentage >= 75: return 3.0
        elif percentage >= 70: return 2.7
        elif percentage >= 65: return 2.3
        elif percentage >= 60: return 2.0
        elif percentage >= 55: return 1.7
        elif percentage >= 50: return 1.0
        else: return 0.0
    
    @staticmethod
    def predict_final_grade(current_assignments, future_score, future_weight):
        current_grade = GradeCalculator.calculate_course_grade(current_assignments)
        current_weight = sum(assign['weight'] for assign in current_assignments if assign['score'] is not None)
        
        future_contribution = future_score * (future_weight / 100)
        current_contribution = current_grade * (current_weight / 100)
        
        return current_contribution + future_contribution



