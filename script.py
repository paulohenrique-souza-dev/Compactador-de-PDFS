import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def caminho_recurso(relative_path):
    """Obtem o caminho absoluto para um recurso, funciona para executáveis gerados por PyInstaller e scripts normais."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def compress_pdf(input_path, output_path, quality="/printer"):
    gs_executable = caminho_recurso("gswin64c.exe")
    if not os.path.exists(gs_executable):
        messagebox.showerror("Erro", f"Executável do Ghostscript não encontrado:\n{gs_executable}")
        return False
    command = [
        gs_executable,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode() if e.stderr else str(e)
        messagebox.showerror("Erro ao compactar PDF", f"Erro ao compactar {input_path}:\n{err_msg}")
        return False


# nas funçoes a seguir, uso o global para não criar uma variavel local e o programa saber qual a pasta.

def selecionar_pasta_entrada():
    global pasta_entrada
    pasta_entrada = filedialog.askdirectory(title="Selecione a pasta com arquivos PDF")
    if pasta_entrada:
        status_var.set(f"Pasta de entrada selecionada:\n{pasta_entrada}")
    else:
        status_var.set("Nenhuma pasta de entrada selecionada")

def selecionar_pasta_saida():
    global pasta_saida
    pasta_saida = filedialog.askdirectory(title="Selecione a pasta onde salvar os arquivos compactados")
    if pasta_saida:
        status_var.set(f"Pasta de saída selecionada:\n{pasta_saida}")
    else:
        status_var.set("Nenhuma pasta de saída selecionada")

def iniciar_compressao():
    if not pasta_entrada or not pasta_saida:
        messagebox.showwarning("Aviso", "Selecione as duas pastas antes de iniciar a compressão.")
        return

    pdfs_entrada = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(".pdf")]
    if not pdfs_entrada:
        messagebox.showinfo("Nenhum PDF", "Nenhum arquivo PDF encontrado na pasta selecionada.")
        return

    qualidade_escolhida = qualidade_var.get()
    qualidade = opcoes_qualidade.get(qualidade_escolhida, "/printer")

    total = len(pdfs_entrada)
    compactados = 0

    tamanho_original_total = 0
    tamanho_compactado_total = 0

    for i, pdf_file in enumerate(pdfs_entrada, 1):
        input_path = os.path.join(pasta_entrada, pdf_file)
        output_path = os.path.join(pasta_saida, pdf_file)
        tamanho_original_total += os.path.getsize(input_path)

        status_var.set(f"[{i}/{total}] Compactando: {pdf_file}")
        root.update()

        if compress_pdf(input_path, output_path, quality=qualidade):
            compactados += 1

    for pdf_file in os.listdir(pasta_saida):
        if pdf_file.lower().endswith(".pdf"):
            tamanho_compactado_total += os.path.getsize(os.path.join(pasta_saida, pdf_file))

    status_var.set(f"Concluído: {compactados} de {total} PDFs compactados.")

    if compactados > 0 and tamanho_original_total > 0:
        reducao_bytes = tamanho_original_total - tamanho_compactado_total
        reducao_percent = (reducao_bytes / tamanho_original_total) * 100
        reducao_mb = reducao_bytes / (1024 * 1024)
        tamanho_original_mb = tamanho_original_total / (1024 * 1024)
        tamanho_compactado_mb = tamanho_compactado_total / (1024 * 1024)
        reducao_var.set(
            f"Antes: {tamanho_original_mb:.2f} MB  |  Agora: {tamanho_compactado_mb:.2f} MB  |  Redução: {reducao_mb:.2f} MB ({reducao_percent:.2f}%)"
        )
    else:
        reducao_var.set("Nenhum arquivo foi compactado.")

    messagebox.showinfo("Finalizado",
                        f"{compactados} PDFs foram compactados e salvos em:\n{pasta_saida}\n\n"
                        f"{reducao_var.get()}")

pasta_entrada = None
pasta_saida = None

root = tk.Tk()
root.title("Compactador de PDFS")
root.geometry("800x600")
root.resizable(False, False)

background_image_path = caminho_recurso("foto pdf.jpg")
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=900, height=800, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

status_var = tk.StringVar(value="Selecione as pastas para iniciar...")
qualidade_var = tk.StringVar()
reducao_var = tk.StringVar(value="")

opcoes_qualidade = {
    "Mínima (screen)": "/screen",
    "Equilibrada (ebook)": "/ebook",
    "Alta (printer)": "/printer",
    "Muito alta (prepress)": "/prepress"
}

qualidade_var.set("Alta (printer)")  # Valor padrão

btn_entrada = tk.Button(root, text="📂 Selecionar Pasta com PDFs", command=selecionar_pasta_entrada,
                        width=35, bg="#6c63ff", fg="white", font=("Arial", 12, "bold"))
btn_saida = tk.Button(root, text="📂 Selecionar Pasta para Salvar Compactados", command=selecionar_pasta_saida,
                      width=35, bg="#00a86b", fg="white", font=("Arial", 12, "bold"))
btn_iniciar = tk.Button(root, text="▶️ Iniciar Compressão", command=iniciar_compressao,
                        width=35, bg="#ff6f61", fg="white", font=("Arial", 12, "bold"))

status_label = tk.Label(root, textvariable=status_var, fg="white", bg="#222", font=("Arial", 11), wraplength=780, justify="center")
reducao_label = tk.Label(root, textvariable=reducao_var, fg="white", bg="#222", font=("Arial", 12, "bold"), wraplength=780, justify="center")

qualidade_label = tk.Label(root, text="Qualidade da compressão:", fg="white", bg="#222", font=("Arial", 11))
qualidade_menu = tk.OptionMenu(root, qualidade_var, *opcoes_qualidade.keys())
qualidade_menu.config(width=25, bg="#6c63ff", fg="white", font=("Arial", 10, "bold"))

informativo_texto = (
"INFORMATIVOS:\nPARA PDFS COM IMAGENS O IDEAL É ALTA."
"\n\nQUANTO MAIOR A QUALIDADE MENOR A REDUÇÃO DO PDF..."

)
informativo_label = tk.Label(root, text=informativo_texto, fg="white", bg="#ff6f61", font=("Arial", 10), justify="left", anchor="nw")
canvas.create_window(80, 430, window=informativo_label, anchor="nw")


canvas.create_window(400, 40, window=btn_entrada)
canvas.create_window(400, 100, window=btn_saida)
canvas.create_window(400, 160, window=btn_iniciar)

canvas.create_window(120, 220, window=qualidade_label)
canvas.create_window(120, 260, window=qualidade_menu)

canvas.create_window(400, 390, window=status_label, width=780)
canvas.create_window(400, 570, window=reducao_label, width=780)

root.mainloop()
