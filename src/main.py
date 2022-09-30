import re
from urllib.parse import urljoin
import logging

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from outputs import control_output
from constants import (
    MAIN_DOC_URL,
    BASE_DIR,
    PEP,
    EXPECTED_STATUS,
    whats_new_url,
    downloads_url
)
from configs import (
    configure_argument_parser,
    configure_logging
)
from utils import get_response, find_tag


def whats_new(session):
    """Парсим страницу с новостями."""
    response = get_response(session, whats_new_url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1').text
        dl = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((version_link, h1, dl))
    return results


def latest_versions(session):
    """Собираем информацию о версиях Python."""

    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    sidebar = soup.find("div", class_="sphinxsidebarwrapper")
    find_ul = sidebar.find_all("ul")
    for ul in find_ul:
        if "All versions" in ul.text:
            # Если текст найден, ищутся все теги <a> в этом списке.
            a_tags = ul.find_all("a")
            # Остановка перебора списков.
            break
    else:
        raise Exception("Ничего не нашлось")
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    results = [("Ссылка на документацию", "Версия", "Статус")]
    for ver in a_tags:
        text_match = re.search(pattern, ver.text)
        if text_match is not None:
            results.append(
                (
                    ver["href"],
                    text_match.groups()[0],
                    text_match.groups()[1]
                )
            )
        else:
            results.append((ver["href"], ver.text, ""))
    return results


def download(session):
    """Загружаем со страницы загрузок."""

    response = session.get(downloads_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, features="lxml")
    main = find_tag(soup, "div", {"role": "main"})
    responsive_table = find_tag(main, "table", {"class": "docutils"})
    pdf_a4_tag = responsive_table.find(
        "a", {"href": re.compile(r".+pdf-a4\.zip$")}
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag["href"])
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    filename = archive_url.split("/")[-1]
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    """Собираем статусы со страницы PEP
    и сравниваем их со статусами каждого
    в карточке."""

    response = get_response(session, PEP)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    section = find_tag(soup, "section", attrs={"id": "numerical-index"})
    table = section.find("tbody")
    tr = table.find_all("tr")
    storage = {}
    for item in tr:
        link = item.find("a")["href"]
        td = item.find("td").text
        status = td[1] if len(td) > 1 else ""
        pep_link = urljoin(PEP, link)
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup_pep = BeautifulSoup(response.text, features="lxml")
        status_tag = soup_pep.find("dl", class_="rfc2822 field-list simple")
        ex_status = status_tag.find(string="Status").findNext("dd").text
        if ex_status in EXPECTED_STATUS[status]:
            storage[ex_status] = storage.get(ex_status, 0) + 1
        else:
            logging.info(
                f"Статус в карточке: {ex_status}\n"
                f"Ожидаемые статусы: {EXPECTED_STATUS[status]}\n"
                f"{pep_link}\n"
            )
    return [("Статус", "Количество")] + list(storage.items())


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        # передаём их в функцию вывода вместе с аргументами командной строки.
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
