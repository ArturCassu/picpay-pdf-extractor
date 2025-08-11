import pdfplumber
import re
from typing import Dict

class PDFExtractor:
    """
    Extracts structured data from a PicPay PDF statement.
    """

    FOOTER_PREFIXES = (
        "Extrato gerado em",
        "PicPay Serviços S.A.",
        "CNPJ:",
        "Se você ficou com alguma dúvida",
        "Dias úteis",
        "Telefone:",
    )
    PAGE_NUMBER_RE = re.compile(r"^\d+ de \d+$")

    def __init__(self, pdf_path: str):
        """
        Initialize the extractor with the path to the PDF file.
        """
        self.pdf_path = pdf_path
        # Regex to extract transaction fields from cleaned text
        self.pattern = re.compile(
            r"""
            (?P<data>\d{2}/\d{2}/\d{4})                # Date: 30/07/2025
            \s+
            (?P<descricao>[^\n]+?)                     # Description (up to next field)
            \s+
            (?P<valor>-?\s*R\$?\s?[\d.,]+|-)           # Value
            \s+
            (?P<saldo>-?\s*R\$?\s?[\d.,]+|-)           # Balance
            \s+
            (?P<saldo_sacavel>-?\s*R\$?\s?[\d.,]+|-)   # Withdrawable balance
            \s+
            (?P<hora>\d{2}:\d{2}:\d{2})                # Time: 13:04:35
            """,
            re.DOTALL | re.VERBOSE
        )
        # Regexes for header fields
        self.re_usuario = re.compile(r"@([^\s]+)")
        self.re_nome = re.compile(r"\n([A-Z ]{5,})\n")
        self.re_cpf = re.compile(r"CPF:\s*([\d\.\-]+)")
        self.re_agencia = re.compile(r"Agência:\s*(\d+)")
        self.re_conta = re.compile(r"Conta:\s*(\d+)")
        self.re_cliente_desde = re.compile(r"Cliente desde:\s*(\d{2}/\d{2}/\d{4})")

    def remove_footers(self, texto: str) -> str:
        """
        Remove known footer lines and page numbers from the extracted text.
        """
        lines = texto.splitlines()
        cleaned = []
        for line in lines:
            line_stripped = line.strip()
            if any(line_stripped.startswith(prefix) for prefix in self.FOOTER_PREFIXES):
                continue
            if self.PAGE_NUMBER_RE.match(line_stripped):
                continue
            cleaned.append(line)
        return "\n".join(cleaned)


    def normaliza_valor(self, valor_str: str) -> float:
        """
        Convert a currency string to a float. Returns 0.0 if invalid or empty.
        """
        if valor_str == "-" or not valor_str:
            return 0.0
        valor_str = valor_str.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")
        try:
            return float(valor_str)
        except Exception:
            return 0.0

    def extract_data(self) -> Dict:
        """
        Extract all relevant data from the PDF and return as a dictionary.
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            texto_completo = "\n".join(page.extract_text() for page in pdf.pages)
        texto_completo = self.remove_footers(texto_completo)

        usuario = self.re_usuario.search(texto_completo).group(1)
        nome = self.re_nome.search(texto_completo).group(1).strip()
        cpf = self.re_cpf.search(texto_completo).group(1)
        agencia = self.re_agencia.search(texto_completo).group(1)
        conta = self.re_conta.search(texto_completo).group(1)
        cliente_desde = self.re_cliente_desde.search(texto_completo).group(1)

        transacoes = []
        for match in self.pattern.finditer(texto_completo):
            data = match.group("data")
            descricao = match.group("descricao").replace("\n", " ").strip()
            valor = match.group("valor").strip()
            saldo = match.group("saldo").strip()
            saldo_sacavel = match.group("saldo_sacavel").strip()
            hora = match.group("hora")

            if descricao:
                transacoes.append([
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
            "transacoes": transacoes
        }