import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

"""
    WD: Converts a scanned PDF file into text using OCR.
    
    This function uses pdf2image to convert the PDF pages into images and then applies 
    pytesseract OCR to extract text from each image. The extracted text from all pages is 
    combined into a single string and returned.
    """
def pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path, 300)
    full_text = ""
    
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    
    return full_text

"""
    WD: Saves extracted text into a new PDF file.
    
    This function creates a new PDF file and writes the provided text into it using the 
    ReportLab library. Each line of text is added to the PDF, and the document is saved 
    at the specified path.
    """
def save_text_to_pdf(text, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    text_object = c.beginText(40, height - 40)
    
    for line in text.split('\n'):
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()

"""
    WD: Handles PDF extraction and conversion in the CustomTkinter GUI.
    
    This function triggers the process of selecting a PDF file, extracting text from it 
    using OCR, and then saving the extracted text as a new PDF. It also updates the GUI 
    to show the extracted text and prompts the user to save the output as a new PDF file. 
    Error handling is included in case of failures during the extraction process.
    """
def extract_pdf():
    extract_button.configure(state="disabled")
    
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        extract_button.configure(state="normal")
        return
    
    try:
        extracted_text = pdf_to_text(pdf_path)
        
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, extracted_text)
        placeholder_label.place_forget()
        
        save_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if save_pdf_path:
            save_text_to_pdf(extracted_text, save_pdf_path)
            messagebox.showinfo("Success", f"Extracted text saved to: {save_pdf_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    extract_button.configure(state="normal")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("PDF to Editable Text with OCR")
root.geometry("600x500")

frame = ctk.CTkFrame(root, fg_color="#E0E0E0")
frame.pack(padx=20, pady=20, fill="both", expand=True)

extract_button = ctk.CTkButton(frame, text="Choose a Scanned PDF", fg_color="black", text_color="white", command=extract_pdf, height=40)
extract_button.pack(pady=10)

text_box = ctk.CTkTextbox(frame, wrap="word", width=550, height=200)
text_box.pack(pady=10)

placeholder_label = ctk.CTkLabel(frame, text="OUTPUT WILL BE HERE", font=("Times New Roman", 24, "bold"), text_color="gray")
placeholder_label.place(in_=text_box, relx=0.5, rely=0.5, anchor="center")

def on_text_change(event):
    if text_box.get("1.0", "end-1c").strip():
        placeholder_label.place_forget()
    else:
        placeholder_label.place(in_=text_box, relx=0.5, rely=0.5, anchor="center")  # Show placeholder if empty

text_box.bind("<KeyRelease>", on_text_change)

credit_label = ctk.CTkLabel(root, text="Made by Wadie Coder © " + str(datetime.now().year), text_color="blue", cursor="hand2")
credit_label.pack(side="bottom", pady=10)

root.mainloop()
