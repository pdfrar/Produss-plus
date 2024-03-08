import PySimpleGUI as sg
global sites
sites = []
try:
    with open('hosts.txt', 'r') as h:
        for linha in h:
            linha = linha.replace('127.0.0.1    ', '').replace('\n', '')
            sites.append(linha)
except FileNotFoundError:
    sites = []
print(f'LerArquivoDeSites: {sites}')

class FrontEnd:
    def LayoutDaJanelaParaInserirOsSites(self):
        global layoutinsercaodesites
        layoutinsercaodesites = [
            [sg.Text('Insira aqui o URL do site que deseja bloquear: ', font=("Arial", 11))],
            [sg.Input(size=(45,20),key='siteinserido')],
            [sg.Button('OK',key='-OK-')]
        ]
        janelainsercaodesites = sg.Window('Insira seus sites', layoutinsercaodesites, resizable=True)
        self.event, self.values = janelainsercaodesites.read()
        if self.event == '-OK-':
            janelainsercaodesites.close()
            sites.append(self.values['siteinserido'])
        print('{} {}'.format(self.event,self.values['siteinserido']))

class BackEnd:
    def InputNoArquivoDeTexto(self):
        try:
            with open('hosts.txt', 'w') as h:
                for i in range(len(sites)):
                    h.write(f'127.0.0.1    {sites[i]}\n') #Escreve o site no arquivo hosts.txt
           # with open('hostsformatado.txt', 'w') as h:
          #      for i in range(len(sites)):
           #         h.write('{}\n'.format(sites[i]))
        except FileNotFoundError:
            with open('hosts.txt', 'x') as h:
                for i in range(len(sites)):
                    h.write(f'127.0.0.1    {sites[i]}\n') #Cria o arquivo e escreve o site no arquivo hosts.txt
        print('InputNoArquivoDeTexto: ', sites)
           # with open('hostsformatado.txt', 'x') as h:
           #     for i in range(len(sites)):
           #         h.write('{}\n'.format(sites[i]))

while True:
    FrontEnd().LayoutDaJanelaParaInserirOsSites()
    BackEnd().InputNoArquivoDeTexto()
    #Apertar OK e não ter que fechar a atual para abrir outra janela, e limpar o campo de seleção
    #Printar na janela a lista de sites
    #Depois, tornar a lista útil, de forma que dê para excluir os sites.