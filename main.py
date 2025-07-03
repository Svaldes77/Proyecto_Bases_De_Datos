from controlador.login_controlador  import Controlador_login
#FINAL 
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    # Don't hide the root initially since Login_vista will use it
    Controlador_login(root)
    root.mainloop()
    