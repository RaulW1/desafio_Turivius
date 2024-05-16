import logging

from Scraper import Scraper
from helpers_func import format_output, extract_table_urls, extract_table_content, \
    format_table_contents, format_table_urls
from save_output import save_output


def desafio(target_url, search_keywords, exercicio, headless):
    try:
        scraper = Scraper(target_url, headless)
        scraper.wait(0.5)

        # Buscando barra de pesquisa e inserindo key words
        search_words_element = scraper.find_element_by_name("txtTdPalvs")
        scraper.send_keys(search_words_element, search_keywords)

        # Buscando campo "Exercício" e inserindo valores
        exercicio_element = scraper.find_element_by_name("exercicio")
        scraper.send_keys(exercicio_element, exercicio)

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
            scraper.get(url)
            page_html = scraper.get_current_page_source()
            table_contents.append(extract_table_content(page_html))

        scraper.quit_driver()   # Interação com a página web finalizada, encerrando webdriver

        # Formatando tabela com os conteudos referentes a cada processo/documento
        df_table_contents = format_table_contents(table_contents)

        # Formatando output (merge das tabelas geradas baseado no número do processo)
        df_output = format_output(df_table_contents, df_table_urls)

        # salvando o output (armazenamento em diretório e em base)
        save_output(df_output)
    except Exception as e:
        logging.exception(f"Erro durante a execução: {e}")


if __name__ == "__main__":
    URL = "https://www.tce.sp.gov.br/jurisprudencia/"
    KEY_WORDS = "fraude em escolas"
    EXERCICIO = "2023, 2022"
    HEADLESS = True     # Executa selenium no modo headless

    desafio(URL, KEY_WORDS, EXERCICIO, HEADLESS)
