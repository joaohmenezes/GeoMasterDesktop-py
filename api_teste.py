import requests

def carregar_dados_paises():
    print("Baixando dados dos países...")
    url = "https://restcountries.com/v3.1/all?fields=name,flags,translations"
    
    resposta = requests.get(url)
    dados_brutos = resposta.json()
    
    lista_paises = []
    
    
    for pais in dados_brutos:
        nome = pais.get('translations', {}).get('por', {}).get('common', 'Desconhecido')
        bandeira_url = pais.get('flags', {}).get('png', '')
        
        if nome != 'Desconhecido' and bandeira_url:
            lista_paises.append({
                "nome": nome,
                "bandeira": bandeira_url
            })
            
    return lista_paises

paises = carregar_dados_paises()
print(f"\nSucesso! Baixamos dados de {len(paises)} países.")
print(f"Exemplo 1: {paises[0]}")
print(f"Exemplo 2: {paises[15]}")