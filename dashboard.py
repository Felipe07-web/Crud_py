import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Controle Financeiro")
        self.master.geometry("800x600")  # Ajuste o tamanho da janela

        # Dados iniciais
        self.dados = []
        self.orcamento_inicial = 0.0

        # Categorias e Tipos
        self.categorias = [
            "Aluguel", "Condomínio", "Energia Elétrica", "Água", "Gás",
            "Supermercado", "Restaurantes", "Lanches",
            "Combustível", "Transporte Público", "Manutenção do Veículo",
            "Plano de Saúde", "Consultas", "Medicamentos",
            "Mensalidade Escolar", "Cursos", "Livros",
            "Cinema", "Viagens", "Atividades Recreativas",
            "Roupas", "Eletrônicos", "Móveis",
            "Empréstimos", "Juros", "Investimentos",
            "Diversos", "Presentes", "Doações", "Salário"
        ]
        
        self.tipos = [
            "Receita", "Despesa"
        ]

        # Frame para campos de entrada e botões
        self.frame_inputs = tk.Frame(master)
        self.frame_inputs.pack(padx=10, pady=10, fill=tk.X)

        # Layout Grid para entradas
        self.frame_inputs.grid_columnconfigure(0, weight=1)
        self.frame_inputs.grid_columnconfigure(1, weight=1)
        self.frame_inputs.grid_columnconfigure(2, weight=1)
        self.frame_inputs.grid_columnconfigure(3, weight=1)
        self.frame_inputs.grid_columnconfigure(4, weight=1)
        self.frame_inputs.grid_columnconfigure(5, weight=1)
        self.frame_inputs.grid_rowconfigure(0, weight=1)
        self.frame_inputs.grid_rowconfigure(1, weight=1)

        # Criar widgets
        self.label_data = tk.Label(self.frame_inputs, text="Data:")
        self.label_data.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_data = tk.Entry(self.frame_inputs, width=15)
        self.entry_data.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.label_categoria = tk.Label(self.frame_inputs, text="Categoria:")
        self.label_categoria.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.combobox_categoria = ttk.Combobox(self.frame_inputs, values=self.categorias, state="readonly", width=15)
        self.combobox_categoria.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        self.label_descricao = tk.Label(self.frame_inputs, text="Descrição:")
        self.label_descricao.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_descricao = tk.Entry(self.frame_inputs, width=15)
        self.entry_descricao.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)

        self.label_valor = tk.Label(self.frame_inputs, text="Valor:")
        self.label_valor.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_valor = tk.Entry(self.frame_inputs, width=15)
        self.entry_valor.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)

        self.label_tipo = tk.Label(self.frame_inputs, text="Tipo:")
        self.label_tipo.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_tipo = ttk.Combobox(self.frame_inputs, values=self.tipos, state="readonly", width=15)
        self.combobox_tipo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.botao_adicionar = tk.Button(self.frame_inputs, text="Adicionar Entrada", command=self.adicionar_entrada)
        self.botao_adicionar.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.botao_apagar = tk.Button(self.frame_inputs, text="Apagar Selecionado", command=self.apagar_entrada)
        self.botao_apagar.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Frame para a tabela
        self.frame_table = tk.Frame(master)
        self.frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.frame_table, columns=("Data", "Categoria", "Descrição", "Valor", "Tipo"), show='headings', selectmode='browse')
        self.tree.heading("Data", text="Data")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Tipo", text="Tipo")

        self.tree.column("Data", width=100, anchor=tk.W)
        self.tree.column("Categoria", width=150, anchor=tk.W)
        self.tree.column("Descrição", width=200, anchor=tk.W)
        self.tree.column("Valor", width=100, anchor=tk.E)
        self.tree.column("Tipo", width=100, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Label para saldo atual
        self.label_saldo = tk.Label(master, text=f"Saldo Atual: {self.orcamento_inicial:.2f}")
        self.label_saldo.pack(padx=10, pady=10, anchor=tk.W)

        self.calcular_orcamento()

    def criar_conexao(self):
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='admin',
                database='db_sgp',
                port=3300
            )
            if conexao.is_connected():
                return conexao
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao MySQL: {e}")
            return None

    def validar_data(self, data):
        try:
            data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            return data_formatada
        except ValueError:
            messagebox.showerror("Erro", "Data deve estar no formato DD/MM/AAAA!")
            return None

    def adicionar_entrada(self):
        data = self.entry_data.get()
        categoria = self.combobox_categoria.get()
        descricao = self.entry_descricao.get()
        valor = self.entry_valor.get()
        tipo = self.combobox_tipo.get()

        if not data or not categoria or not descricao or not valor or not tipo:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos!")
            return

        data_formatada = self.validar_data(data)
        if not data_formatada:
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número!")
            return

        if tipo not in self.tipos:
            messagebox.showerror("Erro", "Tipo deve ser 'Receita' ou 'Despesa'!")
            return

        # Adicionar dados ao banco de dados
        self.inserir_dado(data_formatada, categoria, descricao, valor, tipo)

        # Adicionar dados à lista e atualizar a visualização
        self.dados.append({
            "Data": data_formatada,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor": valor,
            "Tipo": tipo
        })

        self.tree.insert("", tk.END, values=(data_formatada, categoria, descricao, valor, tipo))
        self.limpar_campos()
        self.calcular_orcamento()

    def apagar_entrada(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhuma entrada selecionada!")
            return

        item_id = selected_item[0]
        item_values = self.tree.item(item_id, "values")

        # Remove item do banco de dados
        self.apagar_dado(item_values[0], item_values[1], item_values[2], float(item_values[3]), item_values[4])

        # Remove item da lista de dados
        self.dados = [item for item in self.dados if item["Data"] != item_values[0] or item["Categoria"] != item_values[1] or item["Descrição"] != item_values[2] or item["Valor"] != float(item_values[3]) or item["Tipo"] != item_values[4]]

        # Remove item da visualização
        self.tree.delete(item_id)

        self.calcular_orcamento()

    def calcular_orcamento(self):
        receitas_totais = sum(item["Valor"] for item in self.dados if item["Tipo"] == "Receita")
        despesas_totais = sum(item["Valor"] for item in self.dados if item["Tipo"] == "Despesa")
        saldo_atual = self.orcamento_inicial + receitas_totais - despesas_totais

        self.label_saldo.config(text=f"Saldo Atual: {saldo_atual:.2f}")

    def limpar_campos(self):
        self.entry_data.delete(0, tk.END)
        self.combobox_categoria.set('')
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.combobox_tipo.set('')

    def inserir_dado(self, data, categoria, descricao, valor, tipo):
        conexao = self.criar_conexao()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO entradas (data, categoria, descricao, valor, tipo)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (data, categoria, descricao, valor, tipo)
            try:
                cursor.execute(query, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Entrada adicionada com sucesso!")
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao inserir dados: {e}")
            finally:
                cursor.close()
                conexao.close()

    def apagar_dado(self, data, categoria, descricao, valor, tipo):
        conexao = self.criar_conexao()
        if conexao:
            cursor = conexao.cursor()
            query = """
                DELETE FROM entradas
                WHERE data = %s AND categoria = %s AND descricao = %s AND valor = %s AND tipo = %s
            """
            valores = (data, categoria, descricao, valor, tipo)
            try:
                cursor.execute(query, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Entrada apagada com sucesso!")
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao apagar dados: {e}")
            finally:
                cursor.close()
                conexao.close()
