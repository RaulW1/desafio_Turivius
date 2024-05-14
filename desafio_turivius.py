from Scraper import Scraper

from helpers_func import format_table


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

    # table_rows = scraper.find_elements_by_class_name("borda-superior")
    current_url = scraper.get_current_url()
    df_table = scraper.extract_table_contents(current_url)

    df_table = format_table(df_table)

    scraper.quit_driver()


if __name__ == "__main__":
    desafio()
    # TODO verificar complitude dos dados
    # TODO scrapar url dos documentos
    # TODO adicionar salvamnto em arquivo
    # TODO adicionar salvamento em base
