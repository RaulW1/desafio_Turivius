import logging

from Scraper import Scraper
from helpers_func import format_output, extract_table_urls, extract_table_content, \
    format_table_contents, format_table_urls
from save_output import save_output


def desafio():
    target_url = "https://www.tce.sp.gov.br/jurisprudencia/"
    search_keywords = ["fraude em escolas"]
    exercicio = ["2023", "2022"]

    try:
        scraper = Scraper(target_url)
        scraper.wait(0.5)

        # Buscando barra de pesquisa e inserindo key words
        search_words_element = scraper.find_element_by_name("txtTdPalvs")
        scraper.send_keys(search_words_element, search_keywords[0])

        # Buscando campo "Exercício" e inserindo valores
        exercicio_element = scraper.find_element_by_name("exercicio")
        scraper.send_keys(exercicio_element, exercicio[0] + ", " + exercicio[1])

        # Buscando botão "Executa" e executando busca
        execute_search_btn = scraper.find_element_by_name("acao")
        scraper.click(execute_search_btn)

        scraper.wait(0.5)

        next_page_btn_xpath = '/html/body/nav/ul/li[3]/a'   # XPATH para botão de próxima página
        next_page = True
        table_urls = []
        # Executando scraping das urls referentes aos processos/documentos
        while next_page:    # Executa scraping enquanto houverem mais páginas com resultados (exibidos de 10 em 10)
            scraper.wait(0.5)

            # Iterando pelas linhas da tabela presentes no resultado da pesquisa e
            # extraindo as urls referentes a cada processo/documento
            page_html = scraper.get_current_page_source()
            table_urls.extend(extract_table_urls(page_html))

            # Buscando botão para avançar para próxima página de resultados
            next_page = scraper.check_element_by_xpath(next_page_btn_xpath)
            if next_page:   # Caso o botão exista (há mais resultados da busca) avança para próxima página
                next_page_btn_element = scraper.find_element_by_xpath(next_page_btn_xpath)
                scraper.click(next_page_btn_element)

        # Formatando tabela com os resultados do scraping das urls
        df_table_urls = format_table_urls(table_urls)

        # Gerando url completa que direciona para as informações de cada processo/documento
        additional_info_urls = df_table_urls['processo'].tolist()
        additional_info_urls = [target_url+url for url in additional_info_urls]

        table_contents = []
        # Executando scraping das informações referentes a cada processo/documento
        for url in additional_info_urls:
            # Iterando entre as páginas referentes a cada processo/documento e
            # extraindo suas respectivas informações
            scraper.webdriver.get(url)
            page_html = scraper.get_current_page_source()
            table_contents.append(extract_table_content(page_html))

        scraper.quit_driver()   # Interação com a página web finalizada, encerrando webdriver

        # Formatando tabela com os conteudos referentes a cada processo/documento
        df_table_contents = format_table_contents(table_contents)

        # Formatando output (merge das tabelas geradas baseado no número do processo)
        df_output = format_output(df_table_contents, df_table_urls)

        save_output(df_output)
    except Exception as e:
        logging.exception(f"Erro durante a execução: {e}")


if __name__ == "__main__":
    desafio()

    """
    Requisitos:
    1. Utilizar biblioteca raspagem de dados para fazer o scraping do site e extrair os
    dados necessários. -> OK
    
    2. Priorizar performance na raspagem dos dados. -> OK
    
    3. Extrair e salvar os dados em um banco de dados (Postgresql, MySQL e etc) - OK
    
    4. A modelagem da tabela no banco de dados deve ser otimizada para recuperação
    de informação baseada em data, matéria e Doc, ou seja através de index e outras
    estruturas de recuperação de informação. - OK
    
    5. O código deve ser pensado de modo a ser colocado em ambiente de produção,
    isto é com variaveis de ambiente localizadas em arquivos de separados (por
    exemplo, .env) - OK
    
    6. Documentar o código de forma clara e concisa, explicando a lógica por trás das
    ações realizadas.
    """

    # TODO adicionar comentarios
    # TODO adicionar salvamento em base
    # TODO adicionar opção de headless scraping
    # TODO containerização
    # TODO documentação
