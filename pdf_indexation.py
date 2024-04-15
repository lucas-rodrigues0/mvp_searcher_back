import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT
from sqlalchemy.exc import IntegrityError
from PyPDF2 import PdfReader

from model import Session, PdfPages


def index_pdf_by_pages():
    """Script para extração das páginas do PDF da constituição federal, e a indexação do conteúdo de cada página.
    Cria um diretório para esse index, ou utiliza um já existente. Insere o conteúdo de cada página no db.
    """
    print("Initialize indexation...")
    # Caminhos para o diretório de índice e para o arquivo PDF
    index_dir = "full_text_searcher/index_directory"
    pdf_file_path = "full_text_searcher/resources/CF.pdf"

    # Schema do índice
    schema = Schema(path=ID(stored=True), content=TEXT(stored=True))

    # Criação do diretório de índice ou abertura se já existir
    print("Create/update index directory...")
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        ix = create_in(index_dir, schema)
    else:
        ix = open_dir(index_dir)

    # Abre conexão com a base de dados para inserir o conteudo das paginas
    session = Session()

    # Criação ou obtenção do escritor do índice
    writer = ix.writer()

    # Extrair texto do PDF
    print("Extracting PDF pages...")
    with open(pdf_file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            page_num = reader.get_page_number(page) + 1
            page_content = page.extract_text()
            pdf_page = PdfPages(
                page_num=int(page_num),
                page_content=page_content,
            )
            session.add(pdf_page)
            writer.add_document(path=str(page_num), content=page_content)
            print("Page ", page_num, ": Ok")

    # Finalizar e otimizar o índice e a inserção na base
    writer.commit(optimize=True)
    print("Index committed")
    try:
        session.commit()
        print("Finished")
    except IntegrityError as e:
        print("Pages already inserted into database")
        session.close()
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    index_pdf_by_pages()
