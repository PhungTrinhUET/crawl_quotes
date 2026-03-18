import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main(argv):
    # Accept multiple keywords from command line or use defaults
    if len(argv) > 1:
        keywords = argv[1:]
    else:
        # Default keywords for comprehensive coffee search
        keywords = ['cà phê', 'robusta', 'arabica']

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # Pass keywords via spider argument
    process.crawl('news_search', keywords=keywords)
    process.start()


if __name__ == '__main__':
    main(sys.argv)
