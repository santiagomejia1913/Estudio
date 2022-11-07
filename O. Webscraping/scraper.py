import requests
import lxml.html as html #Para poder aplicar x.path
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//div[@class="news V_Title_Img"]/a[1]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

def parse_notice(link, today):
    try: 
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0] # Esto me trae un lista por defecto. Y como title es una lista con un solo elemento  por eso se pone el indice 0. Diferente a como sucede con body.
                title = title.replace('\"', '') # Se genera un error si hay comillas en el titulo. Por lo tanto en caso de que haya comillas, el caracter se remmplaza por ""
                title = title.strip()
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)

            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                #With es un Manejador contextual: Permite que si el archivo llega a cerrarse de manera inesperada porque el script no funciono, mantiene todo de forma segura. Por lo tanto no se corrompe el archivo. Open por su parte esta crando un archivo con el titulo de la noticia en la carpeta que tenga la fecha de hoy (today)
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL) # Para obtener el documento HTML y todo lo que involura http
        if response.status_code == 200:
            home = response.content.decode('utf-8') # response.content me devuelve el documento HTML de la respuesta. decode me permite manejar caracteres especiales
            parsed = html.fromstring(home) #Toma el contenido de HTML que yo ya tengo en variable home y lo transforma en un documento especial en el cual yo puedo hacer xpath. 
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today): 
                # Trae FALSE o TRUE en caso de que haya una carpeta donde tenemos nuestro proyecto con un nombre especifico
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

    
if __name__ == '__main__':
    run()
