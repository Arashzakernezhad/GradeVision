import pandas as pd
import json
import os

class DataManager:
    def __init__(self):
        self.courses = []
    
    def add_course(self, course_name, assignments):
        course = {
            'name': course_name,
            'assignments': assignments
        }
        self.courses.append(course)
    
    def save_to_csv(self, filename='grade_data.csv'):
        data = []
        for course in self.courses:
            for assignment in course['assignments']:
                data.append({
                    'course': course['name'],
                    'assignment': assignment['name'],
                    'weight': assignment['weight'],
                    'score': assignment['score'],
                    'max_score': assignment['max_score']
                })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def load_from_csv(self, filename='grade_data.csv'):
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            self.courses = []
            
            for course_name in df['course'].unique():
                course_data = df[df['course'] == course_name]
                assignments = []
                
                for _, row in course_data.iterrows():
                    assignments.append({
                        'name': row['assignment'],
                        'weight': row['weight'],
                        'score': row['score'],
                        'max_score': row['max_score']
                    })
                
                self.add_course(course_name, assignments)
            print(f"Data loaded from {filename}")
            return True
        else:
            print(f"File {filename} not found")
            return False
    
    def get_course_names(self):
        return [course['name'] for course in self.courses]
    
    def get_course_data(self, course_name):
        for course in self.courses:
            if course['name'] == course_name:
                return course
        return None


