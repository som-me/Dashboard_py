import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class TiffLayerEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("TIFF Layer Editor")
        self.root.geometry("1000x700")
        
        # Initialize layers and other variables
        self.layers = []  # List to hold layer images as NumPy arrays
        self.layer_tk_images = []  # To display images on the GUI
        self.selected_layer_index = None
        
        # Set up the layout
        self.create_layout()

    def create_layout(self):
        # Create a frame for control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Button to load TIFF file
        load_button = tk.Button(control_frame, text="Load TIFF", command=self.load_tiff_file)
        load_button.pack(pady=5)

        # Layer selection list
        self.layer_listbox = tk.Listbox(control_frame, height=10)
        self.layer_listbox.pack(pady=5)
        self.layer_listbox.bind("<<ListboxSelect>>", self.on_layer_select)
        
        # Buttons for image modifications
        color_button = tk.Button(control_frame, text="Change Color", command=self.change_layer_color)
        color_button.pack(pady=5)
        
        texture_button = tk.Button(control_frame, text="Apply Texture", command=self.apply_texture)
        texture_button.pack(pady=5)

        # Save button
        save_button = tk.Button(control_frame, text="Save TIFF", command=self.save_tiff)
        save_button.pack(pady=5)

        # Canvas to display the selected layer
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="gray")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def load_tiff_file(self):
        # Open file dialog to load a TIFF file
        file_path = filedialog.askopenfilename(title="Select TIFF File", filetypes=[("TIFF Files", "*.tiff *.tif")])
        if not file_path:
            return

        # Open TIFF image using Pillow
        tiff_image = Image.open(file_path)

        # Extract all layers (TIFF pages) and store them in NumPy arrays
        self.layers = []
        try:
            for i in range(tiff_image.n_frames):
                tiff_image.seek(i)
                # Convert to a format suitable for OpenCV (RGB)
                layer = np.array(tiff_image.convert("RGBA"))
                self.layers.append(layer)
        except EOFError:
            pass

        # Reset the listbox and canvas
        self.layer_listbox.delete(0, tk.END)
        self.canvas.delete("all")

        # Populate the listbox with layers
        for i in range(len(self.layers)):
            self.layer_listbox.insert(tk.END, f"Layer {i + 1}")

    def on_layer_select(self, event):
        # Get the selected layer index
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_layer_index = index
            self.display_layer(index)

    def display_layer(self, layer_index):
        if layer_index is None:
            return
        
        # Get the selected layer image
        layer_image = self.layers[layer_index]
        
        # Convert the NumPy array to ImageTk format for display in Tkinter
        image_pil = Image.fromarray(layer_image)
        image_tk = ImageTk.PhotoImage(image_pil)

        # Clear the canvas and display the image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image = image_tk  # Keep a reference to avoid garbage collection

    def change_layer_color(self):
        if self.selected_layer_index is None:
            messagebox.showwarning("No Layer Selected", "Please select a layer first!")
            return

        # Ask the user for a color using colorchooser
        color = colorchooser.askcolor()[1]
        if color:
            # Convert hex color to RGB tuple
            color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
            # Get the selected layer
            layer = self.layers[self.selected_layer_index]
            
            # Apply the color overlay (blend with the original image)
            colored_layer = self.apply_color_overlay(layer, color_rgb)
            
            # Update the layer with the new colored version
            self.layers[self.selected_layer_index] = colored_layer
            
            # Refresh the display
            self.display_layer(self.selected_layer_index)

    def apply_color_overlay(self, image, color_rgb):
        """ Apply a color overlay to the layer using OpenCV. """
        overlay = np.full_like(image[:, :, :3], color_rgb, dtype=np.uint8)  # Ignore the alpha channel
        blended_image = cv2.addWeighted(overlay, 0.5, image[:, :, :3], 0.5, 0)
        result = np.dstack((blended_image, image[:, :, 3]))  # Add back the alpha channel
        return result

    def apply_texture(self):
        if self.selected_layer_index is None:
            messagebox.showwarning("No Layer Selected", "Please select a layer first!")
            return

        # Get the selected layer
        layer = self.layers[self.selected_layer_index]

        # Apply a simple texture effect (e.g., embossing)
        texture = self.apply_emboss_filter(layer[:, :, :3])
        
        # Combine the processed image with the alpha channel
        textured_layer = np.dstack((texture, layer[:, :, 3]))

        # Update the layer with the textured version
        self.layers[self.selected_layer_index] = textured_layer
        
        # Refresh the display
        self.display_layer(self.selected_layer_index)

    def apply_emboss_filter(self, image):
        """ Apply an emboss filter to the layer using OpenCV. """
        kernel = np.array([[2, 0, 0], [0, -1, 0], [0, 0, -1]])
        embossed_image = cv2.filter2D(image, -1, kernel)
        return embossed_image

    def save_tiff(self):
        # Open file dialog to save the TIFF file
        file_path = filedialog.asksaveasfilename(defaultextension=".tiff", filetypes=[("TIFF Files", "*.tiff *.tif")])
        if not file_path:
            return

        # Convert each layer back to Pillow images
        pil_layers = [Image.fromarray(layer) for layer in self.layers]

        # Save the layers as a multi-page TIFF
        pil_layers[0].save(file_path, save_all=True, append_images=pil_layers[1:])

        messagebox.showinfo("Saved", "Your TIFF file has been saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiffLayerEditor(root)
    root.mainloop()
