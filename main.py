import PySimpleGUI as sg
import os
import ctypes

global sites
global ip
global num_linhas

sites = []
linhasparaapagar = []
sitesparamostrar = []
num_linhas = 0

if not os.path.exists('sitesparabloquear.txt'):
    open('sitesparabloquear.txt', 'w').close()

class FrontEnd:
    def LayoutDaJanelaParaInserirOsSites(self):
        global layoutinsercaodesites
        layoutinsercaodesites = [
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))],
            [sg.Text('(Recomenda-se copiar e colar o link.)', font=("Arial", 9))],
            [sg.Input(size=(45, 20), key='siteinserido')],
            [sg.Button('BLOQUEAR SITE', key='add')],
            [sg.Button('REMOVER ALGUNS SITES', key='removeralguns')],
            [sg.Button('DESATIVAR BLOQUEIO', key='des')]
        ]
        self.janelainsercaodesites = sg.Window('Produc+: Bloqueador de Sites', layoutinsercaodesites, resizable=True)

    def LayoutDaJanelaParaApagarAlgunsSites(self):
        global sitesparamostrar
        linhasparaapagar.clear()
        for i in range(len(sites)):
            linhasparaapagar.append(sites[i])
        sitesparamostrar.clear()
        for element in linhasparaapagar:
            sitesparamostrar.append([sg.Checkbox(f'{element}', key=f'{element}', size=(45, 1))])
        global layoutexclusaodesites
        layoutexclusaodesites = [
            [sg.Text('Selecione os sites que deseja excluir da lista de bloqueio: ', font=("Arial", 11))],
            *sitesparamostrar,
            [sg.Button('OK', key='-OK-')]
        ]
        self.janelaexclusaodesites = sg.Window('Excluir sites', layoutexclusaodesites, resizable=True)

    def AbrirELerJanelaParaInserirOsSites(self):
        self.event, self.values = self.janelainsercaodesites.read()
        return self.event

    def AbrirELerJanelaParaApagarAlgunsSites(self):
        self.event, self.values = self.janelaexclusaodesites.read()
        return self.event, self.values

class BackEnd:
    @staticmethod
    def limparHost():
        linhasparaapagar.clear()
        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'r') as arqhost:
            linhashost = arqhost.readlines()
        for i, linha in enumerate(linhashost):
            if linha[0] != '#':
                linhasparaapagar.append(i)
        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w') as arqhost:
            for i, linha in enumerate(linhashost):
                if i not in linhasparaapagar:
                    arqhost.write(linha)

    @staticmethod
    def contar_linhas(arq):
        global num_linhas
        num_linhas = 0
        with open(f'{arq}', 'r') as arquivo:
            for linha in arquivo:
                num_linhas += 1
        return num_linhas

    @staticmethod
    def sitesiniciais():
        with open('sitesparabloquear.txt', 'r') as arquivo:
            for linha in arquivo:
                sites.append(linha.strip())

    def ControleDeOcorrencias(self, event):
        global sites
        if event == 'add':
            spb = open('sitesparabloquear.txt', 'r')
            siteinserido = front_end.values['siteinserido']
            if f'{siteinserido}\n' not in spb and siteinserido not in spb and siteinserido != '':
                sites.append(siteinserido)
                with open('sitesparabloquear.txt', 'a+') as h:
                    h.write(f'{siteinserido}\n')
                BackEnd.limparHost()
                with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a+') as h:
                    for site in sites:
                        h.write(f'\n127.0.0.1    {site}')
                sg.popup("Site bloqueado com sucesso!")
            elif siteinserido == '':
                sg.popup("Por favor, insira um site para ser bloqueado no campo acima.")
        elif event == 'des':
            if sites:
                BackEnd.limparHost()
                open('sitesparabloquear.txt', 'w').close()
                sg.popup('Bloqueio desativado com sucesso!')
            else:
                sg.popup('Não há bloqueios para desativar.')
        elif event == 'removeralguns':
            listadesitesparaapagar = []
            front_end.LayoutDaJanelaParaApagarAlgunsSites()
            if sites:
                while True:
                    event, values = front_end.AbrirELerJanelaParaApagarAlgunsSites()
                    if event == sg.WINDOW_CLOSED or event == '-OK-':
                        break
                for site in sites:
                    if values.get(site, False):
                        listadesitesparaapagar.append(site)
                with open('sitesparabloquear.txt', 'r') as b:
                    linhas = b.readlines()
                linhas_modificadas = [linha for linha in linhas if linha.strip() not in listadesitesparaapagar]
                with open('sitesparabloquear.txt', 'w') as b:
                    b.writelines(linhas_modificadas)
                BackEnd.limparHost()
                sites.clear()
                BackEnd.sitesiniciais()
                with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a+') as h:
                    for site in sites:
                        h.write(f'\n127.0.0.1    {site}')
                front_end.janelaexclusaodesites.close()
                if listadesitesparaapagar:
                    sg.popup('Sites removidos com sucesso!')
            else:
                sg.popup("Não há sites para remover.")

front_end = FrontEnd()
back_end = BackEnd()
BackEnd.sitesiniciais()
front_end.LayoutDaJanelaParaInserirOsSites()

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    sg.popup("Você deve executar o programa como administrador.")
else:
    while True:
        event = front_end.AbrirELerJanelaParaInserirOsSites()
        if event == sg.WINDOW_CLOSED:
            break
        back_end.ControleDeOcorrencias(event)
