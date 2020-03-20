# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:53:05 2020

@author: Chan Chak Tong
"""

#%%
# Window meta
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import shutil
import os

class Utility:
    @staticmethod
    def save_data(data, data_path=r'./data.txt'):
        assert isinstance(data, (list, tuple)), 'Invalid type of data'
        with open(data_path, 'w') as streamer:
            for (name, path) in data:
                streamer.write('%s-!-%s\n' % (name, path))
    
    @staticmethod
    def load_data(data_path=r'./data.txt'):
        with open(data_path, 'r') as streamer:
            data = streamer.read().splitlines()
        return list(map(lambda s: s.split('-!-'), data))
    
class PathDialog(tk.Toplevel):
    def __init__(self, parent, backup_path='./savedata'):
        tk.Toplevel.__init__(self, parent)
        self.grab_set()
        self.lift()
        self.title(r'Path of backup folder')
        self.build(backup_path)
        self.wait_window()
        
    def build(self, backup_path):
        # Prompt frame
        self.prompt_frame = tk.Frame(self)
        self.prompt_frame.pack(side=tk.TOP,
                               padx=30, pady=5)
        
        self.path_label = tk.Label(self.prompt_frame, text='Select Folder: ')
        self.path_label.pack(side=tk.TOP,
                             ipadx=5, ipady=2)
        
        self.path_string = tk.StringVar(value=backup_path)
        self.path_textbox = tk.Entry(self.prompt_frame, width=50,
                                     textvariable=self.path_string)
        self.path_textbox.pack(side=tk.TOP,
                               padx=5, pady=2)
        
        # Option frame
        self.option_frame = tk.Frame(self)
        self.option_frame.pack(side=tk.TOP, 
                          padx=30, pady=5)
        
        # OK button
        self.ok_button = tk.Button(self.option_frame, text='OK', command=self.confirm)
        self.ok_button.grid(row=0, column=0,
                       ipadx=20, padx=5)
        
        # Cancel button
        self.cancel_button = tk.Button(self.option_frame, text='Clear', command=self.destroy)
        self.cancel_button.grid(row=0, column=1,
                          ipadx=20, padx=5)
    
    def confirm(self):
        path = self.path_string.get()
        if path.strip == '':
            tk.messagebox.showerror('Error', 'Entry cannot be empty')
        else:
            self.destroy()
            self.grab_release()
            self.path = path
    
    def fetch(self):
        return self.path

class SettingDialog(tk.Toplevel):
    def __init__(self, parent, name_text='', path_text=''):
        tk.Toplevel.__init__(self, parent)
        self.grab_set()
        self.lift()
        self.title(r'Setting')
        self.build(name_text, path_text)
        self.wait_window()

    def build(self, name_text, path_text):
        # Prompt frame
        self.prompt_frame = tk.Frame(self)
        self.prompt_frame.pack(side=tk.TOP, 
                          padx=30, pady=5)
        
        # Name
        self.name_label = tk.Label(self.prompt_frame, text='Name')
        self.name_label.grid(row=0, column=0, 
                        ipadx=5, ipady=2)
        
        self.name_string = tk.StringVar(value=name_text)
        self.name_textbox = tk.Entry(self.prompt_frame, width=50,
                                     textvariable=self.name_string)
        self.name_textbox.grid(row=0, column=1,
                          padx=5, pady=2)
        
        # Path
        self.path_label = tk.Label(self.prompt_frame, text='Path')
        self.path_label.grid(row=1, column=0,
                        ipadx=5, ipady=2)
        
        self.path_string = tk.StringVar(value=path_text)
        self.path_textbox = tk.Entry(self.prompt_frame, width=50,
                                     textvariable=self.path_string)
        self.path_textbox.grid(row=1, column=1,
                          padx=5, pady=2)
        
        self.path_select_button = tk.Button(self.prompt_frame, text=r'Select...',
                                       command=self.path_selected)
        self.path_select_button.grid(row=1, column=2,
                                ipadx=7, ipady=2)
        
        # Option frame
        self.option_frame = tk.Frame(self)
        self.option_frame.pack(side=tk.TOP, 
                          padx=30, pady=5)
        
        # OK button
        self.ok_button = tk.Button(self.option_frame, text='OK', command=self.confirm)
        self.ok_button.grid(row=0, column=0,
                       ipadx=20, padx=5)
        
        # Clear button
        self.clear_button = tk.Button(self.option_frame, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=1,
                          ipadx=20, padx=5)

    def path_selected(self):
        self.path_string.set(filedialog.askdirectory())
  
    def confirm(self):
        name = self.name_string.get()
        path = self.path_string.get()
        # Check if it's blank
        if name.strip() == '' or path.strip() == '':
            tk.messagebox.showerror('Error', 'Entries cannot be empty')
        else:
            self.destroy()
            self.grab_release()
            self.name = name
            self.path = path
    
    def fetch(self):
        return self.name, self.path
    
    def clear(self):
        self.name_textbox.delete(0, 'end')
        self.path_textbox.delete(0, 'end')
        
class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        # Information Panel
        self.information_frame = tk.Frame(self)
        self.information_frame.pack(side=tk.TOP)
        
        self.detail_table = DetailTable(self.information_frame, ('Name', 'Path'))
        self.detail_table.pack()
        
        # Button Panel
        self.option_frame = tk.Frame(self)
        self.option_frame.pack(side=tk.TOP)
        
        self.add_button = tk.Button(self.option_frame, text=r'Add...',
                                    command=self.create_item)
        self.add_button.pack(side=tk.LEFT,
                             ipadx=7, ipady=2, padx=5, pady=2)
        
        self.edit_button = tk.Button(self.option_frame, text=r'Edit...',
                                     command=self.edit_item)
        self.edit_button.pack(side=tk.LEFT,
                              ipadx=7, ipady=2, padx=5, pady=2)
        
        self.delete_button = tk.Button(self.option_frame, text=r'Delete',
                                       command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT,
                                ipadx=7, ipady=2, padx=5, pady=2)
        
        self.backup_button = tk.Button(self.option_frame, text=r'Backup...',
                                       command=self.backup)
        self.backup_button.pack(side=tk.LEFT,
                                ipadx=7, ipady=2, padx=5, pady=2)
        
        # Progress Bar
        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(side=tk.TOP)
        
        self.progress_string = tk.StringVar()
        self.progress_label = tk.Label(self.progress_frame, textvariable=self.progress_string)
        self.progress_label.pack(side=tk.TOP,
                                 padx=5, pady=2)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient='horizontal', length=600, mode='determinate')
        self.progress_bar['maximum'] = 100
        self.progress_bar['value'] = 0
        self.progress_bar.pack(side=tk.TOP,
                               padx=5, pady=5)
    def create_item(self):
        setting_dialog = SettingDialog(self)
        try:
            name, path = setting_dialog.fetch()
            self.detail_table.insert('', 'end', values=(name, path))
            self.detail_table.save()
        except AttributeError:
            pass
    
    def edit_item(self):
        index, name, path = self.detail_table.get_selected()
        if index == -1:
            tk.messagebox.showerror('Error', 'No item is selected')
        else:
            setting_dialog = SettingDialog(self, name, path)
            try:
                name, path = setting_dialog.fetch()
                self.detail_table.item(index, values=(name, path))
                self.detail_table.save()
            except AttributeError:
                pass
    
    def delete_item(self):
        index, _, _ = self.detail_table.get_selected()
        if index == -1:
            tk.messagebox.showerror('Error', 'No item is selected')
        else:
            self.detail_table.delete(index)
            self.detail_table.save()
    
    def backup(self):
        path_dialog = PathDialog(self)
        try:
            dst = path_dialog.fetch()
            for name, src in Utility.load_data():
                if not os.path.isdir(r'%s/%s' % (dst, name)):
                    shutil.copytree(src, r'%s/%s' % (dst, name))
        except AttributeError:
            pass
        
        
class DetailTable(ttk.Treeview):
    def __init__(self, parent, columns):
        ttk.Treeview.__init__(self, parent, columns=columns,
                              show='headings', selectmode='browse')

        self.column('Name', width=100)
        self.column('Path', width=500)
        self.heading('Name', text='Name')
        self.heading('Path', text='Path')
        self.bind('<<TreeviewSelect>>', self.on_select)
        
        self.selected = (-1,)
        
        self.load()
        
    def load(self):
        data = Utility.load_data()
        for name, path in data:
            self.insert('', 'end', values=(name, path))
    
    def save(self):
        data = self.get_all_items()
        Utility.save_data(data)
    
    def get_all_items(self):
        indices = self.get_children()
        return list(map(lambda i: self.item(i)['values'], indices))
        
    def on_select(self, event):
        self.selected = event.widget.selection()
    
    def get_selected(self):
        index = self.selected[0]
        if self.exists(index):
            name, path = self.item(index)['values']
            return index, name, path
        else:
            return -1, '', ''
#%%
window = tk.Tk()
window.title('Save Restorer')
MainFrame(window).pack()
window.mainloop()
