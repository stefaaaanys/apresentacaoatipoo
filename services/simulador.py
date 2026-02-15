from models.tipo_imovel import TipoImovel
from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

class SimuladorAluguel:

    def __init__(self):
        self.contrato = 2000.00
        self.kitnet = 1200.00
        self.casa1 = 900.00
        self.casa2 = 1150.00
        self.apartamento1 = 700.00
        self.apartamento2 = 900.00
        self.garagem = 300.00
        self.desconto_filhos = 0.95
        self.vagas_padrao = 250.00
        self.vaga = 60.00

    def calcular_valor_aluguel(self, imovel, quartos, garagem_op, filhos, qtd_vagas):

        if imovel == TipoImovel.KITNET:
            if not garagem_op:
                valor = self.kitnet
            else:
                if qtd_vagas <= 2:
                    valor = self.kitnet + self.vagas_padrao
                else:
                    valor = self.kitnet + self.vagas_padrao + ((qtd_vagas - 2) * self.vaga)

        elif imovel == TipoImovel.APARTAMENTO:
            valor = self.apartamento1 if quartos == 1 else self.apartamento2
            if garagem_op:
                valor += self.garagem
            if not filhos:
                valor *= self.desconto_filhos

        elif imovel == TipoImovel.CASA:
            valor = self.casa1 if quartos == 1 else self.casa2
            if garagem_op:
                valor += self.garagem

        return round(valor, 2)


    def gerar_orcamento_12_meses(self, valor_aluguel, parcelas):
        from datetime import datetime
        from calendar import month_name
        
        if parcelas < 1 or parcelas > 5:
            raise ValueError("O número de parcelas deve estar entre 1 e 5.")

        orcamento = {}

        hoje = datetime.now()
        ano = hoje.year
        mes_atual = hoje.month

        if parcelas > 1:
            valor_parcela = round(self.contrato / parcelas, 2)
        else:
            valor_parcela = self.contrato

        for i in range(12):
            mes_calculado = mes_atual + i
            ano_calculado = ano

            # Ajuste de virada de ano
            if mes_calculado > 12:
                mes_calculado -= 12
                ano_calculado += 1

            nome_mes = month_name[mes_calculado]

            if parcelas <= 1:
                if i == 0:
                    valor = valor_aluguel + self.contrato
                else:
                    valor = valor_aluguel
            else:
                if i < parcelas:
                    valor = valor_aluguel + valor_parcela
                else:
                    valor = valor_aluguel

            chave = f"{nome_mes}/{ano_calculado}"
            orcamento[chave] = round(valor, 2)

        return orcamento
