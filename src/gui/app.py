import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from implant_detector import ImplantDetector

class ImplantDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-ray Implant Detector")
        self.root.geometry("1000x800")
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        self.upload_btn = ttk.Button(
            main_frame,
            text="Upload X-ray Image",
            command=self.upload_image
        )
        self.upload_btn.grid(row=0, column=0, pady=10)
        
        # Image display area
        self.image_frame = ttk.Frame(main_frame)
        self.image_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack()
        
        # Results text area
        self.results_text = tk.Text(main_frame, height=10, width=60)
        self.results_text.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='indeterminate'
        )
        self.progress.grid(row=3, column=0, columnspan=2, pady=10)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select X-ray Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.process_image(file_path)
            
    def process_image(self, file_path):
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Processing image...\n")
        
        try:
            # Initialize detector
            detector = ImplantDetector(file_path)
            
            # Detect implants
            implants = detector.detect_implants()
            
            if not implants:
                messagebox.showinfo("No Implants", "No implants were detected in the image.")
                return
                
            # Measure implants
            implants_data = detector.measure_implants(implants)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Implant Measurements:\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n\n")
            
            for i, measurements in enumerate(implants_data, 1):
                self.results_text.insert(tk.END, f"Implant {i}:\n")
                self.results_text.insert(tk.END, f"Width: {measurements['width']:.1f} mm\n")
                self.results_text.insert(tk.END, f"Height: {measurements['height']:.1f} mm\n")
                self.results_text.insert(tk.END, f"Diameter: {measurements['diameter']:.1f} mm\n\n")
            
            # Annotate and save image
            detector.annotate_image(implants_data)
            output_path = detector.save_annotated_image()
            
            # Display the annotated image
            self.display_image(output_path)
            
            self.results_text.insert(tk.END, f"\nAnnotated image saved as: {output_path}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
        finally:
            self.progress.stop()
            
    def display_image(self, image_path):
        # Load and resize image for display
        image = Image.open(image_path)
        # Calculate resize dimensions while maintaining aspect ratio
        display_size = (800, 600)
        image.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage for display
        photo = ImageTk.PhotoImage(image)
        
        # Update image label
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference