import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os
import webbrowser
import datetime

# --- Variáveis Globais ---
tabela = None

# --- Funções de Upload ---
def adicionar_ocorrencia_na_tabela(nome_arquivo):
    """Adiciona uma nova ocorrência à lista de dados e atualiza a tabela."""
    global tabela

    data_e_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nova_ocorrencia = {
        "data": data_e_hora_atual,
        "tipo": "Automático",
        "tempo": "0.00s", # Tempo é um valor de demonstração
        "link": nome_arquivo
    }
    ocorrencias_data.append(nova_ocorrencia)

    if tabela and tabela.winfo_exists():
        tabela.insert("", "end", values=(
            nova_ocorrencia["data"],
            nova_ocorrencia["tipo"],
            nova_ocorrencia["tempo"],
            nova_ocorrencia["link"]
        ))
    else:
        mudar_pagina("Ocorrências", "Conteúdo da página de ocorrências.", "ocorrencias")

def upload_arquivo_ocorrencia():
    """Abre um diálogo para o usuário selecionar um arquivo e adiciona à tabela."""
    try:
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de ocorrência",
            filetypes=[("Arquivos de Vídeo", "*.mp4;*.avi;*.mov"),
                       ("Todos os arquivos", "*.*")]
        )
        if filepath:
            nome_do_arquivo = os.path.basename(filepath)
            adicionar_ocorrencia_na_tabela(nome_do_arquivo)
            messagebox.showinfo(
                "Upload Selecionado", 
                f"Arquivo selecionado e adicionado à tabela:\n{filepath}\n\n(Simulação de envio)"
            )
        else:
            messagebox.showinfo("Nenhum Arquivo Selecionado", "O upload foi cancelado.")
    except Exception as e:
        messagebox.showerror("Erro de Upload", f"Ocorreu um erro: {e}")

# --- Funções de Download (Mantidas, mas sem botão no cabeçalho) ---
def salvar_arquivo_mp4():
    """Chama a função de salvar para um arquivo de vídeo."""
    url_do_arquivo = "http://techslides.com/demos/sample-videos/small.mp4"
    nome_padrao = "video_exemplo.mp4"
    salvar_arquivo(url_do_arquivo, nome_padrao)

def salvar_arquivo(url, nome_arquivo):
    """Baixa um arquivo de uma URL e salva no local escolhido pelo usuário."""
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".*",
            initialfile=nome_arquivo,
            filetypes=[("Todos os arquivos", "*.*"), ("Vídeos MP4", "*.mp4")],
        )
        if not filepath:
            return
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        messagebox.showinfo("Download Concluído", f"Arquivo salvo com sucesso em:\n{filepath}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Download", f"Erro ao baixar o arquivo: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

# --- Função de Impressão ---
def imprimir_pagina():
    """Simula a impressão de uma página."""
    messagebox.showinfo("Imprimir", "A função de impressão foi acionada!")

# --- Dados de exemplo para a tabela de ocorrências ---
ocorrencias_data = [
    {"data": "2025-12-09 10:30:00", "tipo": "Baixa", "tempo": "2.14s", "link": "corte1.mp4"},
    {"data": "2025-12-10 14:15:00", "tipo": "Média", "tempo": "5.30s", "link": "corte2.mp4"},
    {"data": "2025-12-11 08:45:00", "tipo": "Alta", "tempo": "1.55s", "link": "corte3.mp4"},
    {"data": "2025-12-12 22:00:00", "tipo": "Baixa", "tempo": "3.88s", "link": "corte4.mp4"},
]

# --- Função para abrir o link do corte ---
def abrir_link_corte(event):
    """Abre o arquivo de vídeo associado à linha da tabela clicada."""
    item_selecionado = tabela.focus()
    if item_selecionado:
        valores = tabela.item(item_selecionado, 'values')
        link_do_corte = valores[3]
        
        caminho_completo = os.path.join(os.getcwd(), "corte", link_do_corte)
        
        try:
            webbrowser.open(caminho_completo)
        except Exception as e:
            messagebox.showerror("Erro ao Abrir Arquivo", f"Não foi possível abrir o arquivo:\n{caminho_completo}\n\nErro: {e}")

# --- Função para criar a tabela de ocorrências ---
def criar_tabela_ocorrencias(frame_pai):
    """Cria e preenche uma tabela (Treeview) com dados de ocorrências."""
    global tabela
    
    colunas = ("data", "tipo", "tempo", "link")
    tabela = ttk.Treeview(frame_pai, columns=colunas, show="headings")
    tabela.heading("data", text="Data da Ocorrência")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("tempo", text="Tempo")
    tabela.heading("link", text="Link do Corte")
    
    tabela.column("data", width=180, anchor="center")
    tabela.column("tipo", width=100, anchor="center")
    tabela.column("tempo", width=100, anchor="center")
    tabela.column("link", width=250, anchor="center")
    
    for item in ocorrencias_data:
        tabela.insert("", "end", values=(item["data"], item["tipo"], item["tempo"], item["link"]))
    
    tabela.pack(side="left", fill="both", expand=True)
    
    tabela.bind("<Double-1>", abrir_link_corte)
    
    return tabela

# --- Função para mudar o conteúdo da página ---
def mudar_pagina(titulo, texto, pagina_id=None):
    """
    Limpa o conteúdo anterior e exibe um novo conteúdo no frame principal.
    Adiciona um `pagina_id` para identificar qual tela exibir.
    """
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    ttk.Label(main_content_frame, text=titulo, font=('Arial', 16, 'bold')).pack(pady=10)

    if pagina_id == "ocorrencias":
        criar_tabela_ocorrencias(main_content_frame)
    else:
        ttk.Label(main_content_frame, text=texto, wraplength=500).pack(padx=20, pady=10)

# --- Criar a janela principal ---
janela = ThemedTk(theme="adapta")
janela.title("Globo.com")
janela.geometry("800x600")

# --- Estilos personalizados ---
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TLabel', font=('Helvetica', 10))

# --- Estrutura de Layout ---
header_frame = ttk.Frame(janela, style='TFrame')
header_frame.pack(fill='x', side='top', pady=5)
header_frame.grid_rowconfigure(0, weight=1)
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=5)
header_frame.grid_columnconfigure(2, weight=1)

