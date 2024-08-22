import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import locale
import shutil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Configura a localidade para a moeda corrente local
locale.setlocale(locale.LC_ALL, '')

class ImpressaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serviços de Impressão")

        self.status_file = "status.json"

        # Dicionário para armazenar os serviços, quantidades e valores
        self.servicos = {
            "Impressão Colorida": {"quantidade": 0, "valor": 0.0},
            "Cópia Colorida": {"quantidade": 0, "valor": 0.0},
            "Impressão Preto e Branco": {"quantidade": 0, "valor": 0.0},
            "Cópia Preto e Branco": {"quantidade": 0, "valor": 0.0},
            "Impressão Foto 10x15": {"quantidade": 0, "valor": 0.0},
            "Impressão A3 Preto": {"quantidade": 0, "valor": 0.0},
            "Impressão A3 Colorido": {"quantidade": 0, "valor": 0.0},
            "Impressão Foto A4": {"quantidade": 0, "valor": 0.0},
            "Foto 3x4 (4 fotos)": {"quantidade": 0, "valor": 0.0},
            "Foto 3x4 (8 fotos)": {"quantidade": 0, "valor": 0.0},
            "Impressão A3 Foto": {"quantidade": 0, "valor": 0.0},  # Novo serviço adicionado
            "Desperdício": {"quantidade": 0}  # Apenas quantidade
        }

        self.load_status()
        self.create_widgets()

    def load_status(self):
        if os.path.exists(self.status_file):
            with open(self.status_file, "r") as file:
                status = json.load(file)
                if status.get("system_restarted", False):
                    self.reset_calculations()
                    status["system_restarted"] = False
                    self.save_status(status)
                else:
                    self.servicos = status.get("servicos", self.servicos)
        else:
            self.save_status({"system_restarted": False, "servicos": self.servicos})

    def save_status(self, status):
        with open(self.status_file, "w") as file:
            json.dump(status, file, indent=4)

    def reset_calculations(self):
        self.servicos = {servico: {"quantidade": 0, "valor": 0.0 if "valor" in dados else None}
                         for servico, dados in self.servicos.items()}

    def create_widgets(self):
        row = 0
        for servico in self.servicos:
            label = tk.Label(self.root, text=servico, font=('Arial', 10, 'bold'))
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantidade_label = tk.Label(self.root, text="Quantidade:")
            quantidade_label.grid(row=row, column=1, padx=5, pady=5, sticky="e")

            quantidade_entry = tk.Entry(self.root, width=10)
            quantidade_entry.grid(row=row, column=2, padx=5, pady=5)

            valor_entry = None
            if servico != "Desperdício":
                valor_label = tk.Label(self.root, text="Valor (R$):")
                valor_label.grid(row=row, column=3, padx=5, pady=5, sticky="e")

                valor_entry = tk.Entry(self.root, width=10)
                valor_entry.grid(row=row, column=4, padx=5, pady=5)

            add_button = tk.Button(self.root, text="Adicionar", command=lambda s=servico, q=quantidade_entry, v=valor_entry: self.add_servico(s, q, v))
            add_button.grid(row=row, column=5, padx=5, pady=5)

            row += 1

        self.finalizar_button = tk.Button(self.root, text="Finalização Diária", command=self.finalizar_pedido)
        self.finalizar_button.grid(row=row, column=0, columnspan=6, pady=20)

        self.copy_button = tk.Button(self.root, text="Copiar Resumo", command=self.copy_resumo, state=tk.DISABLED)
        self.copy_button.grid(row=row + 1, column=0, columnspan=6, pady=10)

        self.bkp_button = tk.Button(self.root, text="Realizar Backup", command=self.realizar_bkp)
        self.bkp_button.grid(row=row + 2, column=0, columnspan=6, pady=10)

        self.restaurar_button = tk.Button(self.root, text="Restaurar Backup", command=self.restaurar_bkp)
        self.restaurar_button.grid(row=row + 3, column=0, columnspan=6, pady=10)

    def add_servico(self, servico, quantidade_entry, valor_entry):
        try:
            quantidade = int(quantidade_entry.get())
            if quantidade > 0:
                if valor_entry:
                    valor = float(valor_entry.get().replace(',', '.'))
                    self.servicos[servico]["quantidade"] += quantidade
                    self.servicos[servico]["valor"] += quantidade * valor
                else:
                    self.servicos[servico]["quantidade"] += quantidade

                self.save_status({"system_restarted": False, "servicos": self.servicos})
                quantidade_entry.delete(0, tk.END)
                if valor_entry:
                    valor_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Entrada inválida", "Por favor, insira valores válidos para quantidade.")
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Quantidade deve ser um número inteiro e valor deve ser um número decimal.")

    def finalizar_pedido(self):
        total_quantidade = sum(servico["quantidade"] for servico in self.servicos.values())
        total_valor = sum(servico["valor"] for servico in self.servicos.values() if "valor" in servico and servico["valor"] is not None)

        resumo = self.gerar_resumo(total_quantidade, total_valor)

        messagebox.showinfo("Finalização Diária", resumo)

        # Ativa o botão Copiar Resumo
        self.copy_button.config(state=tk.NORMAL)

        # Gera gráfico de colunas e salva como PDF após a finalização
        self.gerar_grafico_pdf()

    def gerar_resumo(self, total_quantidade, total_valor):
        resumo = "Resumo da Finalização Diária:\n"
        for servico, dados in self.servicos.items():
            if "valor" in dados and dados["valor"] is not None:
                valor_formatado = locale.currency(dados['valor'], grouping=True)
                resumo += f"{servico}: {dados['quantidade']} unidades - {valor_formatado}\n"
            else:
                resumo += f"{servico}: {dados['quantidade']} unidades\n"

        resumo += f"\nTotal de Serviços: {total_quantidade} unidades"
        if total_valor > 0:
            valor_formatado = locale.currency(total_valor, grouping=True)
            resumo += f"\nValor Total: {valor_formatado}"

        return resumo

    def copy_resumo(self):
        resumo = self.gerar_resumo(
            sum(servico["quantidade"] for servico in self.servicos.values()),
            sum(servico["valor"] for servico in self.servicos.values() if "valor" in servico and servico["valor"] is not None)
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(resumo)
        self.root.update()  # Mantém a área de transferência

    def gerar_grafico_pdf(self):
        servicos = [servico for servico in self.servicos.keys() if servico != "Desperdício"]
        valores = [dados["valor"] for servico, dados in self.servicos.items() if servico != "Desperdício" and "valor" in dados and dados["valor"] is not None]

        plt.figure(figsize=(10, 6))  # Ajuste o tamanho do gráfico
        plt.bar(servicos, valores, color='skyblue')
        plt.xlabel('Serviços')
        plt.ylabel('Valores (R$)')
        plt.title('Distribuição de Valores dos Serviços')
        plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos no eixo x para melhor visualização
        plt.tight_layout()  # Ajusta o layout para não cortar os rótulos

        # Salva o gráfico em um arquivo PDF
        pdf_filename = "grafico_distribuicao_servicos.pdf"
        with PdfPages(pdf_filename) as pdf:
            pdf.savefig(bbox_inches="tight")  # Salva a figura com todas as legendas visíveis
            plt.close()  # Fecha a figura para liberar memória

        messagebox.showinfo("Gráfico Salvo", f"O gráfico foi salvo como {pdf_filename}.")

        # Abre o arquivo PDF gerado
        os.startfile(pdf_filename)

    def realizar_bkp(self):
        backup_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if backup_file:
            shutil.copy(self.status_file, backup_file)
            messagebox.showinfo("Backup realizado", f"Backup realizado com sucesso em {backup_file}.")

    def restaurar_bkp(self):
        backup_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if backup_file:
            shutil.copy(backup_file, self.status_file)
            self.load_status()
            messagebox.showinfo("Restauração realizada", f"Restauração realizada com sucesso de {backup_file}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImpressaoApp(root)
    root.mainloop()
