import tkinter as tk  # Import the Tkinter module for creating GUI applications
from tkinter import messagebox, filedialog  # Import messagebox and filedialog for dialog windows
import os  # Import the os module for interacting with the operating system
from PIL import Image, ImageTk  # Import Image and ImageTk from the PIL module for handling images
import traceback  # Import traceback for detailed error information

# Custom exceptions
class FriendNotFoundException(Exception):
    pass

class InvalidFileFormatException(Exception):
    pass

# Function to display the list of friends in the container
def show_friends(container):
    try:
        # Clear the container of any existing widgets
        for widget in container.winfo_children():
            widget.destroy()

        # Loop through the files in the friends folder
        for filename in os.listdir(friends_folder):
            # Check if the file is an image
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                friend_name = os.path.splitext(filename)[0]  # Get the friend name without extension
                image_path = os.path.join(friends_folder, filename)  # Get the full image path
                img = Image.open(image_path)  # Open the image
                img = img.resize((100, 100))  # Resize the image to 100x100 pixels
                img = ImageTk.PhotoImage(img)  # Convert the image to PhotoImage
                # Create a button with the friend's image and name
                friend_button = tk.Button(container, image=img, text=friend_name, compound='top',
                                          command=lambda path=image_path, name=friend_name: show_friend(container, path, name))
                friend_button.image = img  # Keep a reference to the image to prevent garbage collection
                friend_button.pack(side='left')  # Pack the button to the left
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to display the details of a selected friend
def show_friend(parent, image_path, friend_name):
    try:
        if not os.path.exists(image_path):
            raise FriendNotFoundException(f"Friend image not found: {friend_name}")

        # Create a new top-level window for the friend's portrait
        portrait_window = tk.Toplevel(parent)
        portrait_window.title(friend_name)  # Set the window title to the friend's name
        portrait_window.geometry("1300x950")  # Set the window size
        portrait_window.configure(bg='lightgreen')  # Set the background color

        img = Image.open(image_path)  # Open the image
        img = img.resize((300, 300))  # Resize the image to 300x300 pixels
        img = ImageTk.PhotoImage(img)  # Convert the image to PhotoImage
        img_label = tk.Label(portrait_window, image=img)  # Create a label with the image
        img_label.image = img  # Keep a reference to the image to prevent garbage collection
        img_label.pack()  # Pack the label

        menu_frame = tk.Frame(portrait_window)  # Create a frame for the menu buttons
        menu_frame.pack(side=tk.TOP, pady=10)  # Pack the frame to the top with padding

        gallery_frame = tk.Frame(portrait_window, bg='lightgreen')  # Create a frame for the friend's friends gallery
        gallery_frame.pack(side=tk.TOP, pady=10)  # Pack the frame to the top with padding

        # Create a folder for the friend's friends if it doesn't exist
        friend_folder = os.path.join(friends_folder, friend_name)
        if not os.path.exists(friend_folder):
            os.makedirs(friend_folder)

        # Function to display the friends of the selected friend
        def show_friends_of_friend():
            try:
                # Clear the gallery frame of any existing widgets
                for widget in gallery_frame.winfo_children():
                    widget.destroy()
                
                # Loop through the files in the friend's friends folder
                for filename in os.listdir(friend_folder):
                    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        friend_name_of_friend = os.path.splitext(filename)[0]  # Get the friend's friend's name
                        image_path = os.path.join(friend_folder, filename)  # Get the full image path
                        img = Image.open(image_path)  # Open the image
                        img = img.resize((100, 100))  # Resize the image to 100x100 pixels
                        img = ImageTk.PhotoImage(img)  # Convert the image to PhotoImage
                        # Create a button with the friend's friend's image and name
                        friend_button = tk.Button(gallery_frame, image=img, text=friend_name_of_friend, compound='top',
                                                  command=lambda path=image_path, name=friend_name_of_friend: show_friend(portrait_window, path, name))
                        friend_button.image = img  # Keep a reference to the image to prevent garbage collection
                        friend_button.pack(side='left')  # Pack the button to the left
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                traceback.print_exc()

        # Create buttons in the new friend window
        create_rounded_button(menu_frame, "Show Friends", show_friends_of_friend, "lightblue", "red")
        create_rounded_button(menu_frame, "Clear All", lambda: clear_all(gallery_frame), "yellow", "black")
        create_rounded_button(menu_frame, "Delete a Friend", lambda: delete_friend(gallery_frame, friend_folder), "pink", "black")
        create_rounded_button(menu_frame, "Add New Friend", lambda: add_new_friend(gallery_frame, friend_folder), "white", "black")
        create_rounded_button(menu_frame, "Quit", portrait_window.destroy, "lightblue", "black")
    except FriendNotFoundException as fnfe:
        messagebox.showerror("Error", str(fnfe))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to clear all widgets in the container
