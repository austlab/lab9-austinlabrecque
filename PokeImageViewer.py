from http.client import responses
from tkinter import *
from tkinter import ttk
from urllib import response
from pokeapi import get_pokemon_list, get_poke_image
import os
import sys
import ctypes
import requests

def main():
    
    #locates directory of script, creates 'images' directory in script's location if not already present
    script_directory = sys.path[0]
    img_dir = os.path.join(script_directory, 'images')
    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)

    #initializes main frame of GUI and name on application title bar
    root = Tk()
    root.title("Pokemon Image Viewer")
    
    #sets titlebar and taskbar icons, configures window geometry when resizing
    app_id = 'COMP593.PokeImageViewer' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_directory, 'Premier-Ball.ico'))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('600x600')

    #creates frame to segment into columns/rows. Places widgets
    frame = ttk.Frame(root)
    frame.grid(sticky=(N,S,E,W))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    
    img_pokemon = PhotoImage(file= os.path.join(script_directory, 'pokeball-png.png'))
    img_label = Label(frame, image= img_pokemon)
    img_label.grid(row=0, column=0, padx=10, pady=10)
    
    #places combobox widget and calls get_pokemon_list function in pokeapi script to populate combobox with pokemon names
    pokemon_list = get_pokemon_list() 
    cmbo_poke_selector = ttk.Combobox(frame, values=pokemon_list, state='readonly')
    cmbo_poke_selector.set('Select a Pokemon')
    cmbo_poke_selector.grid(row=1, column=0)
    
    def handle_cmbo_sel(event):
        '''
        pokemon_name: name of pokemon from pokeapi GET request
        image_url: url of pokemon image on pokeapi.co
        img_path: sets name of downloaded image
        download_image: calls function to download image
        returns: none
        '''
        pokemon_name = cmbo_poke_selector.get()
        image_url = get_poke_image(pokemon_name)
        img_path = os.path.join(img_dir, pokemon_name + '.png')
        download_image(image_url, img_path )
        if download_image(image_url, img_path):
            img_pokemon['file'] = img_path
    
    cmbo_poke_selector.bind('<<ComboboxSelected>>', handle_cmbo_sel)
    
    def btn_set_dsktop_click():
        '''
        pokemon_name: name of pokemon from pokeapi GET request
        img_path: sets name of downloaded image
        set_bckground: calls function to change background image
        returns: none
        '''
        pokemon_name = cmbo_poke_selector.get()
        img_path = os.path.join(img_dir, pokemon_name + '.png')
        set_bckgrnd(img_path)
    
    btn_set_desktop = ttk.Button(frame, text = 'Set as Desktop Image', command=btn_set_dsktop_click)
    btn_set_desktop.state(['!disabled'])
    btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)
    

    root.mainloop()
    
def download_image(url, path):
    '''
    resp: data returned from GET request
    returns: path if file management is successful
    '''
    resp = requests.get(url)
    if resp.status_code==200:
        try:
            img_data = resp.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        except:
            return
    else:
        print('Failed to download image. Response code:', resp.status_code)    
        
        
def set_bckgrnd(path):
  '''
    uses ctypes library to change background image
    returns: none
    '''
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    

main()