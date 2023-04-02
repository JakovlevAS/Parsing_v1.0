# Import required modules
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import os
import datetime

def active_label(parent):
    # Create a container frame
    frame = Frame(parent)

    lbl1 = Label(frame, text='Отправьте ссылку на картинку') #Creates a Label widget with the caption
    lbl2 = Label(frame, text='Время работы программы: ')
    lbl1.grid(column=0, row=0, padx=10, pady=10)
    lbl2.grid(column=1, row=1, padx=10, pady=10)
    url_entry = ttk.Entry(frame) #Creates an Entry widget for inputting a URL.
    url_entry.grid(column=0, row=1, padx=10, pady=10)

    # Define the start time for the elapsed time label
    start_time = datetime.datetime.now()


    def on_submit(): #Defines the behavior when the "Отправить" button is clicked.
        url_entry_text = url_entry.get()
        parsing(url_entry_text)
        clear(url_entry)

    btn1 = Button(frame, text='Отправить', command=on_submit)
    btn1.grid(column=0, row=3, padx=10, pady=10)

    frame.grid(row=0, column=0, sticky="nsew") #Places the frame widget in a grid layout in row 0 and column 0 and sets the widget to stretch in all directions.
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Start the label update loop
    lbl2.after(1000, update_label, lbl2, start_time)

    return url_entry, frame, lbl2

def update_label(lbl2, start_time):
    delta = str(datetime.datetime.now() - start_time)
    lbl2.config(text='Время работы программы: ' + delta.split('.')[0])
    lbl2.after(1000, update_label, lbl2, start_time)



def clear(url_entry):   #Defines the clear() function to clear the entry widget.
    url_entry.delete(0, END)


def parsing(url_entry_text): # Defines the function parsing() to extract information from the URL entered in the entry widget
    if not url_entry_text:  # It performs a check to see if the entry is empty or not and prints an error message if it is empty.
        print("Invalid URL: No URL supplied")
        return

    # make sure the input has a valid prefix
    if not url_entry_text.startswith('http'):
        url_entry_text = 'http://' + url_entry_text

    try:
        response = requests.get(url_entry_text)
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    folder_path = 'X:\\Картинки'

    #The function then checks if a directory exists at the specified path, and creates it if it does not exist.
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except os.error as e:
        print("Error creating directory:", e)
        return
    #For each <img> tag found in the HTML content, the function extracts the image URL and attempts to write the image to the specified directory using requests and open.
    for img_tag in soup.find_all('img'):
        image_url = img_tag.get('src')
        if image_url is not None and 'http' in image_url:
            image_name = image_url.split("/")[-1]
            try:
                with open(os.path.join(folder_path, image_name), 'wb') as f:
                    f.write(requests.get(image_url).content)
            except IOError as e:
                print("Error writing image file:", e)


if __name__ == '__main__':
    root = Tk()
    root.title("Приложение для парсинга")
    root.geometry("400x400")
    bt1 = active_label(root)
    root.mainloop()