def clear_all(container):
    try:
        # Check if there are any widgets in the container
        if not container.winfo_children():
            messagebox.showinfo("Information", "No need to clear as nothing is displayed")
        else:
            # Destroy all widgets in the container
            for widget in container.winfo_children():
                widget.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to delete a friend
def delete_friend(container, folder):
    try:
        # Open a file dialog to select a file to delete
        file_path = filedialog.askopenfilename(initialdir=folder, title="Select a file to delete")
        if file_path:
            file_name = os.path.basename(file_path)  # Get the file name
            # Ask for confirmation to delete the file
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {file_name}?")
            if confirm:
                os.remove(file_path)  # Delete the file
                show_friends(container)  # Refresh the friends list
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to add a new friend
def add_new_friend(container, folder):
    try:
        # Open a file dialog to select a file to add
        file_path = filedialog.askopenfilename(title="Select a file to add")
        if file_path:
            if not file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise InvalidFileFormatException("Invalid file format. Please select an image file.")
            
            dest_path = os.path.join(folder, os.path.basename(file_path))  # Get the destination path
            # Ask for confirmation to add the file
            confirm = messagebox.askyesno("Confirm Addition", f"Are you sure you want to add {os.path.basename(file_path)}?")
            if confirm:
                os.rename(file_path, dest_path)  # Move the file to the friends folder
                show_friends(container)  # Refresh the friends list
    except InvalidFileFormatException as iffe:
        messagebox.showerror("Error", str(iffe))
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to quit the application
def quit_app():
    try:
        # Ask for confirmation to quit the application
        confirm = messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?")
        if confirm:
            root.quit()  # Quit the application
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Function to create a button with rounded corners
def create_rounded_button(container, text, command, bg_color, fg_color):
    try:
        # Create a canvas for drawing the rounded button
        canvas = tk.Canvas(container, width=120, height=50, bg=bg_color, highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=10, pady=10)  # Pack the canvas to the left with padding
        # Draw an oval shape for the rounded button
        canvas.create_oval(10, 10, 110, 40, fill=bg_color, outline=bg_color)
        # Bind the button click event to the command
        canvas.bind("<Button-1>", lambda event: command())
        # Create a label for the button text
        label = tk.Label(container, text=text, bg=bg_color, fg=fg_color)
        label.place(in_=canvas, relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the label in the center of the canvas
        # Bind the button click event to the command
        label.bind("<Button-1>", lambda event: command())
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        traceback.print_exc()

# Main application window
root = tk.Tk()  # Create the main window
root.title("My Friends GUI")  # Set the window title
root.geometry("1300x950")  # Set the window size
root.configure(bg='lightgreen')  # Set the background color

friends_folder = 'friends'  # Folder containing friend images

# Ensure the friends folder exists
if not os.path.exists(friends_folder):
    os.makedirs(friends_folder)

# Create a frame for the menu buttons
menu_frame = tk.Frame(root, bg='lightgreen')
menu_frame.pack(side=tk.TOP, pady=10)

# Create a container frame for the friends gallery
gallery_frame = tk.Frame(root, bg='lightgreen')
gallery_frame.pack(side=tk.TOP, pady=10)

# Create buttons in the main window
create_rounded_button(menu_frame, "Show Friends", lambda: show_friends(gallery_frame), "lightblue", "red")
create_rounded_button(menu_frame, "Clear All", lambda: clear_all(gallery_frame), "yellow", "black")
create_rounded_button(menu_frame, "Delete a Friend", lambda: delete_friend(gallery_frame, friends_folder), "pink", "black")
create_rounded_button(menu_frame, "Add New Friend", lambda: add_new_friend(gallery_frame, friends_folder), "white", "black")
create_rounded_button(menu_frame, "Quit", quit_app, "lightblue", "black")

# Run the main event loop
root.mainloop()
