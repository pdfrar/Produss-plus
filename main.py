import PySimpleGUI as sg
global sites
fecharJanela = False
sites = []
exposicaoDeSites = []
try: #Aqui, o programa inicia verificando se já tem sites adicionado no arquivo, em caso verdadeiro, copia esses sites para uma variável de lista
    with open('hosts.txt', 'r') as h: #Em caso falso, define a variável para []
        for linha in h:
            linha = linha.replace('127.0.0.1    ', '').replace('\n', '')
            sites.append(linha)
    for i in range(len(sites)):
        exposicaoDeSites.append([sg.Checkbox(sites[i], key=f'site{i}')])
except FileNotFoundError:
    sites = []

class FrontEnd:
    def __init__(self):
        self.layout = self.LayoutDaJanelaParaInserirOsSites() #Aqui o Layout é armazenado em uma variável

    def LayoutDaJanelaParaInserirOsSites(self):
        layoutinsercaodesites = [
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))],
            [sg.Input(size=(45,20),key='siteinserido')],
            [sg.Button('Apagar selecionados', key='apagarsite')],
            [sg.Column([sg.Text('Sites bloqueados:')], key='colunadesites')],
            [sg.Button('OK', key='-OK-')],
            [sg.Button('Fechar', key ='Fechar')]
        ]
        return sg.Window('Insira seus sites', layoutinsercaodesites, resizable=True)

    def AtualizarJanela(self, window): #Aqui é uma tarefa para atualizar a janela constantemente
        global fecharJanela 
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Fechar': #Caso tente fechar a janela seja no X ou no botão Fechar
            fecharJanela = True
        elif event == '-OK-':
            sites.append(values['siteinserido']) #Adiciona o site para a lista
            for i in range(len(sites)):
              window['colunadesites'].append([sg.Checkbox(sites[i], key=f'site{i}')])
            window['siteinserido'].update('') #Reseta o campo de inserção de sites
            window['colunadesites'.update]

class BackEnd:
    def InputNoArquivoDeTexto(self):
        try:
            with open('hosts.txt', 'w') as h:
                for i in range(len(sites)):
                    h.write(f'127.0.0.1    {sites[i]}\n') #Escreve o site no arquivo hosts.txt
        except FileNotFoundError:
            with open('hosts.txt', 'x') as h:
                for i in range(len(sites)):
                    h.write(f'127.0.0.1    {sites[i]}\n') #Cria o arquivo e escreve o site no arquivo hosts.txt

frontEnd = FrontEnd()
backEnd = BackEnd()

while True:
    if fecharJanela == True:
        break
    else:
        frontEnd.AtualizarJanela(frontEnd.layout)
        backEnd.InputNoArquivoDeTexto()
    #Apertar OK e não ter que fechar a atual para abrir outra janela, e limpar o campo de seleção
    #Printar na janela a lista de sites
    #Depois, tornar a lista útil, de forma que dê para excluir os sites.