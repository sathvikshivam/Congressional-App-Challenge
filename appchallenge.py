import sqlite3
import tkinter as tk
from tkinter import messagebox, font, Scrollbar, Checkbutton, IntVar
from datetime import datetime

# Database setup
conn = sqlite3.connect('community_food_share.db')
cursor = conn.cursor()

# Creating the table for food posts (if it doesn't already exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS food_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    quantity TEXT,
                    location TEXT,
                    post_date TEXT)''')
conn.commit()

# Function to add food post to the database
def add_food_post(description, quantity, location):
    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO food_posts (description, quantity, location, post_date) VALUES (?, ?, ?, ?)",
                   (description, quantity, location, post_date))
    conn.commit()
    messagebox.showinfo("Success", "Surplus food added successfully!")

# Function to view food posts with checkboxes to remove them
def view_food_posts():
    cursor.execute("SELECT id, description, quantity, location, post_date FROM food_posts")
    posts = cursor.fetchall()  # Fetch all posts as tuples
    display_posts(posts)

# Function to display posts with checkboxes and a remove button
def display_posts(posts):
    post_window = tk.Toplevel(app)
    post_window.title("Available Surplus Food")
    post_window.geometry("400x400")
    post_window.configure(bg="#F1F1F1")

    canvas = tk.Canvas(post_window, bg="#F1F1F1")
    scrollbar = Scrollbar(post_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F1F1F1")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Store variables for checkboxes
    check_vars = []

    for post in posts:
        post_id, description, quantity, location, post_date = post
        var = IntVar()  # Checkbox variable
        check_vars.append((var, post_id))

        # Display each post with a checkbox
        post_label = tk.Label(
            scrollable_frame, 
            text=f"{description} - {quantity} portions, Location: {location}, Posted on: {post_date}",
            bg="#E8F9FD",
            fg="#333333",
            font=custom_font_small,
            wraplength=350,
            justify="left"
        )
        post_label.pack(padx=10, pady=5, fill="x", expand=True)

        checkbox = Checkbutton(scrollable_frame, variable=var, bg="#F1F1F1")
        checkbox.pack(pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Button to remove selected posts
    remove_button = tk.Button(scrollable_frame, text="Remove Selected", command=lambda: remove_selected(check_vars, post_window), bg="#FF6666", fg="white", padx=5, pady=5)
    remove_button.pack(pady=20)

# Function to remove selected posts from the database
def remove_selected(check_vars, window):
    selected_posts = [post_id for var, post_id in check_vars if var.get() == 1]
    
    if selected_posts:
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove the selected posts?")
        if confirm:
            cursor.executemany("DELETE FROM food_posts WHERE id = ?", [(post_id,) for post_id in selected_posts])
            conn.commit()
            messagebox.showinfo("Success", "Selected posts have been removed.")
            window.destroy()  # Close the window and refresh
            view_food_posts()  # Refresh the list
    else:
        messagebox.showwarning("No Selection", "Please select at least one item to remove.")

# GUI Setup
app = tk.Tk()
app.title("Community Food Share")
app.geometry("500x400")
app.configure(bg="#E8F9FD")

# Custom fonts
custom_font_large = font.Font(family="Arial", size=16, weight="bold")
custom_font_medium = font.Font(family="Arial", size=12)
custom_font_small = font.Font(family="Arial", size=10)

# Title Label
title_label = tk.Label(app, text="Community Food Share", font=custom_font_large, bg="#E8F9FD", fg="#333333")
title_label.pack(pady=20)

# Frame for adding food
add_frame = tk.Frame(app, bg="#F1F1F1", padx=10, pady=10)
add_frame.pack(pady=10, fill="x", padx=20)

tk.Label(add_frame, text="Description", font=custom_font_medium, bg="#F1F1F1").grid(row=0, column=0, sticky="w")
description_entry = tk.Entry(add_frame, font=custom_font_small, width=30)
description_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(add_frame, text="Quantity", font=custom_font_medium, bg="#F1F1F1").grid(row=1, column=0, sticky="w")
quantity_entry = tk.Entry(add_frame, font=custom_font_small, width=30)
quantity_entry.grid(row=1, column=1, pady=5, padx=5)

tk.Label(add_frame, text="Location", font=custom_font_medium, bg="#F1F1F1").grid(row=2, column=0, sticky="w")
location_entry = tk.Entry(add_frame, font=custom_font_small, width=30)
location_entry.grid(row=2, column=1, pady=5, padx=5)

def add_food():
    description = description_entry.get()
    quantity = quantity_entry.get()
    location = location_entry.get()
    
    if description and quantity and location:
        add_food_post(description, quantity, location)
        description_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

add_button = tk.Button(add_frame, text="Add Food", command=add_food, font=custom_font_medium, bg="#5BC8AF", fg="white", padx=5, pady=5)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# View Surplus Food Button
view_button = tk.Button(app, text="View Available Surplus Food", command=view_food_posts, font=custom_font_medium, bg="#5BC8AF", fg="white", padx=5, pady=5)
view_button.pack(pady=20)

app.mainloop()
