from Scraper import Scraper

from helpers_func import format_output, extract_table_urls, extract_table_content, format_table_contents


def desafio():
    target_url = "https://www.tce.sp.gov.br/jurisprudencia/"
    search_keywords = ["fraude em escolas"]
    exercicio = ["2023", "2022"]

    scraper = Scraper(target_url)

    scraper.wait(0.5)

    search_words_element = scraper.find_element_by_name("txtTdPalvs")
    scraper.send_keys(search_words_element, search_keywords[0])

    exercicio_element = scraper.find_element_by_name("exercicio")
    scraper.send_keys(exercicio_element, exercicio[0] + ", " + exercicio[1])

    execute_search_btn = scraper.find_element_by_name("acao")
    scraper.click(execute_search_btn)

    scraper.wait(0.5)

    current_url = scraper.get_current_url()
    df_table_urls = extract_table_urls(current_url)

    additional_info_urls = df_table_urls['processo'].tolist()
    additional_info_urls = [target_url+url for url in additional_info_urls]

    table_contents = []
    for url in additional_info_urls:
        scraper.webdriver.get(url)
        # scraper.wait(0.5)

        table_contents.append(extract_table_content(url))

    scraper.quit_driver()

    df_table_contents = format_table_contents(table_contents)

    df_output = format_output(df_table_contents, df_table_urls)


if __name__ == "__main__":
    desafio()
    # TODO verificar complitude dos dados
    # TODO scrapar url dos documentos
    # TODO adicionar salvamnto em arquivo
    # TODO adicionar salvamento em base
    # TODO adicionar opção de headless scraping
