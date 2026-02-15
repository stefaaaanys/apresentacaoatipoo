import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox

from services.simulador import SimuladorAluguel
from models.tipo_imovel import TipoImovel

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Simulador de Orçamento de Aluguel")
        self.geometry("450x740")

        self.simulador = SimuladorAluguel()

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("green")

        self.criar_widgets()

    def criar_widgets(self):

        ctk.CTkLabel(self, text="Simulador de Aluguel",text_color="#8FC1B5", font=("Arial", 18, "bold")).pack(pady=15)

        # Imóvel
        ctk.CTkLabel(self, text="Tipo de imóvel").pack(pady=3)
        self.combo_imovel = ctk.CTkComboBox(
            self,
            values=[tipo.value for tipo in TipoImovel],
            state="readonly",
            command=self.atualizar_campos
        )
        self.combo_imovel.set(TipoImovel.CASA.value)
        self.combo_imovel.pack(pady=3)

        # Quartos
        ctk.CTkLabel(self, text="Quantidade de quartos").pack(pady=3)
        self.combo_quartos = ctk.CTkComboBox(
            self,
            values=["1","2"]
        )

        self.combo_quartos.set("1")  # valor inicial
        self.combo_quartos.pack(pady=3)

        # Garagem
        self.garagem_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Incluir garagem", variable=self.garagem_var).pack(pady=5)

        # Vagas
        ctk.CTkLabel(self, text="Quantidade de vagas (Válido no Kitnet)").pack(pady=3)
        self.entry_vagas = ctk.CTkEntry(self)
        self.entry_vagas.insert(0, "2")
        self.entry_vagas.pack(pady=3)

        # Filhos
        self.filhos_var = ctk.BooleanVar()
        self.checkbox_filhos = ctk.CTkCheckBox(
            self,
            text="Possui filhos (Válido no Apartamento)",
            variable=self.filhos_var
        )
        self.checkbox_filhos.pack(pady=3)


        # Parcelas
        ctk.CTkLabel(self, text="Parcelas do contrato").pack(pady=3)
        self.combo_parcelas= ctk.CTkComboBox(
            self,
            values=["1", "2", "3","4","5"]
        )

        self.combo_parcelas.set("1")  # valor inicial
        self.combo_parcelas.pack(pady=3)

        # Botão
        ctk.CTkButton(self, text="Simular orçamento", command=self.simular).pack(pady=10)

        # Resultado
        self.resultado = ctk.CTkTextbox(
            self,
            width=400,
            height=300,
            font=("Consolas", 15)
        )
        self.resultado.pack(pady=10)

        self.atualizar_campos(self.combo_imovel.get())

    def atualizar_campos(self, escolha):
        tipo = TipoImovel(escolha)

        # Vagas só para KITNET
        if tipo == TipoImovel.KITNET:
            self.entry_vagas.configure(state="normal")
        else:
            self.entry_vagas.delete(0, tk.END)
            self.entry_vagas.insert(0, "0")
            self.entry_vagas.configure(state="disabled")

        # Filhos só para APARTAMENTO
        if tipo == TipoImovel.APARTAMENTO:
            self.filhos_var.set(False)
            # habilita checkbox
            self.checkbox_filhos.configure(state="normal")
        else:
            self.filhos_var.set(False)
            self.checkbox_filhos.configure(state="disabled")


    def simular(self):
        try:
            imovel_str = self.combo_imovel.get()
            imovel = TipoImovel(imovel_str)
            quartos = int(self.combo_quartos.get())
            parcelas = int(self.combo_parcelas.get())
            garagem_op = self.garagem_var.get()
            qtd_vagas = int(self.entry_vagas.get())

            filhos = self.filhos_var.get()

            valor_aluguel = self.simulador.calcular_valor_aluguel(
                imovel, quartos, garagem_op, filhos, qtd_vagas
            )

            orcamento = self.simulador.gerar_orcamento_12_meses(valor_aluguel, parcelas)

            self.resultado.delete("1.0", tk.END)
            self.resultado.insert(tk.END, f"Valor do aluguel: R$ {valor_aluguel:.2f}\n\n")

            for mes, valor in orcamento.items():
                self.resultado.insert(tk.END, f"{mes}: R$ {valor:.2f}\n")

        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores inseridos.")