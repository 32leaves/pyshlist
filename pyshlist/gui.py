from tkinter import *

def purchase(data = None):
    """Produces a TKinter form for editing purchase data and returns the data as hash"""

    root = Tk()
    root.title("Purchase")
    
    field_names = [ "name", "price", "due_date", "category", "description" ]
    field_vars = { name: StringVar() for name in field_names }

    if data is None:
        data = { }
    else:
        for name in field_names:
            field_vars[name].set(data.get(name) or "")

    def save():
        for name in field_names:
            data[name] = field_vars[name].get()
        root.destroy()
    def cancel():
        root.destroy()    

    mainframe = Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    
    field_widgets = {}
    for idx, name in enumerate(field_names):
        Label(mainframe, text=name).grid(column=1, row=idx + 1, sticky=W)
        entry = Entry(mainframe, width=20, textvariable=field_vars[name])
        entry.grid(column=2, row=idx+1, sticky=(W, E))
        field_widgets[name] = entry
        
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    field_widgets[field_names[0]].focus()
    
    button_row = len(field_names) + 1
    Button(mainframe, text="Save", command=save).grid(column=1, row=button_row, sticky=W)
    Button(mainframe, text="Cancel", command=cancel).grid(column=2, row=button_row, sticky=W)
    
    mainframe.after(1, lambda: mainframe.focus_force())
    
    mainloop()
    return data


def compare(a, b):
    """Opens a window for comparing two strings and returns a hash with the keys canceled, important, less_important"""
    root = Tk()
    root.title("Compare")
    mainframe = Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    
    result = { 'canceled' : True, 'a' : a, 'b' : b }
    def choose(was_canceled, a_more_important):
        result["canceled"] = was_canceled
        result["a_more_important"] = a_more_important
        root.destroy()

    fb = Button(mainframe, text=a, command=lambda: choose(False, True), width=50)
    fb.grid(row=1, column=1, sticky=W, padx=10)
    Button(mainframe, text=b, command=lambda: choose(False, False), width=50).grid(row=2, column=1, sticky=W, padx=10)
    Button(mainframe, text="None", command=lambda: choose(False, None), width=50).grid(row=4, column=1, sticky=W, pady=10, padx=10)
    Button(mainframe, text="Cancel", command=lambda: choose(True, None), width=50).grid(row=5, column=1, sticky=W, padx=10)
    fb.focus()
    
    mainframe.after(1, lambda: mainframe.focus_force())
    
    mainloop()
    return result
