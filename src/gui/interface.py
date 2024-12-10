import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

class XrayAnalyzerGUI:
    def __init__(self, root, process_callback):
        self.root = root
        self.process_callback = process_callback
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI interface"""
        self.root.title("X-ray Implant Analyzer")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        upload_btn = ttk.Button(
            main_frame,
            text="Upload X-ray Image",
            command=self.upload_image
        )
        upload_btn.grid(row=0, column=0, pady=10)
        
        # Results text area
        self.results_text = tk.Text(main_frame, height=10, width=50)
        self.results_text.grid(row=1, column=0, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='indeterminate'
        )
        self.progress.grid(row=2, column=0, pady=10)
        
    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.process_image(file_path)
            
    def process_image(self, file_path):
        """Process the uploaded image"""
        self.progress.start()
        try:
            results = self.process_callback(file_path)
            if results:
                self.display_results(results)
            else:
                messagebox.showinfo(
                    "No Implants Found",
                    "No implants were detected in the image."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
        finally:
            self.progress.stop()
            
    def display_results(self, results):
        """Display processing results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Processing Results:\n\n")
        
        for output in results:
            self.results_text.insert(tk.END, output + "\n\n")