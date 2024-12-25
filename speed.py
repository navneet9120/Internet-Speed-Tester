import tkinter as tk
from tkinter import ttk, messagebox
import speedtest
import threading
import time

def check_speed():
    # Disable the "Test Speed" button and show "Please Wait" message
    check_button.config(state=tk.DISABLED)
    waiting_label.config(text="Please Wait... Testing Speed...")
    # Start the spinning animation
    animate_spinner(True)
    
    try:
        # Initialize Speedtest
        st = speedtest.Speedtest()
        st.get_best_server()  # Get the best server

        # Perform speed tests
        download_speed = st.download() / 1e6  # Convert to Mbps
        upload_speed = st.upload() / 1e6      # Convert to Mbps
        ping = st.results.ping
        
        # Update GUI with results after the test completes
        download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        ping_label.config(text=f"Ping: {ping:.2f} ms")
        
        # Show success message
        success_label.config(text="Speed Test Successful!", fg="green")
    
    except speedtest.SpeedtestCLIError as e:
        messagebox.showerror("Error", f"Speedtest CLI error: {e}")
    except Exception as e:
        if '403' in str(e):
            messagebox.showerror("Error", "HTTP 403 Forbidden: The server is blocking your request.")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        # Re-enable the "Test Speed" button and hide the "Please Wait" message
        check_button.config(state=tk.NORMAL)
        waiting_label.config(text="")
        # Stop the spinner animation
        animate_spinner(False)

def animate_spinner(animate):
    """Function to animate a spinning circle."""
    if animate:
        # Rotate the spinner
        angle = 0
        while angle < 360:
            canvas.delete("all")
            canvas.create_arc(10, 10, 90, 90, start=angle, extent=30, outline="white", width=4)
            angle += 10
            canvas.update()
            time.sleep(0.05)  # Adjust speed of animation
    else:
        canvas.delete("all")

def run_speed_test():
    # Run the speed test in a separate thread to avoid freezing the UI
    threading.Thread(target=check_speed, daemon=True).start()

# Create the main window
root = tk.Tk()
root.title("Internet Speed Tester")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="black")

# Add widgets
title_label = tk.Label(root, text="Internet Speed Tester", font=("Arial", 16, "bold"), bg="black", fg="white")
title_label.pack(pady=10)

# Instruction label
instruction_label = tk.Label(
    root,
    text="Click the 'Test Speed' button below to measure your internet speed.",
    font=("Arial", 12),
    bg="green",
    fg="white",
    wraplength=360,
    justify="center"
)
instruction_label.pack(pady=5)

# "Please Wait" message
waiting_label = tk.Label(root, text="", font=("Arial", 12), bg="black", fg="white")
waiting_label.pack(pady=5)

# Create a frame for the output box
output_frame = tk.Frame(root, bg="white", bd=2, relief="solid")  # White box with a border
output_frame.pack(pady=10, padx=20, fill="x")

# Add output labels inside the frame
download_label = tk.Label(output_frame, text="Download Speed: N/A", font=("Arial", 12), bg="white", fg="green")
download_label.pack(pady=5)

upload_label = tk.Label(output_frame, text="Upload Speed: N/A", font=("Arial", 12), bg="white", fg="green")
upload_label.pack(pady=5)

ping_label = tk.Label(output_frame, text="Ping: N/A", font=("Arial", 12), bg="white", fg="green")
ping_label.pack(pady=5)

# Success message label
success_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="black", fg="green")
success_label.pack(pady=5)

# Add the "Test Speed" button
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), foreground="green", background="white")
style.map("TButton", background=[("active", "lightgray")])

check_button = ttk.Button(root, text="Test Speed", command=run_speed_test, style="TButton")
check_button.pack(pady=10)

# Add the "Exit" button
exit_button = ttk.Button(root, text="Exit", command=root.destroy, style="TButton")
exit_button.pack(pady=10)



# Create the canvas for the spinning animation
canvas = tk.Canvas(root, width=100, height=100, bg="black", bd=0, highlightthickness=0)
canvas.pack(pady=10)





# Run the application
root.mainloop()
