import tkinter as tk

 

if __name__ == "__main__":

    root = tk.Tk()

    def test(window):
        window=window
        window
        window.configure(bg="blue")   

    root.geometry("800x500")
    root.title("GUI")
    
    label = tk.Label(root, text="XD", font=('Arial', 18))
    label.pack(padx=10, pady=20)

    textbox = tk.Text(root, height=1, width=100, font=("Arial", 16))
    textbox.pack(padx=350)
    

    button = tk.Button(command=lambda:test(root))
    button.pack()
    print(type(root))
    print(root)

    root.mainloop()