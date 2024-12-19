import time
from crawler import Crawler

def main(max_tries=1, intervalo=0):
    tries = 0
    crawler = Crawler()
    while tries < max_tries:
        try:
            resultado = crawler.run()
            return resultado
        except Exception as e:
            tries += 1
            print(f"Tentativa {tries} falhou: {e}")
            if tries < max_tries:
                time.sleep(intervalo)

main()