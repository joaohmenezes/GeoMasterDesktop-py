import random
import os
from io import BytesIO
import customtkinter as ctk
import requests
from PIL import Image

#Conf do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


lista_paises = []
pais_correto = {}
pontos = 0
cor_padrao_botao = None


#func para buscar os dados na api
def carregar_dados_paises():
    global lista_paises
    try:
        url = "https://restcountries.com/v3.1/all?fields=name,flags,translations,capital,independent,cca2"
        resposta = requests.get(url)
        dados_brutos = resposta.json()

        for pais in dados_brutos:
            independente = pais.get("independent", False)
            sigla = pais.get("cca2", "").lower()
            
            nome = pais.get("translations", {}).get("por", {}).get("common", "Desconhecido")
            bandeira_url = pais.get("flags", {}).get("png", "")
            
            capital_lista = pais.get("capital", [])
            capital = capital_lista[0] if capital_lista else "Desconhecida"

            # filtro para apenas paises independentes
            if independente and nome != "Desconhecido" and bandeira_url:
                lista_paises.append({
                    "nome": nome, 
                    "bandeira": bandeira_url,
                    "capital": capital,
                    "sigla": sigla
                })
    except Exception as e:
        print(f"Erro ao baixar dados: {e}")


# verifiica e pinta os botoes
def verificar_resposta(resposta_escolhida, botao_clicado):
    global pontos
    botoes = [btn1, btn2, btn3, btn4]
    
    for btn in botoes:
        btn.configure(state="disabled")

    if resposta_escolhida == pais_correto["nome"]:
        pontos += 1
        botao_clicado.configure(fg_color="#2FA572")
    else:
        pontos = 0 
        botao_clicado.configure(fg_color="#D13A42")
        for btn in botoes:
            if btn.cget("text") == pais_correto["nome"]:
                btn.configure(fg_color="#2FA572")
        
    texto_pontos.configure(text=f"Pontuação: {pontos}")
    janela.after(1500, preparar_proxima_rodada)


def preparar_proxima_rodada():
    botoes = [btn1, btn2, btn3, btn4]
    for btn in botoes:
        btn.configure(fg_color=cor_padrao_botao, state="normal")
    nova_rodada()


# function de nova rodada com mapas e bandeiras
def nova_rodada():
    global lista_paises, pais_correto

    if not lista_paises:
        return

    #sorteia os paises
    pais_correto = random.choice(lista_paises)
    opcoes_erradas = []
    
    while len(opcoes_erradas) < 3:
        sorteado = random.choice(lista_paises)
        if sorteado["nome"] != pais_correto["nome"] and sorteado not in opcoes_erradas:
            opcoes_erradas.append(sorteado)

    todas_opcoes = [pais_correto] + opcoes_erradas
    random.shuffle(todas_opcoes)

    texto_capital.configure(text=f"Capital: {pais_correto['capital']}")

    #mapa ou bandeira
    tipo_rodada = random.choice(["bandeira", "mapa"])
    
    #procura a imagem tamanho 256
    caminho_mapa = f"mapas/{pais_correto['sigla']}/256.png"

    try:
        #se sorteou mapa e a imagem existe
        if tipo_rodada == "mapa" and os.path.exists(caminho_mapa):
            img_pillow = Image.open(caminho_mapa)
            titulo.configure(text="De que país é este mapa?")
            
        #se sorteou bandeira ou se o mapa falhar
        else:
            resposta_img = requests.get(pais_correto["bandeira"])
            img_dados = BytesIO(resposta_img.content)
            img_pillow = Image.open(img_dados)
            titulo.configure(text="De que país é esta bandeira?")

        #renderiza a imagem 
        imagem_ctk = ctk.CTkImage(light_image=img_pillow, dark_image=img_pillow, size=(300, 200))
        espaco_imagem.configure(image=imagem_ctk, text="")
        espaco_imagem.image = imagem_ctk
        
    except Exception as e:
        espaco_imagem.configure(text="Erro ao carregar imagem")

    #atualiza os botões
    btn1.configure(text=todas_opcoes[0]["nome"], command=lambda txt=todas_opcoes[0]["nome"], b=btn1: verificar_resposta(txt, b))
    btn2.configure(text=todas_opcoes[1]["nome"], command=lambda txt=todas_opcoes[1]["nome"], b=btn2: verificar_resposta(txt, b))
    btn3.configure(text=todas_opcoes[2]["nome"], command=lambda txt=todas_opcoes[2]["nome"], b=btn3: verificar_resposta(txt, b))
    btn4.configure(text=todas_opcoes[3]["nome"], command=lambda txt=todas_opcoes[3]["nome"], b=btn4: verificar_resposta(txt, b))


#criacao da janela principal e UI
janela = ctk.CTk()
janela.geometry("600x750")
janela.title("Adivinhe o País!")

titulo = ctk.CTkLabel(janela, text="Carregando...", font=("Arial", 28, "bold"))
titulo.pack(pady=(20, 5))

texto_capital = ctk.CTkLabel(janela, text="Capital: Carregando...", font=("Arial", 18, "italic"), text_color="gray70")
texto_capital.pack(pady=(0, 10))

texto_pontos = ctk.CTkLabel(janela, text="Pontuação: 0", font=("Arial", 18))
texto_pontos.pack(pady=(0, 10))

espaco_imagem = ctk.CTkLabel(janela, text="Carregando jogo...", width=300, height=200, fg_color="gray20", corner_radius=10, font=("Arial", 14))
espaco_imagem.pack(pady=10)

frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_botoes.pack(pady=20)

btn1 = ctk.CTkButton(frame_botoes, text="...", width=200, height=50, font=("Arial", 16))
btn1.grid(row=0, column=0, padx=10, pady=10)

btn2 = ctk.CTkButton(frame_botoes, text="...", width=200, height=50, font=("Arial", 16))
btn2.grid(row=0, column=1, padx=10, pady=10)

btn3 = ctk.CTkButton(frame_botoes, text="...", width=200, height=50, font=("Arial", 16))
btn3.grid(row=1, column=0, padx=10, pady=10)

btn4 = ctk.CTkButton(frame_botoes, text="...", width=200, height=50, font=("Arial", 16))
btn4.grid(row=1, column=1, padx=10, pady=10)

cor_padrao_botao = btn1.cget("fg_color")

carregar_dados_paises()
nova_rodada()

janela.mainloop()