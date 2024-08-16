import csv
import os
from pathlib import Path
from datetime import datetime
import customtkinter as ctk
import tkinter as tk


def salvar_relatorio(tabela, children, columns, tree):
    table_data = []
    headers = [x.ljust(25) for x in tree['columns']]
    headers[-1] += '\n'
    table_data.append(headers)
    # Itera sobre os itens filhos (children) da tabela
    for item in children:
        row_data = []
        # Para cada coluna, obtenha o texto da célula
        for col in range(columns):
            cell_text = tree.item(item, 'values')[col] if col < len(tree.item(item, 'values')) else ''
            row_data.append(cell_text.ljust(25))
        table_data.append(row_data)

    # Formata a data e hora para o nome do arquivo
    data = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    file_name = f"relatorio_{tabela}_{data}.txt"

    # Define o caminho completo do arquivo
    desktop_path = Path.home() / "Desktop"
    reports_dir = desktop_path / "Relatorios_ERP"
    reports_dir.mkdir(parents=True, exist_ok=True)
    file_path = reports_dir / file_name

    # Grava os dados no arquivo
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerows(table_data)