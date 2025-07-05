from tkinter import Entry, END, messagebox
from tkinter.ttk import Combobox

class GUIComponents:
    @staticmethod
    def clear_entries(*entries):
        for entry in entries:
            if isinstance(entry, Entry):
                entry.delete(0, END)
            elif isinstance(entry, Combobox):
                entry.set('') # Clear combobox selection

    @staticmethod
    def show_info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title, message):
        messagebox.showwarning(title, message)

    @staticmethod
    def ask_yes_no(title, message):
        return messagebox.askyesno(title, message)

    @staticmethod
    def validate_not_empty(value, field_name):
        if not value.strip():
            GUIComponents.show_warning("Campo Vazio", f"O campo '{field_name}' não pode estar vazio.")
            return False
        return True

    @staticmethod
    def validate_email(email):
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            GUIComponents.show_warning("Email Inválido", "Por favor, insira um endereço de e-mail válido.")
            return False
        return True

    @staticmethod
    def validate_cpf(cpf):
        # Simplistic CPF validation for demonstration. A real one would be more complex.
        if not cpf.isdigit() or len(cpf) != 11:
            GUIComponents.show_warning("CPF Inválido", "O CPF deve conter 11 dígitos numéricos.")
            return False
        return True

    @staticmethod
    def validate_cnpj(cnpj):
        # Simplistic CNPJ validation for demonstration. A real one would be more complex.
        if not cnpj.isdigit() or len(cnpj) != 14:
            GUIComponents.show_warning("CNPJ Inválido", "O CNPJ deve conter 14 dígitos numéricos.")
            return False
        return True

    @staticmethod
    def validate_phone(phone):
        # Allows digits, spaces, hyphens, and parentheses
        import re
        if not re.match(r"^[0-9\s\-()]+$", phone):
            GUIComponents.show_warning("Telefone Inválido", "O telefone contém caracteres inválidos.")
            return False
        return True

    @staticmethod
    def validate_date(date_str):
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%m/%d/%Y") # Assuming DD/MM/YYYY format
            return True
        except ValueError:
            GUIComponents.show_warning("Data Inválida", "Formato de data inválido. Use DD/MM/YYYY.")
            return False




