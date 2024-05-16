# desafio_Turivius
desafio_Turivius

<h1>Objetivo</h1>
Desenvolver um robô de automação de processos utilizando Python e as bibliotecas
requests_html, Selenium e Scrapy. O candidato deverá demonstrar habilidades em
navegação web, extração de dados e manipulação de informações, utilizando essas
ferramentas.

<h1>Requisitos:</h1>
1. Utilizar biblioteca raspagem de dados para fazer o scraping do site e extrair os
dados necessários.<br>
2. Priorizar performance na raspagem dos dados.<br>
3. Extrair e salvar os dados em um banco de dados (Postgresql, MySQL e etc)<br>
4. A modelagem da tabela no banco de dados deve ser otimizada para recuperação
de informação baseada em data, matéria e Doc, ou seja através de index e outras
estruturas de recuperação de informação.<br>
5. O código deve ser pensado de modo a ser colocado em ambiente de produção,
isto é com variaveis de ambiente localizadas em arquivos de separados (por
exemplo, .env).<br>
6. Documentar o código de forma clara e concisa, explicando a lógica por trás das
ações realizadas.<br>

<h1>Descrição do fluxo:</h1>

Entrar no site  https://www.tce.sp.gov.br/jurisprudencia/ e executar uma busca e extrair os documentos referentes 
a cada processo bem como inforações adicionais seguindo o seguinte formato.<br>

<img src="\readme_imgs\formatacao_dados.png" alt="">
![formatacao_dados.png][\readme_imgs\formatacao_dados.png]

Para executar a busca, são preenchidos os campos "Todas as Palavras" e "Exercício" (Tela 1). 

<img src="\readme_imgs\Tela1.png" alt="tela_1">

Após executar a busca o navegador é direcionado para seguinte página (Tela 2):

<img src="\readme_imgs\Tela2.png" alt="tela_2">

esta página exibe os resultados da busca em forma tabular, onde cada linha é refenre a um processo. Os campos "Doc."
e "N° Proc." direcionam respectivamente para o PDF do documento referente ao processo e para uma página contendo
informações adicionais.<br>

Na página de informações adicionais temos os campos "Parte 1", "Parte 2", "Matéria", e "Atuação".

<img src="\readme_imgs\Tela3.png" alt="tela_3">

<h1>Extração dos dados:</h1>

<h2>Tela 1</h2>
É utilizado Selenium para encontrar os elementos referentes aos campos "Todas as Palavras" e "Exercício" e
o botão "Executar", realizar o input dos parâmetros de pesquisa e executar a busca para avançar para a Tela 2.


    # Buscando barra de pesquisa e inserindo key words
    search_words_element = scraper.find_element_by_name("txtTdPalvs")
    scraper.send_keys(search_words_element, search_keywords)
    
    # Buscando campo "Exercício" e inserindo valores
    exercicio_element = scraper.find_element_by_name("exercicio")
    scraper.send_keys(exercicio_element, exercicio)
    
    # Buscando botão "Executa" e executando busca
    execute_search_btn = scraper.find_element_by_name("acao")
    scraper.click(execute_search_btn)

<h1>Tela 2</h2>

É utilizado Selenium para encontrar o elemento referente ao botão para exibir mais resultados da busca. Enquanto o
elemento exitir na tela, existem resultados a serem extraídos. A extração das informações é feita utilizando 
BeautifulSoap para interagir com o código fonte da página e localizar as url para a Tela 3.

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

<h2>Tela 3</h2>

É utilizado BeautifulSoap para interagir com o código fonte da pagina e localizar as tabelas contendo as informações
referentes a cada processo.

        table_contents = []
        # Executando scraping das informações referentes a cada processo/documento
        for url in additional_info_urls:
            # Iterando entre as páginas referentes a cada processo/documento e
            # extraindo suas respectivas informações
            scraper.get(url)
            page_html = scraper.get_current_page_source()
            table_contents.append(extract_table_content(page_html))

<h1>Armazenamento dos Dados</h1>

Os dados são armazenados de maneira em diretório na froma de um arquivo .csv e em uma base de dados Postgresql.
A base contem as tabelas registro, doc e materia, Onde os identificadores unicos de doc e materia são chaves 
estrangeiras na tabela registro que contem a saída da automação. As tabelas podem ser criadas executando os scripts
dentro do diretório .\sql_scripts.<br>

<h1>Separação de Ambientes:</h1>

A separação de ambientes (DEV e PROD) é feita utilizando um arquivo .env (.env.dev e .env.prod) que contém o caminho 
do diretório de armazenamento e as credenciais da base.<br>

<h1>Execução da Automação:</h1>

Para executar a automação basta instalar os requisitos presentes no arquivo requirements.txt.

    pip install -r ./requirements.txt

Configurar os parâmetros de busca dentro do arquivo desafio_turivius.py.

    URL = "https://www.tce.sp.gov.br/jurisprudencia/"
    KEY_WORDS = "fraude em escolas"
    EXERCICIO = "2023, 2022"
    HEADLESS = True     # Executa selenium no modo headless

E especificar o ambiente de execução dentro do arquivo DataBase.py:

    PROD = True
    if not PROD:
    load_dotenv('.env.dev')
    else:
    load_dotenv('.env.prod')





