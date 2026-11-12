import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

BG='#10131b'; PANEL='#1a2030'; FG='#e6eaf3'; ACC='#8c7aff'
class App:
    def __init__(self,root):
        self.root=root; root.title('luna lua studio — standalone'); root.geometry('940x640'); root.configure(bg=BG)
        self.tabs={}; self.count=0
        head=tk.Frame(root,bg=BG); head.pack(fill='x',padx=16,pady=(14,8))
        tk.Label(head,text='◈  luna lua studio',font=('Segoe UI',19,'bold'),bg=BG,fg=FG).pack(side='left')
        tk.Label(head,text='standalone lua • no roblox injection',bg=BG,fg='#a3aabc').pack(side='right')
        bar=tk.Frame(root,bg=BG);bar.pack(fill='x',padx=16,pady=6)
        for label,fn in [('＋ new tab',self.new_tab),('open',self.open_file),('save',self.save_file),('▶ execute',self.execute),('clear',self.clear)]:
            tk.Button(bar,text=label,command=fn,bg=ACC if 'execute' in label else PANEL,fg='white',activebackground='#6654cf',activeforeground='white',relief='flat',font=('Segoe UI',10,'bold'),padx=13,pady=8).pack(side='left',padx=(0,8))
        style=ttk.Style();style.theme_use('default');style.configure('TNotebook',background=BG,borderwidth=0);style.configure('TNotebook.Tab',background=PANEL,foreground=FG,padding=(15,8));style.map('TNotebook.Tab',background=[('selected',ACC)])
        self.notebook=ttk.Notebook(root);self.notebook.pack(fill='both',expand=True,padx=16,pady=(4,8))
        tk.Label(root,text='output console',bg=BG,fg=FG,font=('Segoe UI',10,'bold')).pack(anchor='w',padx=16)
        self.output=tk.Text(root,height=9,bg='#0a0d14',fg='#a9efc0',insertbackground=FG,relief='flat',font=('Consolas',10),state='disabled');self.output.pack(fill='x',padx=16,pady=(5,16))
        self.new_tab()
    def current(self):
        tab=self.notebook.select();return self.tabs.get(tab)
    def new_tab(self,content='-- welcome to luna lua studio\nprint("hello from lua!")\n',name=None):
        self.count+=1; frame=tk.Frame(self.notebook,bg=PANEL)
        editor=tk.Text(frame,bg=PANEL,fg=FG,insertbackground=FG,selectbackground='#594ca1',undo=True,wrap='none',font=('Consolas',12),relief='flat',padx=14,pady=14)
        sy=tk.Scrollbar(frame,command=editor.yview);sy.pack(side='right',fill='y');editor.configure(yscrollcommand=sy.set);editor.pack(fill='both',expand=True)
        editor.insert('1.0',content);self.notebook.add(frame,text=name or f'script {self.count}');self.notebook.select(frame)
        self.tabs[str(frame)]={'editor':editor,'path':None}
    def open_file(self):
        path=filedialog.askopenfilename(filetypes=[('lua scripts','*.lua'),('text files','*.txt'),('all files','*.*')]);
        if path:
            try:
                self.new_tab(Path(path).read_text(encoding='utf-8'),Path(path).name);self.current()['path']=path
            except Exception as exc:messagebox.showerror('open error',str(exc))
    def save_file(self):
        cur=self.current();path=cur['path'] or filedialog.asksaveasfilename(defaultextension='.lua',filetypes=[('lua scripts','*.lua')]);
        if path:
            try:
                Path(path).write_text(cur['editor'].get('1.0','end-1c'),encoding='utf-8');cur['path']=path;self.notebook.tab(self.notebook.select(),text=Path(path).name);self.log('saved: '+path)
            except Exception as exc:messagebox.showerror('save error',str(exc))
    def clear(self):self.current()['editor'].delete('1.0','end')
    def log(self,s):
        def append():
            self.output.configure(state='normal');self.output.insert('end',str(s)+'\n');self.output.see('end');self.output.configure(state='disabled')
        self.root.after(0,append)
    def execute(self):
        script=self.current()['editor'].get('1.0','end-1c');self.log('> executing standalone lua script...')
        def work():
            try:
                from lupa import LuaRuntime
                lua=LuaRuntime(unpack_returned_tuples=True)
                # No Python bridge beyond a simple print callback. Avoid exposing Python globals.
                lua.globals().print=lambda *args:self.log('  '.join(map(str,args)))
                lua.execute(script);self.log('✓ finished')
            except ImportError:self.log('lua runtime missing: install lupa (pip install lupa)')
            except Exception as exc:self.log('error: '+str(exc))
        threading.Thread(target=work,daemon=True).start()
if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
