import pickle
import PySimpleGUI as sg

# Dicionário de vacinas
VACINAS = {
    "Hepatite B": {
        "doses": 3,
        "intervalo": 30
    },
    "DTaP": {
        "doses": 5,
        "intervalo": 60
    },
    "Febre Amarela": {
        "doses": 1,
        "intervalo": 10
    }
}

# Função para carregar os dados do paciente
def carregar_dados(cpf):
    try:
        with open(f"paciente_{cpf}.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Função para salvar os dados do paciente
def salvar_dados(cpf, dados):
    with open(f"paciente_{cpf}.pkl", "wb") as f:
        pickle.dump(dados, f)

# Função para registrar uma nova vacina
def registrar_vacina(cpf, nome_vacina, data_aplicacao, lote, dose):
    dados = carregar_dados(cpf)
    if dados is None:
        dados = {"vacinas": {}}
    vacinas = dados["vacinas"]
    if nome_vacina not in vacinas:
        vacinas[nome_vacina] = []
    vacinas[nome_vacina].append({"data": data_aplicacao, "lote": lote, "dose": dose})
    salvar_dados(cpf, dados)

# Função para calcular a próxima dose
def calcular_proxima_dose(nome_vacina, data_aplicacao, dose):
    doses = VACINAS[nome_vacina]["doses"]
    intervalo = VACINAS[nome_vacina]["intervalo"]
    if dose < doses:
        proxima_data = (data_aplicacao + timedelta(days=intervalo))
        return proxima_data.strftime("%d/%m/%Y")
    return None

# Função para mostrar o histórico de vacinação
def mostrar_historico(cpf):
    dados = carregar_dados(cpf)
    if dados is None:
        sg.popup("Nenhuma informação de vacinação encontrada.")
        return
    vacinas = dados["vacinas"]
    texto = ""
    for nome_vacina, doses in vacinas.items():
        texto += f"**{nome_vacina}**\n"
        for dose in doses:
            texto += f" - Dose {dose['dose']}: {dose['data']} (lote: {dose['lote']})\n"
        texto += "\n"
    sg.popup(texto)

# Função para mostrar as próximas doses
def mostrar_proximas_doses(cpf):
    dados = carregar_dados(cpf)
    if dados is None:
        sg.popup("Nenhuma informação de vacinação encontrada.")
        return
    vacinas = dados["vacinas"]
    texto = ""
    for nome_vacina, doses in vacinas.items():
        ultima_dose = doses[-1]
        proxima_dose = calcular_proxima_dose(nome_vacina, ultima_dose["data"], ultima_dose["dose"])
        if proxima_dose is not None:
            texto += f"**{nome_vacina} - Dose {ultima_dose['dose'] + 1}:** {proxima_dose}\n"
    if texto == "":
        sg.popup("Não há próximas doses agendadas.")
    else:
        sg.popup(texto)

# Layout da interface
layout = [
    [sg.Text("Cartão de Vacina Virtual")],
    [sg.Text("CPF:", size=(10, 1)), sg.InputText(key="cpf", size=(15, 1))],
    [sg.Button("Carregar Dados"), sg.Button("Registrar Vacina")],
    [sg.Button("Histórico"), sg.Button("Próximas Doses")],
    [sg.Output(size=(50, 10))]
]

# Janela principal
window = sg.Window("Cartão de Vacina Virtual", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Carregar Dados":
        cpf = values["cpf"]
        dados = carregar_
