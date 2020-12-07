import datetime
from bs4 import *
import requests
from tkinter import *
import ast

file = open('moedas.txt', 'r', encoding='UTF-8')
moedas = file.read().replace('\n',', ')
file.close()
moedas = ast.literal_eval(moedas)
dataAtual = str(datetime.datetime.now())
dataAtual = dataAtual[:dataAtual.index(' ')]
dataAtual = dataAtual[:dataAtual.rindex('-')]+str(int(dataAtual[dataAtual.rindex('-'):])+1)

def conversao():
    global valor
    global moedaOriginal
    global moedaDestino
    valorOriginal = valor1.get()
    moedaOriginal = moedas[moeda1.get()]
    moedaDestino = moedas[moeda2.get()]
    
    try:
        url = f'https://www3.bcb.gov.br/bc_moeda/rest/converter/{valorOriginal}/1/{moedaOriginal}/{moedaDestino}/{dataAtual}'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        valor = soup.find('valor-convertido')

        if valor == None:
            if atualizarCotacao():
                url = f'https://www3.bcb.gov.br/bc_moeda/rest/converter/{valorOriginal}/1/{moedaOriginal}/{moedaDestino}/{dataAtual}'
                req = requests.get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                valor = soup.find('valor-convertido')

        valor = soup.find('valor-convertido').text
        valor2.set(valor)
        cotacao.setvar(dataAtual)

        print(">>> Conversão bem-sucedida")
        return True

    except Exception as E:
        print(">>> Erro na conversão")
        print(">>> "+ str(E))
        return False

def inversao():
    temp = moeda1.get()
    moeda1.set(moeda2.get())
    moeda2.set(temp)

def atualizarCotacao():
    global dataAtual
    global valor
    window.title('Carregando...')

    while valor == None:
            url = f'https://www3.bcb.gov.br/bc_moeda/rest/converter/1/1/{moedaOriginal}/{moedaDestino}/{dataAtual}'
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            valor = soup.find('valor-convertido')
            if valor != None:
                break
            else:
                if int(dataAtual[dataAtual.rindex('-')+1:]) != 1:
                    dataAtual = dataAtual[:dataAtual.rindex('-')]+str(int(dataAtual[dataAtual.rindex('-'):])+1)
                else:
                    dataAtual = dataAtual[:dataAtual.index('-')]+'-'+str(int(dataAtual[dataAtual.index('-')+1:dataAtual.rindex('-')])-1)+'-'+str(30)

    window.title('Conversor de moedas')
    cotacao.config(text='Cotação de:\n'+dataAtual.replace('-','/'))
    return True

if __name__ == "__main__":    
    window = Tk()
    window.title('Conversor de moedas')
    window.resizable(False,False)

    De = Label(window, text= 'De:')
    De.grid(row=0, column=0)

    Para = Label(window, text= 'Para:')
    Para.grid(row=1, column=0)

    valor1 = StringVar()
    valor1.set(1.00)
    v1 = Entry(window, textvariable=valor1)
    v1.grid(row=0, column=1)

    valor2 = StringVar()
    v2 = Entry(window, textvariable=valor2)
    v2.grid(row=1, column=1)

    moeda1 = StringVar(window)
    moeda1.set('Dólar dos Estados Unidos (USD)')
    moeda1dropdown = OptionMenu(window,moeda1, *moedas)
    moeda1dropdown.grid(row=0, column=3)

    moeda2 = StringVar(window)
    moeda2.set('Real Brasileiro (BRL)')
    moeda2dropdown = OptionMenu(window,moeda2, *moedas)
    moeda2dropdown.grid(row=1, column=3)

    cotacaoText = ''
    cotacao = Label(window, text='Cotação de:\n'+cotacaoText)
    cotacao.grid(row=3,column=0)
    cotacao.config(text='Cotação de:\n'+dataAtual.replace('-','/'))
    
    conversao()
    
    botaoConverter = Button(window, text='Converter', command=conversao)
    botaoConverter.grid(row=3,column=1)

    botaoInverter = Button(window, text='Inverter Moedas', command=inversao)
    botaoInverter.grid(row=3,column=3)

    window.mainloop()