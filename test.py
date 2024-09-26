import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Class to represent each layer
class Layer:
    def __init__(self, name, visible=True):
        self.name = name
        self.visible = visible

# Main Application class
class PhotopeaClone:
    def __init__(self, root):
        self.root = root
        self.root.title("Photopea Clone")

        # Menu for loading images
        self.create_menu()

        # Create the layout
        self.create_layout()

        # Initialize layer list
        self.layers = []

    # Create the Menu Bar
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    # Create the main layout for the GUI
    def create_layout(self):
        # Left Frame for Image Display
        self.canvas_frame = tk.Frame(self.root, width=600, height=400, bg='gray')
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=500, height=400)
        self.canvas.pack()

        # Right Frame for Layer Panel
        self.layer_frame = tk.Frame(self.root, width=200, height=400, bg='lightgray')
        self.layer_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.layer_title = tk.Label(self.layer_frame, text="Layers", font=("Arial", 12, "bold"))
        self.layer_title.pack(pady=5)

        # Frame inside for the layers
        self.layer_list_frame = tk.Frame(self.layer_frame, bg="white")
        self.layer_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Add layer button
        self.add_layer_button = tk.Button(self.layer_frame, text="Add Layer", command=self.add_layer)
        self.add_layer_button.pack(pady=5)

    # Function to load the image
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.tiff;*.psd")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

            # Add a base layer (mock for now)
            self.add_layer(name=os.path.basename(file_path))

    # Function to display the image on canvas
    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image.resize((500, 400)))
        self.canvas.create_image(250, 200, image=self.tk_image)

    # Add a new layer
    def add_layer(self, name="Layer"):
        new_layer = Layer(name=name)
        self.layers.append(new_layer)
        self.update_layer_list()

    # Update the layer list UI
    def update_layer_list(self):
        for widget in self.layer_list_frame.winfo_children():
            widget.destroy()

        for index, layer in enumerate(self.layers):
            frame = tk.Frame(self.layer_list_frame, bg="white", padx=5, pady=5)
            frame.pack(fill=tk.X)

            # Checkbutton for visibility
            var = tk.BooleanVar(value=layer.visible)
            check = tk.Checkbutton(frame, variable=var, command=lambda i=index, v=var: self.toggle_visibility(i, v))
            check.pack(side=tk.LEFT)

            # Label for layer name
            label = tk.Label(frame, text=layer.name)
            label.pack(side=tk.LEFT, padx=5)

    # Toggle layer visibility
    def toggle_visibility(self, index, var):
        self.layers[index].visible = var.get()
        messagebox.showinfo("Info", f"Layer '{self.layers[index].name}' visibility: {self.layers[index].visible}")

    # Function to save the image
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path and self.image:
            self.image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotopeaClone(root)
    root.mainloop()



#-------------------------------------------------


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Class to represent each layer
class Layer:
    def __init__(self, name, image, visible=True):
        self.name = name
        self.image = image
        self.visible = visible

# Main Application class
class PhotopeaClone:
    def __init__(self, root):
        self.root = root
        self.root.title("Photopea Clone")

        # Menu for loading images
        self.create_menu()

        # Create the layout
        self.create_layout()

        # Initialize layer list
        self.layers = []

    # Create the Menu Bar
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_tiff_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    # Create the main layout for the GUI
    def create_layout(self):
        # Left Frame for Image Display
        self.canvas_frame = tk.Frame(self.root, width=600, height=400, bg='gray')
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=500, height=400)
        self.canvas.pack()

        # Right Frame for Layer Panel
        self.layer_frame = tk.Frame(self.root, width=200, height=400, bg='lightgray')
        self.layer_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.layer_title = tk.Label(self.layer_frame, text="Layers", font=("Arial", 12, "bold"))
        self.layer_title.pack(pady=5)

        # Frame inside for the layers
        self.layer_list_frame = tk.Frame(self.layer_frame, bg="white")
        self.layer_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Add layer button
        self.add_layer_button = tk.Button(self.layer_frame, text="Add Layer", command=self.add_layer)
        self.add_layer_button.pack(pady=5)

    # Function to load the TIFF image and break into layers
    def load_tiff_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])
        if file_path:
            tiff_image = Image.open(file_path)

            # Extract layers/pages from the TIFF file
            self.layers = []  # Clear existing layers
            try:
                for i in range(tiff_image.n_frames):  # Iterate through the pages/layers
                    tiff_image.seek(i)
                    layer_image = tiff_image.copy()
                    layer_name = f"Layer {i+1}"
                    self.add_layer(name=layer_name, image=layer_image)
            except EOFError:
                pass

            self.display_image(self.layers[0].image)  # Display the first layer initially

    # Function to display the selected layer image
    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image.resize((500, 400)))
        self.canvas.create_image(250, 200, image=self.tk_image)

    # Add a new layer
    def add_layer(self, name="Layer", image=None):
        if image is None:
            # Create a blank image if no image is provided
            image = Image.new('RGBA', (500, 400), (255, 255, 255, 0))  
        new_layer = Layer(name=name, image=image)
        self.layers.append(new_layer)
        self.update_layer_list()

    # Update the layer list UI
    def update_layer_list(self):
        for widget in self.layer_list_frame.winfo_children():
            widget.destroy()

        for index, layer in enumerate(self.layers):
            frame = tk.Frame(self.layer_list_frame, bg="white", padx=5, pady=5)
            frame.pack(fill=tk.X)

            # Checkbutton for visibility
            var = tk.BooleanVar(value=layer.visible)
            check = tk.Checkbutton(frame, variable=var, command=lambda i=index, v=var: self.toggle_visibility(i, v))
            check.pack(side=tk.LEFT)

            # Label for layer name
            label = tk.Label(frame, text=layer.name)
            label.pack(side=tk.LEFT, padx=5)

            # Button to display the layer
            display_button = tk.Button(frame, text="Show", command=lambda i=index: self.display_image(self.layers[i].image))
            display_button.pack(side=tk.RIGHT)

    # Toggle layer visibility
    def toggle_visibility(self, index, var):
        self.layers[index].visible = var.get()
        messagebox.showinfo("Info", f"Layer '{self.layers[index].name}' visibility: {self.layers[index].visible}")

    # Function to save the image
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path and self.layers:
            # Merge visible layers and save
            base_image = self.layers[0].image.copy()
            for layer in self.layers[1:]:
                if layer.visible:
                    base_image.paste(layer.image, (0, 0), layer.image)  # Paste with transparency
            base_image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotopeaClone(root)
    root.mainloop()
