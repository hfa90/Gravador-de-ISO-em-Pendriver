import subprocess  # Importa o módulo subprocess para executar comandos do sistema
import tkinter as tk  # Importa a biblioteca tkinter para criar a interface gráfica
from tkinter import filedialog, messagebox  # Importa submódulos específicos do tkinter

# Função para escrever a ISO no pendrive
def write_iso_to_usb(iso_path, usb_path, partition_type):
    try:
        # Executa o comando dd para copiar a ISO para o pendrive
        subprocess.run(['sudo', 'dd', 'bs=4M', 'if=' + iso_path, 'of=' + usb_path, 'status=progress'])
        
        # Verifica o tipo de partição selecionado e ajusta o esquema de partição
        if partition_type == "MBR":
            subprocess.run(['sudo', 'fdisk', usb_path], input=b'n\np\n1\n\n\nw\n')
        elif partition_type == "GPT":
            subprocess.run(['sudo', 'gdisk', usb_path], input=b'o\nY\nn\n\n\n\n0700\nw\nY\n')
        
        # Exibe uma mensagem de sucesso se o processo for concluído sem erros
        messagebox.showinfo("Success", "ISO written to USB successfully!")
    except Exception as e:
        # Exibe uma mensagem de erro se ocorrer uma exceção
        messagebox.showerror("Error", str(e))

# Função para selecionar o arquivo ISO
def select_iso_file():
    # Abre uma janela de seleção de arquivo e obtém o caminho do arquivo selecionado
    iso_file_path = filedialog.askopenfilename(filetypes=[("ISO files", "*.iso")])
    
    # Insere o caminho do arquivo selecionado no campo de entrada
    iso_entry.delete(0, tk.END)
    iso_entry.insert(0, iso_file_path)

# Função para selecionar o pendrive USB
def select_usb_drive():
    # Abre uma janela de seleção de diretório e obtém o caminho do diretório selecionado
    usb_drive_path = filedialog.askdirectory()
    
    # Insere o caminho do diretório selecionado no campo de entrada
    usb_entry.delete(0, tk.END)
    usb_entry.insert(0, usb_drive_path)

# Função para iniciar o processo de escrita da ISO no pendrive
def start_write():
    # Obtém os caminhos do arquivo ISO e do pendrive USB e o tipo de partição selecionado
    iso_path = iso_entry.get()
    usb_path = usb_entry.get()
    partition_type = partition_var.get()

    # Verifica se ambos os campos foram preenchidos
    if iso_path and usb_path:
        # Chama a função para escrever a ISO no pendrive
        write_iso_to_usb(iso_path, usb_path, partition_type)
    else:
        # Exibe uma mensagem de erro se algum campo estiver vazio
        messagebox.showerror("Error", "Please select ISO file and USB drive!")

# Cria uma janela principal
window = tk.Tk()
window.title("Gravador de ISO Hayden_ISO")  # Define o título da janela

# Cria frames para organizar os widgets
iso_frame = tk.Frame(window)
usb_frame = tk.Frame(window)
partition_frame = tk.Frame(window)
button_frame = tk.Frame(window)

# Cria os widgets necessários
iso_label = tk.Label(iso_frame, text="ISO File:")  # Rótulo para o campo de entrada do arquivo ISO
iso_entry = tk.Entry(iso_frame, width=40)  # Campo de entrada para o caminho do arquivo ISO
iso_button = tk.Button(iso_frame, text="Browse", command=select_iso_file)  # Botão para selecionar o arquivo ISO

usb_label = tk.Label(usb_frame, text="USB Drive:")  # Rótulo para o campo de entrada do pendrive USB
usb_entry = tk.Entry(usb_frame, width=40)  # Campo de entrada para o caminho do pendrive USB
usb_button = tk.Button(usb_frame, text="Browse", command=select_usb_drive)  # Botão para selecionar o pendrive USB

partition_label = tk.Label(partition_frame, text="Partition Type:")  # Rótulo para o tipo de partição
partition_var = tk.StringVar()  # Variável para armazenar o tipo de partição selecionado
partition_var.set("MBR")  # Define o valor padrão como MBR
mbr_radio = tk.Radiobutton(partition_frame, text="MBR", variable=partition_var, value="MBR")  # Botão de seleção para MBR
gpt_radio = tk.Radiobutton(partition_frame, text="GPT", variable=partition_var, value="GPT")  # Botão de seleção para GPT

start_button = tk.Button(button_frame, text="Start", command=start_write)  # Botão para iniciar o processo de escrita

# Organiza os widgets dentro dos frames
iso_label.grid(row=0, column=0)
iso_entry.grid(row=0, column=1)
iso_button.grid(row=0, column=2)

usb_label.grid(row=0, column=0)
usb_entry.grid(row=0, column=1)
usb_button.grid(row=0, column=2)

partition_label.pack(side=tk.LEFT)
mbr_radio.pack(side=tk.LEFT)
gpt_radio.pack(side=tk.LEFT)

start_button.pack()

# Organiza os frames dentro da janela principal
iso_frame.pack(pady=10)
usb_frame.pack(pady=10)
partition_frame.pack(pady=10)
button_frame.pack(pady=10)

# Inicia o loop da janela
window.mainloop()
