from linkedin_api import Linkedin
import time

api = Linkedin('youremail@email.com', 'your-password')

def main(max_tentativas=10, intervalo=2):
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            resultado = scrap()
            return resultado  # Retorna o resultado se bem-sucedido
        except Exception as e:
            tentativas += 1
            print(f"Tentativa {tentativas} falhou: {e}")
            if tentativas < max_tentativas:
                time.sleep(intervalo)  # Espera antes de tentar novamente
    print("Todas as tentativas falharam.")
    return None  # Retorna None ou levanta uma exceção, se preferir

def scrap():
    with open('notambush.txt', 'w') as arquivo:
        arquivo.write("") 

    with open('url-list.txt', 'r') as file:
        linhas = file.readlines()

    linhas = [linha.strip() for linha in linhas]

    ids_perfis = []

    for url in linhas:
        id_perfil = extrair_id_linkedin(url)
        if id_perfil:  # Adiciona apenas se o ID não for None
            ids_perfis.append(id_perfil)

    for id_perfil in ids_perfis:
        print(id_perfil)
        profile = api.get_profile(id_perfil)
        experiencias_ambush = [exp for exp in profile.get('experience', []) if exp.get('companyName') == 'Ambush']
        # Se não encontrar a experiência, escreve no arquivo
        if not experiencias_ambush:
            with open('notambush.txt', 'a') as file:
                file.write('https://www.linkedin.com/in/' + id_perfil + "\n")
            print("Nenhuma experiência encontrada com a empresa 'Ambush'. URL escrita em notambush.txt.")

def extrair_id_linkedin(url):
    # Verifica se a URL contém '/in/'
    if '/in/' in url:
        # Divide a URL na parte do '/in/' e pega o que vem depois
        id_perfil = url.split('/in/')[-1]
        # Remove qualquer barra adicional no final da string, se houver
        id_perfil = id_perfil.strip('/')
        return id_perfil
    else:
        return None  # Retorna None se a URL não tiver o padrão '/in/'

main()