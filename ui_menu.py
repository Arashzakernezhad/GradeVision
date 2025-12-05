import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add src to path
sys.path.append('./src')
from data_manager import DataManager
from grade_calculator import GradeCalculator
from visualizer import GradeVisualizer

class GradeVisionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GradeVision - Grade Visualization Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.data_manager = DataManager()
        self.current_file = None
        
        # Create UI elements
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_area()
        
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load CSV File", command=self.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizations", menu=view_menu)
        view_menu.add_command(label="Course Grades", command=lambda: self.show_visualization('course_grades'))
        view_menu.add_command(label="Assignment Performance", command=lambda: self.show_visualization('assignment_performance'))
        view_menu.add_command(label="Grade Distribution", command=lambda: self.show_visualization('grade_distribution'))
        view_menu.add_command(label="Weight Distribution", command=lambda: self.show_visualization('weight_distribution'))
        view_menu.add_command(label="GPA Overview", command=lambda: self.show_visualization('gpa'))
        
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg='#e0e0e0', relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Load file button
        load_btn = tk.Button(toolbar, text="📁 Load CSV File", command=self.load_file,
                            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                            padx=10, pady=5, cursor='hand2')
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Visualization buttons
        viz_frame = tk.Frame(toolbar, bg='#e0e0e0')
        viz_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(viz_frame, text="Visualizations:", bg='#e0e0e0', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        
        viz_buttons = [
            ("📊 Course Grades", 'course_grades'),
            ("📈 Assignments", 'assignment_performance'),
            ("📉 Distribution", 'grade_distribution'),
            ("⚖️ Weights", 'weight_distribution'),
            ("🎓 GPA", 'gpa')
        ]
        
        for text, viz_type in viz_buttons:
            btn = tk.Button(viz_frame, text=text, 
                           command=lambda vt=viz_type: self.show_visualization(vt),
                           bg='#2196F3', fg='white', font=('Arial', 9),
                           padx=8, pady=5, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)
        
        # Status label
        self.status_label = tk.Label(toolbar, text="No file loaded", bg='#e0e0e0',
                                     font=('Arial', 9), fg='#666')
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
    def create_main_area(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info tab
        self.info_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.info_frame, text="📋 Information")
        self.create_info_tab()
        
        # Visualization tab
        self.viz_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.viz_frame, text="📊 Visualizations")
        self.create_viz_tab()
        
    def create_info_tab(self):
        # Scrollable text area
        scrollbar = tk.Scrollbar(self.info_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(self.info_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                                 font=('Consolas', 10), bg='#fafafa', padx=10, pady=10)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.info_text.yview)
        
        # Initial message
        self.update_info_display()
        
    def create_viz_tab(self):
        self.viz_canvas_frame = tk.Frame(self.viz_frame, bg='white')
        self.viz_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        initial_label = tk.Label(self.viz_canvas_frame, 
                                text="Load a CSV file to view visualizations",
                                font=('Arial', 14), bg='white', fg='#666')
        initial_label.pack(expand=True)
        
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data_manager = DataManager()
                success = self.data_manager.load_from_csv(file_path)
                
                if success:
                    self.current_file = file_path
                    self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}", fg='green')
                    self.update_info_display()
                    messagebox.showinfo("Success", f"File loaded successfully!\n{len(self.data_manager.courses)} course(s) found.")
                else:
                    messagebox.showerror("Error", "Failed to load file. Please check the file format.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file:\n{str(e)}")
    
    def update_info_display(self):
        self.info_text.delete(1.0, tk.END)
        
        if not self.data_manager.courses:
            self.info_text.insert(tk.END, "No data loaded. Please load a CSV file.\n\n")
            self.info_text.insert(tk.END, "Expected CSV format:\n")
            self.info_text.insert(tk.END, "course,assignment,weight,score,max_score\n")
            self.info_text.insert(tk.END, "CPSC 3720,Midterm 1,25,85,100\n")
            return
        
        # Display course information
        self.info_text.insert(tk.END, "=" * 60 + "\n")
        self.info_text.insert(tk.END, "GRADE INFORMATION\n")
        self.info_text.insert(tk.END, "=" * 60 + "\n\n")
        
        for course in self.data_manager.courses:
            course_name = course['name']
            assignments = course['assignments']
            grade = GradeCalculator.calculate_course_grade(assignments)
            
            self.info_text.insert(tk.END, f"Course: {course_name}\n", 'heading')
            self.info_text.insert(tk.END, f"Current Grade: {grade:.2f}%\n\n")
            
            self.info_text.insert(tk.END, "Assignments:\n", 'subheading')
            self.info_text.insert(tk.END, "-" * 60 + "\n")
            
            for assignment in assignments:
                if assignment['score'] is not None:
                    percentage = GradeVisualizer.calculate_percentage(assignment['score'], assignment['max_score'])
                    self.info_text.insert(tk.END, 
                        f"  {assignment['name']:30s} "
                        f"Weight: {assignment['weight']:5.1f}%  "
                        f"Score: {assignment['score']:5.1f}/{assignment['max_score']:5.1f}  "
                        f"({percentage:5.1f}%)\n")
                else:
                    self.info_text.insert(tk.END, 
                        f"  {assignment['name']:30s} "
                        f"Weight: {assignment['weight']:5.1f}%  "
                        f"Score: Not yet graded\n")
            
            self.info_text.insert(tk.END, "\n")
        
        # Overall GPA
        gpa = GradeCalculator.calculate_gpa(self.data_manager.courses)
        self.info_text.insert(tk.END, "=" * 60 + "\n")
        self.info_text.insert(tk.END, f"Overall GPA: {gpa:.2f}\n", 'gpa')
        self.info_text.insert(tk.END, "=" * 60 + "\n")
        
        # Configure text tags for styling
        self.info_text.tag_config('heading', font=('Consolas', 12, 'bold'), foreground='#2E86AB')
        self.info_text.tag_config('subheading', font=('Consolas', 10, 'bold'), foreground='#A23B72')
        self.info_text.tag_config('gpa', font=('Consolas', 12, 'bold'), foreground='#06A77D')
    
    def show_visualization(self, viz_type):
        if not self.data_manager.courses:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # Clear previous visualization
        plt.close('all')
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        
        try:
            if viz_type == 'course_grades':
                GradeVisualizer.plot_course_grades(self.data_manager, fig)
            elif viz_type == 'assignment_performance':
                # Ask for course selection if multiple courses
                if len(self.data_manager.courses) > 1:
                    course_name = self.select_course()
                    if course_name:
                        GradeVisualizer.plot_assignment_performance(self.data_manager, course_name, fig)
                    else:
                        GradeVisualizer.plot_assignment_performance(self.data_manager, None, fig)
                else:
                    GradeVisualizer.plot_assignment_performance(self.data_manager, None, fig)
            elif viz_type == 'grade_distribution':
                GradeVisualizer.plot_grade_distribution(self.data_manager, fig)
            elif viz_type == 'weight_distribution':
                # Ask for course selection if multiple courses
                course_name = None
                if len(self.data_manager.courses) > 1:
                    course_name = self.select_course()
                    if course_name == "CANCEL":
                        return

                GradeVisualizer.plot_assignment_performance(self.data_manager, course_name, fig)
            elif viz_type == 'gpa':
                GradeVisualizer.plot_gpa_trend(self.data_manager, fig)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Switch to visualization tab
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating visualization:\n{str(e)}")
    
    def select_course(self):
        course_names = self.data_manager.get_course_names()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Course")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = ["CANCEL"]
        
        tk.Label(dialog, text="Select a course:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        listbox = tk.Listbox(dialog, font=('Arial', 10), height=6)
        listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        for course_name in course_names:
            listbox.insert(tk.END, course_name)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                result[0] = course_names[selection[0]]
            dialog.destroy()
        
        def on_all():
            result[0] = None
            dialog.destroy()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Select", command=on_select,
                 bg='#4CAF50', fg='white', padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="All Courses", command=on_all,
                 bg='#2196F3', fg='white', padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#f44336', fg='white', padx=10).pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()
        return result[0]

def main():
    root = tk.Tk()
    app = GradeVisionUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

