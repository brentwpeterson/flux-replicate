import tkinter as tk
from tkinter import messagebox
import replicate
import webbrowser
import csv
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='image_generation.log', filemode='w')

def read_last_prompt():
    try:
        with open('prompts.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                last_prompt = rows[-1][0]
                return last_prompt
            else:
                return ""
    except FileNotFoundError:
        return ""

def read_last_output_url():
    try:
        with open('output_urls.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                last_output_url = rows[-1][0]
                return last_output_url
            else:
                return ""
    except FileNotFoundError:
        return ""

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Download Complete", f"Image downloaded as {filename}")
    except Exception as e:
        logging.error("An error occurred while downloading the image: %s", e)
        messagebox.showerror("Error", f"An error occurred while downloading the image: {e}")

def generate_image():
    prompt = prompt_entry.get()
    aspect_ratio = aspect_ratio_entry.get()
    logging.info("Prompt entered: %s", prompt)
    logging.info("Aspect ratio entered: %s", aspect_ratio)
    
    if not prompt:
        logging.warning("No prompt entered.")
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    input = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio
    }

    try:
        logging.info("Sending request to replicate.run with input: %s", input)
        output = replicate.run(
            "black-forest-labs/flux-pro",
            input=input
        )
        logging.info("Received output: %s", output)

        output_entry.config(state='normal')
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output)
        output_entry.config(state='readonly')
        
        # Save the prompt to prompts.csv
        logging.info("Saving prompt to prompts.csv.")
        with open('prompts.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prompt])
        
        # Save the output URL to output_urls.csv
        logging.info("Saving output URL to output_urls.csv.")
        with open('output_urls.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([output])
        
        # Open the image URL in a web browser
        logging.info("Opening web browser with URL: %s", output)
        webbrowser.open(output)
        
    except Exception as e:
        logging.error("An error occurred: %s", e)
        messagebox.showerror("Error", f"An error occurred: {e}")

def use_last_prompt():
    last_prompt = read_last_prompt()
    if last_prompt:
        prompt_entry.delete(0, tk.END)
        prompt_entry.insert(0, last_prompt)
    else:
        messagebox.showinfo("Info", "No previous prompt found.")

def download_last_image():
    last_output_url = read_last_output_url()
    if last_output_url:
        download_image(last_output_url, "last_generated_image.png")
    else:
        messagebox.showinfo("Info", "No previous output URL found.")

# Create the main window
root = tk.Tk()
root.title("Image Generation Interface")

# Create and place the prompt label and entry
prompt_label = tk.Label(root, text="Enter your prompt:")
prompt_label.pack(pady=10)
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(pady=10)

# Create and place the aspect ratio label and entry
aspect_ratio_label = tk.Label(root, text="Enter aspect ratio (e.g., 16:9):")
aspect_ratio_label.pack(pady=10)
aspect_ratio_entry = tk.Entry(root, width=20)
aspect_ratio_entry.pack(pady=10)

# Create and place the generate button
generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=10)

# Create and place the use last prompt button
use_last_prompt_button = tk.Button(root, text="Use Last Prompt", command=use_last_prompt)
use_last_prompt_button.pack(pady=10)

# Create and place the output label
output_label = tk.Label(root, text="Output URL:")
output_label.pack(pady=10)

# Create and place the output entry
output_entry = tk.Entry(root, width=80)
output_entry.pack(pady=10)
output_entry.config(state='readonly')

# Create and place the download last image button
download_last_image_button = tk.Button(root, text="Download Last Created Image", command=download_last_image)
download_last_image_button.pack(pady=10)

# Create and place the close button
close_button = tk.Button(root, text="Close Window", command=root.quit)
close_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
