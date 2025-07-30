import pdfplumber
import re
from typing import Dict

class PDFExtractor:    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pattern = re.compile(
            r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?\s*R\$?\s?[\d.,]+|-)\s+(-?\s*R\$?\s?[\d.,]+|-)\s+(-?\s*R\$?\s?[\d.,]+|-)\s+(\d{2}:\d{2}:\d{2})",
            re.DOTALL
        )
        self.re_usuario = re.compile(r"@([^\s]+)")
        self.re_nome = re.compile(r"\n([A-Z ]{5,})\n")
        self.re_cpf = re.compile(r"CPF:\s*([\d\.\-]+)")
        self.re_agencia = re.compile(r"Agência:\s*(\d+)")
        self.re_conta = re.compile(r"Conta:\s*(\d+)")
        self.re_cliente_desde = re.compile(r"Cliente desde:\s*(\d{2}/\d{2}/\d{4})")

    def limpa_descricao(self, descricao: str) -> str:
        # Remove unwanted footer/header patterns from description
        unwanted_patterns = [
            "PicPay Serviços S.A.",
            "CNPJ:",
            "Ouvidoria",
            "Telefone:",
            "Cliente desde:",
            "MOVIMENTAÇÕES",
            "Agência:",
            "Conta:",
            "CPF:",
            "de 3",
            "@",
            "Dias úteis",
            "Se você ficou com alguma dúvida",
        ]
        for pattern in unwanted_patterns:
            idx = descricao.find(pattern)
            if idx != -1:
                descricao = descricao[:idx].strip()
        return descricao

    def normaliza_valor(self, v: str) -> float:
        if v == "-" or not v:
            return 0.0
        v = v.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")
        try:
            return float(v)
        except:
            return 0.0

    def extract_data(self) -> Dict:
        with pdfplumber.open(self.pdf_path) as pdf:
            texto_completo = "\n".join(page.extract_text() for page in pdf.pages)

        usuario = self.re_usuario.search(texto_completo).group(1)
        nome = self.re_nome.search(texto_completo).group(1).strip()
        cpf = self.re_cpf.search(texto_completo).group(1)
        agencia = self.re_agencia.search(texto_completo).group(1)
        conta = self.re_conta.search(texto_completo).group(1)
        cliente_desde = self.re_cliente_desde.search(texto_completo).group(1)

        dados = []
        for match in self.pattern.finditer(texto_completo):
            data = match.group(1)
            descricao = match.group(2).replace("\n", " ").strip()
            descricao = self.limpa_descricao(descricao)
            valor = match.group(3).strip()
            saldo = match.group(4).strip()
            saldo_sacavel = match.group(5).strip()
            hora = match.group(6)

            dados.append([
                data, hora, descricao, valor, saldo, saldo_sacavel,
                self.normaliza_valor(valor),
                self.normaliza_valor(saldo),
                self.normaliza_valor(saldo_sacavel)
            ])

        return {
            "usuario": usuario,
            "nome": nome,
            "cpf": cpf,
            "agencia": agencia,
            "conta": conta,
            "cliente_desde": cliente_desde,
            "transacoes": dados
        }