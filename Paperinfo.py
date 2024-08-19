import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Função para salvar dados em JSON


def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Função para ler dados de JSON


def read_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para cadastrar cliente


def cadastrar_cliente():
    clientes = read_from_json('clientes.json')

    def salvar_cliente():
        nome = nome_var.get()
        cpf_cnpj = cpf_cnpj_var.get().strip()
        tipo_pessoa = tipo_pessoa_var.get().lower()

        if tipo_pessoa not in ["física", "jurídica"]:
            messagebox.showerror(
                "Erro", "Tipo de pessoa inválido. Use 'física' ou 'jurídica'.")
            return

        if tipo_pessoa == "física":
            if cpf_cnpj in clientes:
                messagebox.showinfo("Cliente Existente", f"Cliente com CPF {
                                    cpf_cnpj} já está cadastrado.\n{clientes[cpf_cnpj]}")
            else:
                clientes[cpf_cnpj] = {
                    "Nome": nome,
                    "Tipo": "Pessoa Física"
                }
                save_to_json(clientes, 'clientes.json')
                messagebox.showinfo(
                    "Sucesso", "Cliente cadastrado com sucesso.")
                limpar_campos()

        elif tipo_pessoa == "jurídica":
            cnpj = cpf_cnpj
            if cnpj in clientes:
                messagebox.showinfo("Cliente Existente", f"Cliente com CNPJ {
                                    cnpj} já está cadastrado.\n{clientes[cnpj]}")
            else:
                clientes[cnpj] = {
                    "Nome": nome,
                    "Tipo": "Pessoa Jurídica"
                }
                save_to_json(clientes, 'clientes.json')
                messagebox.showinfo(
                    "Sucesso", "Cliente cadastrado com sucesso.")
                limpar_campos()

    def limpar_campos():
        nome_var.set("")
        cpf_cnpj_var.set("")
        tipo_pessoa_var.set("")

    cliente_window = tk.Toplevel(root)
    cliente_window.title("Cadastrar Cliente")

    tk.Label(cliente_window, text="Nome completo:").pack(pady=5)
    nome_var = tk.StringVar()
    tk.Entry(cliente_window, textvariable=nome_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(cliente_window, text="CPF (ou CNPJ para pessoa jurídica):").pack(pady=5)
    cpf_cnpj_var = tk.StringVar()
    tk.Entry(cliente_window, textvariable=cpf_cnpj_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(cliente_window,
             text="Tipo de pessoa (física ou jurídica):").pack(pady=5)
    tipo_pessoa_var = tk.StringVar()
    tk.Entry(cliente_window, textvariable=tipo_pessoa_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Button(cliente_window, text="Salvar", command=salvar_cliente,
              font=("Arial", 12)).pack(pady=10)
    tk.Button(cliente_window, text="Limpar", command=limpar_campos,
              font=("Arial", 12)).pack(pady=10)

# Função para cadastrar produto


def cadastro_produto():
    produtos = read_from_json('produtos.json')

    def salvar_produto():
        codigo = codigo_var.get()
        nome = nome_var.get()
        custo = custo_var.get()
        preco_venda = preco_venda_var.get()
        estoque = estoque_var.get()

        produtos[codigo] = {
            "Nome": nome,
            "Custo": custo,
            "Preço de Venda": preco_venda,
            "Estoque": estoque
        }

        save_to_json(produtos, 'produtos.json')
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
        limpar_campos()

    def limpar_campos():
        codigo_var.set("")
        nome_var.set("")
        custo_var.set("")
        preco_venda_var.set("")
        estoque_var.set("")

    produto_window = tk.Toplevel(root)
    produto_window.title("Cadastrar Produto")

    tk.Label(produto_window, text="Código do produto:").pack(pady=5)
    codigo_var = tk.StringVar()
    tk.Entry(produto_window, textvariable=codigo_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(produto_window, text="Nome do produto:").pack(pady=5)
    nome_var = tk.StringVar()
    tk.Entry(produto_window, textvariable=nome_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(produto_window, text="Custo do produto:").pack(pady=5)
    custo_var = tk.DoubleVar()
    tk.Entry(produto_window, textvariable=custo_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(produto_window, text="Preço de venda:").pack(pady=5)
    preco_venda_var = tk.DoubleVar()
    tk.Entry(produto_window, textvariable=preco_venda_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(produto_window, text="Quantidade em estoque:").pack(pady=5)
    estoque_var = tk.IntVar()
    tk.Entry(produto_window, textvariable=estoque_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Button(produto_window, text="Salvar", command=salvar_produto,
              font=("Arial", 12)).pack(pady=10)
    tk.Button(produto_window, text="Limpar", command=limpar_campos,
              font=("Arial", 12)).pack(pady=10)

# Função para remover cliente


def remover_cliente():
    clientes = read_from_json('clientes.json')

    def remover():
        cpf_cnpj = cpf_cnpj_var.get().strip()
        if cpf_cnpj in clientes:
            del clientes[cpf_cnpj]
            save_to_json(clientes, 'clientes.json')
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso.")
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    def limpar_campos():
        cpf_cnpj_var.set("")

    remover_window = tk.Toplevel(root)
    remover_window.title("Remover Cliente")

    tk.Label(remover_window,
             text="Digite o CPF ou CNPJ do cliente a ser removido:").pack(pady=5)
    cpf_cnpj_var = tk.StringVar()
    tk.Entry(remover_window, textvariable=cpf_cnpj_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Button(remover_window, text="Remover", command=remover,
              font=("Arial", 12)).pack(pady=10)
    tk.Button(remover_window, text="Limpar", command=limpar_campos,
              font=("Arial", 12)).pack(pady=10)

# Função para gerar relatórios


def gerar_relatorio():
    produtos = read_from_json('produtos.json')
    df = pd.DataFrame.from_dict(produtos, orient='index')

    filename = filedialog.asksaveasfilename(
        defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if filename:
        df.to_excel(filename, index=False)
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso.")

# Função para criar gráficos


def criar_graficos():
    produtos = read_from_json('produtos.json')
    df = pd.DataFrame.from_dict(produtos, orient='index')

    plt.figure(figsize=(10, 6))
    plt.bar(df['Nome'], df['Estoque'])
    plt.xlabel('Produto')
    plt.ylabel('Estoque')
    plt.title('Estoque de Produtos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para criar ordem de serviço


def cadastrar_ordem_servico():
    servicos = read_from_json('servicos.json')

    def confirmar_ordem():
        id_ordem = str(datetime.now().timestamp()).replace('.', '')
        tipo_equipamento = tipo_equipamento_var.get()
        fabricante = fabricante_var.get()
        modelo = modelo_var.get()
        problema = problema_var.get()
        data_entrada = data_entrada_var.get()

        if not tipo_equipamento or not fabricante or not modelo or not problema or not data_entrada:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        servicos[id_ordem] = {
            "ID Ordem de Serviço": id_ordem,
            "Tipo de Equipamento": tipo_equipamento,
            "Fabricante": fabricante,
            "Modelo": modelo,
            "Problema Relatado": problema,
            "Data de Entrada": data_entrada,
            "Data de Saída": "",
            "Análise Realizada": "",
            "Serviço a ser Realizado": "",
            "Peças a ser Distribuídas": "",
            "Valor da Peça": "",
            "Valor do Serviço Total": "",
            "Status da Análise": "Serviço em aberto"
        }
        save_to_json(servicos, 'servicos.json')
        gerar_pdf_ordem(id_ordem)
        messagebox.showinfo(
            "Sucesso", "Ordem de serviço cadastrada com sucesso.")
        limpar_campos()

    def gerar_pdf_ordem(id_ordem):
        ordem = servicos[id_ordem]

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Ordem de Serviço: {
                 id_ordem}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Tipo de Equipamento: {
                 ordem['Tipo de Equipamento']}", ln=True)
        pdf.cell(200, 10, txt=f"Fabricante: {ordem['Fabricante']}", ln=True)
        pdf.cell(200, 10, txt=f"Modelo: {ordem['Modelo']}", ln=True)
        pdf.cell(200, 10, txt=f"Problema Relatado: {
                 ordem['Problema Relatado']}", ln=True)
        pdf.cell(200, 10, txt=f"Data de Entrada: {
                 ordem['Data de Entrada']}", ln=True)

        pdf_filename = f"ordem_servico_{id_ordem}.pdf"
        pdf.output(pdf_filename)

        messagebox.showinfo(
            "PDF Gerado", f"PDF da ordem de serviço gerado: {pdf_filename}")

    def limpar_campos():
        tipo_equipamento_var.set("")
        fabricante_var.set("")
        modelo_var.set("")
        problema_var.set("")
        data_entrada_var.set("")

    ordem_servico_window = tk.Toplevel(root)
    ordem_servico_window.title("Cadastrar Ordem de Serviço")

    tk.Label(ordem_servico_window, text="Tipo de Equipamento:").pack(pady=5)
    tipo_equipamento_var = tk.StringVar()
    tk.Radiobutton(ordem_servico_window, text="Smartphone",
                   variable=tipo_equipamento_var, value="Smartphone").pack(anchor='w')
    tk.Radiobutton(ordem_servico_window, text="Notebook",
                   variable=tipo_equipamento_var, value="Notebook").pack(anchor='w')
    tk.Radiobutton(ordem_servico_window, text="Desktop",
                   variable=tipo_equipamento_var, value="Desktop").pack(anchor='w')
    tk.Radiobutton(ordem_servico_window, text="Impressora",
                   variable=tipo_equipamento_var, value="Impressora").pack(anchor='w')

    tk.Label(ordem_servico_window, text="Fabricante:").pack(pady=5)
    fabricante_var = tk.StringVar()
    tk.Entry(ordem_servico_window, textvariable=fabricante_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(ordem_servico_window, text="Modelo:").pack(pady=5)
    modelo_var = tk.StringVar()
    tk.Entry(ordem_servico_window, textvariable=modelo_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(ordem_servico_window, text="Problema Relatado:").pack(pady=5)
    problema_var = tk.StringVar()
    tk.Entry(ordem_servico_window, textvariable=problema_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Label(ordem_servico_window, text="Data de Entrada:").pack(pady=5)
    data_entrada_var = tk.StringVar()
    tk.Entry(ordem_servico_window, textvariable=data_entrada_var,
             font=("Arial", 12)).pack(pady=5)

    tk.Button(ordem_servico_window, text="Confirmar",
              command=confirmar_ordem, font=("Arial", 12)).pack(pady=10)
    tk.Button(ordem_servico_window, text="Limpar",
              command=limpar_campos, font=("Arial", 12)).pack(pady=10)

# Função para criar a interface com abas


def criar_interface():
    global root
    root = tk.Tk()
    root.title("Sistema PAPERINFOTEC")

    font_size = 14  # Tamanho de fonte aumentado em 33% (originalmente 10)

    # Notebook (abas)
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky='nsew')

    # Configurar responsividade
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Abas
    aba_cliente = ttk.Frame(notebook)
    notebook.add(aba_cliente, text="Cadastrar Cliente")

    aba_produto = ttk.Frame(notebook)
    notebook.add(aba_produto, text="Cadastrar Produto")

    aba_remover = ttk.Frame(notebook)
    notebook.add(aba_remover, text="Remover Cliente")

    aba_ordem_servico = ttk.Frame(notebook)
    notebook.add(aba_ordem_servico, text="Cadastrar Ordem de Serviço")

    aba_relatorio = ttk.Frame(notebook)
    notebook.add(aba_relatorio, text="Gerar Relatório")

    aba_graficos = ttk.Frame(notebook)
    notebook.add(aba_graficos, text="Criar Gráficos")

    # Configurar abas para usar pack com expand=True
    for aba in [aba_cliente, aba_produto, aba_remover, aba_ordem_servico, aba_relatorio, aba_graficos]:
        aba.pack(fill='both', expand=True)

    # Botões na aba de Cadastro de Cliente
    tk.Button(
        aba_cliente, text="Cadastrar Cliente", command=cadastrar_cliente, font=("Arial", font_size)
    ).pack(pady=10)

    # Botões na aba de Cadastro de Produto
    tk.Button(
        aba_produto, text="Cadastrar Produto", command=cadastro_produto, font=("Arial", font_size)
    ).pack(pady=10)

    # Botões na aba de Remover Cliente
    tk.Button(
        aba_remover, text="Remover Cliente", command=remover_cliente, font=("Arial", font_size)
    ).pack(pady=10)

    # Botões na aba de Cadastrar Ordem de Serviço
    tk.Button(
        aba_ordem_servico, text="Cadastrar Ordem de Serviço", command=cadastrar_ordem_servico, font=("Arial", font_size)
    ).pack(pady=10)

    # Botões na aba de Gerar Relatório
    tk.Button(
        aba_relatorio, text="Gerar Relatório", command=gerar_relatorio, font=("Arial", font_size)
    ).pack(pady=10)

    # Botões na aba de Criar Gráficos
    tk.Button(
        aba_graficos, text="Criar Gráficos", command=criar_graficos, font=("Arial", font_size)
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    criar_interface()