main_layout_frame = ttk.Frame(janela, style='TFrame')
main_layout_frame.pack(fill='both', expand=True, padx=10, pady=10)

sidebar_frame = ttk.Frame(main_layout_frame, style='TFrame', width=200)
sidebar_frame.pack(fill='y', side='left', padx=10, pady=10)

main_content_frame = ttk.Frame(main_layout_frame, style='TFrame')
main_content_frame.pack(fill='both', expand=True, padx=10, pady=10)

# --- Carregar e exibir imagem do logotipo ---
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "img", "globosf.png")
    if not os.path.exists(img_path):
        img_path = os.path.join("img", "globosf.png")
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {img_path}")
    img = Image.open(img_path)
    img = img.resize((80, 80), Image.LANCZOS)
    logo_globo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(header_frame, image=logo_globo)
    logo_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    logo_label.image = logo_globo
    try:
        janela.iconphoto(False, logo_globo)
    except Exception as e:
        print(f"Não foi possível definir o ícone da janela: {e}")
except FileNotFoundError as e:
    print(f"ERRO: {e}. Verifique se a imagem está na pasta 'img' no mesmo nível do seu script.")
    logo_globo = None
except Exception as e:
    print(f"Erro ao carregar ou processar imagem: {e}")
    logo_globo = None

# --- Título e Botões do Cabeçalho ---
title_label = ttk.Label(header_frame, text="Globo.com", font=("Arial", 14, 'bold'), foreground="#453CF3")
title_label.grid(row=0, column=1, pady=(5, 0))
header_buttons_frame = ttk.Frame(header_frame, style='TFrame')
header_buttons_frame.grid(row=0, column=2, padx=10, pady=5, sticky='e')
ttk.Button(header_buttons_frame, text="IMPRIMIR RELATÓRIO", command=imprimir_pagina).pack(side="left", padx=5)
ttk.Button(header_buttons_frame, text="ENVIAR CLIP OCORRÊNCIA", command=upload_arquivo_ocorrencia).pack(side="left", padx=5)

# --- Conteúdo da Barra Lateral ---
menu_opcoes = [
    ("Menu Principal", lambda: mudar_pagina("Página Principal", "Conteúdo principal da Globo.com.")),
    ("Ocorrências", lambda: mudar_pagina("Ocorrências", "Conteúdo da página de ocorrências.", "ocorrencias")),
    ("Relatórios", lambda: mudar_pagina("Relatórios", "Conteúdo da página de relatórios.")),
    ("Documentação", lambda: mudar_pagina("Documentação", "Conteúdo da página de documentação."))
]

for texto, comando in menu_opcoes:
    ttk.Button(sidebar_frame, text=texto, command=comando, width=25).pack(pady=5, padx=10)

# Exibe a página principal ao iniciar
mudar_pagina("Página Principal", "Conteúdo inicial da Globo.com.")

# --- Loop principal ---
janela.mainloop()