import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, colorchooser  # Import colorchooser module
from PIL import Image, ImageTk
import os

class DesktopDuck:
    def __init__(self, master, image_paths, intervals):
        self.master = master
        self.prev_x = 0
        self.prev_y = 0
        self.image_paths = image_paths
        self.photos = [ImageTk.PhotoImage(Image.open(image)) for image in self.image_paths]
        self.intervals = intervals
        self.current_image_index = 0
        self.notes = []  # Change tasks to notes
        self.note_labels = []  # Initialize note_labels attribute
        self.note_colors = []  # Initialize note_colors attribute
        
        self.label = tk.Label(master, bg='black')
        self.label.pack()
        
        self.update_image()
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        image_width, image_height = self.photos[0].width(), self.photos[0].height()
        x = screen_width - image_width - 300  # Adjusted to be 100 pixels from the right side
        y = screen_height - image_height - 100  # Adjusted to be 100 pixels from the bottom
        
        initial_width = image_width + 400  # Add extra width
        initial_height = image_height + 300  # Add extra height
        
        self.master.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
        self.master.overrideredirect(True)
        self.master.attributes('-transparentcolor', 'black')
        self.master.attributes('-topmost', True)
        self.master.config(bg='black')  # Set background color to black
        
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Add a note", command=self.add_note)  # Change task to note
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Close", command=self.close_window)
        
        self.label.bind("<Button-3>", self.show_context_menu)
        self.label.bind("<ButtonPress-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)
        
        self.rotate_images()
        
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
        
    def close_window(self):
        self.master.destroy()
        
    def add_note(self):
        if len(self.notes) < 10:
            note = simpledialog.askstring("Add a Note", "Enter note description (max 50 characters):")
            if note:
                self.notes.append(note)
                self.note_colors.append('black')  # Default color is black
                self.update_notes_display()
        else:
            messagebox.showerror("Quack!", "You have too many notes already for this little duck to carry!")
            
    def remove_note(self, note_index):
        del self.notes[note_index]
        del self.note_colors[note_index]
        self.update_notes_display()
        
    def copy_note(self, note_index):  # New method to copy note
        note_to_copy = self.notes[note_index]
        self.master.clipboard_clear()
        self.master.clipboard_append(note_to_copy)
        
    def edit_note(self, index):
        edited_note = simpledialog.askstring("Edit Note", "Edit note description:", initialvalue=self.notes[index])
        if edited_note:
            self.notes[index] = edited_note
            self.update_notes_display()
            
    def change_note_color(self, index):
        color = colorchooser.askcolor(title="Choose Color")  # Open color picker dialog
        if color[1]:  # Check if a color is chosen
            self.note_colors[index] = color[1]
            self.update_notes_display()
        
    def update_notes_display(self):
        # Clear existing note labels
        for label in self.note_labels:
            label.destroy()
        
        # Create new note labels
        self.note_labels = []
        for i, (note, color) in enumerate(zip(self.notes, self.note_colors)):
            note_label = tk.Label(self.master, text=note, bg='white', fg=color)  # Set text color
            y_position = 120 + i * 23  # Adjusted to add 3 pixels of space between each note
            note_label.place(relx=0.5, y=y_position, anchor=tk.CENTER)  # Center horizontally
            note_label.bind("<Button-3>", lambda event, index=i: self.show_note_menu(event, index))
            self.note_labels.append(note_label)
        
    def show_note_menu(self, event, index):
        note_menu = tk.Menu(self.master, tearoff=0)
        note_menu.add_command(label="Edit", command=lambda: self.edit_note(index))  # Add edit option
        note_menu.add_command(label="Copy", command=lambda: self.copy_note(index))  # Add copy option
        note_menu.add_command(label="Change Color", command=lambda: self.change_note_color(index))  # Add color option
        note_menu.add_command(label="Delete", command=lambda: self.remove_note(index))  # Change Completed to Delete
        note_menu.post(event.x_root, event.y_root)
        
    def on_drag_start(self, event):
        self.prev_x = event.x_root
        self.prev_y = event.y_root
        
    def on_drag_motion(self, event):
        deltax = event.x_root - self.prev_x
        deltay = event.y_root - self.prev_y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")
        self.prev_x = event.x_root
        self.prev_y = event.y_root
    
    def update_image(self):
        self.label.configure(image=self.photos[self.current_image_index])
        
    def rotate_images(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.photos)
        self.update_image()
        interval = self.intervals[self.current_image_index]  # Get the interval for the current image
        self.master.after(interval, self.rotate_images)

def main():
    root = tk.Tk()
    root.title("Desktop Duck")
    
    image_paths = [
        os.path.join(os.getcwd(), 'duck1.png'),
        os.path.join(os.getcwd(), 'duck2.png'),
        os.path.join(os.getcwd(), 'duck3.png'),
        os.path.join(os.getcwd(), 'duck4.png'),
        os.path.join(os.getcwd(), 'duck5.png')
    ]
    
    # Set intervals for each image rotation (in milliseconds)
    intervals = [700, 100, 100, 100, 100]  # Adjust as needed
    
    pet = DesktopDuck(root, image_paths, intervals)
    
    root.mainloop()

if __name__ == "__main__":
    main()