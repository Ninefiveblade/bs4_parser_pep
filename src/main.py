import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (DOWNLOADS_URL, EXPECTED_STATUS, MAIN_DOC_URL, PEP,
                       WHATS_NEW_URL, BASE_DIR)
from exceptions import InfoNotFound
from outputs import control_output
from utils import find_tag, get_soup_response
from exceptions import EmtyResults, ArgumentParserError


LOGGER_INFORMATION = (
    "Статус в карточке: {} "
    "Ожидаемые статусы: {} "
    "{}"
)


def whats_new(session):
    """Парсим страницу с новостями."""

    soup = get_soup_response(session, WHATS_NEW_URL)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(find_tag(
        main_div, 'div', attrs={'class': 'toctree-wrapper'}
    ).find_all('li', attrs={'class': 'toctree-l1'}), "sections_by_python"):
        version_link = urljoin(WHATS_NEW_URL, find_tag(section, 'a')['href'])
        soup = get_soup_response(session, version_link)
        h1 = find_tag(soup, 'h1').text
        dl = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((version_link, h1, dl))
    return results


def latest_versions(session):
    """Собираем информацию о версиях Python."""

    soup = get_soup_response(session, MAIN_DOC_URL)
    for ul in tqdm(soup.find(
        "div", class_="sphinxsidebarwrapper"
    ).find_all("ul"), "latest_versions"):
        if "All versions" in ul.text:
            # Если текст найден, ищутся все теги <a> в этом списке.
            a_tags = ul.find_all("a")
            # Остановка перебора списков.
            break
    else:
        raise InfoNotFound("Ничего не нашлось")
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

    soup = get_soup_response(session, DOWNLOADS_URL)
    pdf_a4_tag = find_tag(
        find_tag(soup, "div", {"role": "main"}), "table", {"class": "docutils"}
    ).find(
        "a", {"href": re.compile(r".+pdf-a4\.zip$")}
    )
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_tag["href"])
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    """Собираем статусы со страницы PEP
    и сравниваем их со статусами каждого
    в карточке."""

    soup = get_soup_response(session, PEP)
    all_peps = find_tag(
        soup, "section", attrs={"id": "numerical-index"}
    ).find("tbody").find_all("tr")
    storage = defaultdict(int)
    logging_storage = []
    for item in tqdm(all_peps, "pep"):
        link = item.find("a")["href"]
        td = item.find("td").text
        status = td[1] if len(td) > 1 else ""
        pep_link = urljoin(PEP, link)
        soup = get_soup_response(session, pep_link)
        status_tag = soup.find(
            "dl", class_="rfc2822 field-list simple"
        ).find(string="Status").findNext("dd").text
        if status_tag in EXPECTED_STATUS[status]:
            storage[status_tag] += 1
        else:
            storage["undifined_status"] += 1
            logging_storage.append(
                LOGGER_INFORMATION.format(
                    status_tag, EXPECTED_STATUS[status], pep_link
                )
            )
    logging.info(*logging_storage)
    return (
        ("Статус", "Количество"),
        *storage.items(),
        ("Total", sum(storage.values)),
    )


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
    try:
        args = arg_parser.parse_args()
    except ArgumentParserError:
        logging.exception("Неверно переданы аргументы.")
        raise
    logging.info(f"Аргументы командной строки: {args}")
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        else:
            raise TypeError
    except UnboundLocalError as error:
        raise EmtyResults(
            "Получены неверные результаты в results",
            error
        )
    except TypeError as error:
        raise EmtyResults(
            "Получен непредвиденный тип данных: в results",
            error
        )
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
