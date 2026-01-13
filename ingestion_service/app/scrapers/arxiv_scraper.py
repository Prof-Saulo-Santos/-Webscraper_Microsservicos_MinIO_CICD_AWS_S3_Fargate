import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from app.domain.article import Article, Author
from app.core.logger import logger


class ArxivScraper:
    async def fetch_articles(
        self, query: str, max_results: int, start: int = 0
    ) -> List[Article]:
        url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size={max_results}&start={start}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) IngestionService/1.0"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Falha ao buscar página: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("li.arxiv-result")[:max_results]

        if not results:
            logger.warning(
                "Nenhum resultado encontrado. Verifique a query ou mudanças no layout do arXiv."
            )
            return []

        articles = []
        processed_count = 0
        for result in results:
            try:
                # Título
                title_elem = result.select_one("p.title")
                title = title_elem.get_text(strip=True) if title_elem else "Sem título"

                # ID do arXiv (Prioridade: PDF -> Abs -> Unknown)
                arxiv_id = None

                # Tenta pegar do Link PDF
                pdf_link_elem = result.select_one("p.list-pdf a[href*='/pdf/']")
                if pdf_link_elem:
                    href = pdf_link_elem["href"]
                    pdf_link = (
                        href if href.startswith("http") else f"https://arxiv.org{href}"
                    )
                    arxiv_id = pdf_link.split("/")[-1].replace(".pdf", "")
                else:
                    pdf_link = None

                # Tenta pegar do Link Abstract se falhou no PDF
                page_link_elem = result.select_one("a[href*='/abs/']")
                if page_link_elem:
                    href = page_link_elem["href"]
                    link = (
                        href if href.startswith("http") else f"https://arxiv.org{href}"
                    )
                    if not arxiv_id:
                        arxiv_id = link.split("/")[-1]
                else:
                    link = ""

                # Fallback final (garante unicidade global)
                if not arxiv_id:
                    unique_index = start + processed_count
                    arxiv_id = f"unknown_{unique_index}"

                # Autores
                authors_elems = result.select("p.authors a")
                authors = [Author(name=a.get_text(strip=True)) for a in authors_elems]

                # Abstract
                abstract_elem = result.select_one("span.abstract-full")
                summary = (
                    abstract_elem.get_text(separator=" ", strip=True)
                    if abstract_elem
                    else ""
                )

                # Datas (submitted / updated)
                date_span = result.find("span", string=lambda t: t and "Submitted" in t)
                if date_span:
                    try:
                        date_text = date_span.get_text(strip=True)
                        parts = date_text.split(";")
                        published_str = parts[0].replace("Submitted ", "").strip()
                        published = datetime.strptime(published_str, "%d %B %Y")

                        if len(parts) > 1:
                            updated_str = parts[1].replace("updated ", "").strip()
                            updated = datetime.strptime(updated_str, "%d %B %Y")
                        else:
                            updated = published
                    except (ValueError, IndexError) as e:
                        logger.warning(
                            f"Erro no parse de data '{date_text}' ({e}). Usando data atual."
                        )
                        published = updated = datetime.now()
                else:
                    published = updated = datetime.now()

                # Categorias
                categories = [
                    tag.get_text(strip=True)
                    for tag in result.select("span.primary-subject, span.subjects")
                ]

                article = Article(
                    id=arxiv_id,
                    title=title,
                    authors=authors,
                    summary=summary,
                    published=published,
                    updated=updated,
                    categories=categories or [query],
                    link=link,
                    pdf_link=pdf_link,
                )
                articles.append(article)
                processed_count += 1

            except Exception as e:
                logger.error(f"Erro ao processar um artigo: {e}")
                continue

        return articles
