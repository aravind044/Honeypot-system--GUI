import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import datetime

def start_honeypot():
    log_text.insert(tk.END, "[INFO] Honeypot Started...\n")
    log_text.yview(tk.END)
    
    def honeypot_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", 8080))  
        server_socket.listen(5)
        log_text.insert(tk.END, "[INFO] Listening for incoming connections on port 8080...\n")
        log_text.yview(tk.END)
        
        while True:
            client_socket, client_address = server_socket.accept()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_text.insert(tk.END, f"[ALERT] Unauthorized access attempt from {client_address} at {timestamp}\n")
            log_text.yview(tk.END)
            client_socket.send(b"Access Denied! This is a Honeypot.\n")
            client_socket.close()
    
    threading.Thread(target=honeypot_server, daemon=True).start()


root = tk.Tk()
root.title("Honeypot Security System")
root.geometry("500x300")

log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.pack(pady=10)

start_button = tk.Button(root, text="Start Honeypot", command=start_honeypot)
start_button.pack()

root.mainloop()