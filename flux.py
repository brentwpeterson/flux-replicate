import tkinter as tk
from tkinter import messagebox
import replicate
import webbrowser
import csv
import logging

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

def generate_image():
    prompt = prompt_entry.get()
    logging.info("Prompt entered: %s", prompt)
    
    if not prompt:
        logging.warning("No prompt entered.")
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    input = {
        "prompt": prompt
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
        
        # Save the prompt to a CSV file
        logging.info("Saving prompt and output to CSV.")
        with open('prompts.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prompt, output])

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

# Create the main window
root = tk.Tk()
root.title("Image Generation Interface")

# Create and place the prompt label and entry
prompt_label = tk.Label(root, text="Enter your prompt:")
prompt_label.pack(pady=10)
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(pady=10)

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

# Create and place the close button
close_button = tk.Button(root, text="Close Window", command=root.quit)
close_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
