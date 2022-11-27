import socket,threading
import tkinter,tkinter.scrolledtext
from tkinter import simpledialog

host='127.0.0.1' ; port=5555

class Client:
    def __init__(self,host,port) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        self.nickname=simpledialog.askstring("NickName","Please choose a nickname",parent=msg)
        
        self.gui_done=False
        self.Running = True
        
        gui_thread=threading.Thread(target=self.gui_loop,daemon=True)
        receive_thread=threading.Thread(target=self.receive)
        
        gui_thread.start();receive_thread.start()
        
    def gui_loop(self): # The Main Thread
        self.win=tkinter.Tk()
        self.win.configure(bg='lightgrey')
        
        self.chat_label=tkinter.Label(self.win,text='Chat :',bg='lightgrey')
        self.chat_label.config(font=('Arial',12))
        self.chat_label.pack(padx=20,pady=5)
        
        self.text_area=tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label=tkinter.Label(self.win,text='Message :',bg='lightgrey')
        self.msg_label.config(font=('Arial',12))
        self.msg_label.pack(padx=20,pady=5)
        
        self.input_area = tkinter.Text(self.win,height=3)
        self.input_area.pack(padx=20,pady=5)
        
        self.send_btn=tkinter.Button(self.win,text='Send',command=self.write)
        self.send_btn.config(font=('Arial',12))
        self.send_btn.pack(padx=20,pady=5)
        
        self.gui_done=True
        
        # when we close the window , we call stop function to terminate the whole app 
        self.win.protocol('WM_DELETE_WINDOW',self.stop)
        self.win.mainloop()
        
    def stop(self):
        self.Running=False
        self.win.destroy()
        self.sock.close()
        exit(0)
    
    def write(self):
            message = f'{self.nickname}: {self.input_area.get("1.0","end")}' # 1.0  start from the beginning up to the end (get the whole text)
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete("1.0","end") # clear text box after sending message 
    
    def receive(self): # Daemon Thread in the background
        while self.Running :
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done :
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message) # append the message at the end
                        self.text_area.yview('end') # always scroll down to the end 
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError :
                break
            except :
                print("An error occurred !")
                self.sock.close()
                break
                
client=Client(host,port)   
