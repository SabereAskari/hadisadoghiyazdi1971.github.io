import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re, os

class PartlasticSpider(CrawlSpider):
    name = "partlastic"
    allowed_domains = ["partlasticgroup.com"]
    start_urls = ["https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d8%a8%d8%b3%d9%be%d8%a7%d8%b1-%d8%b3%d8%a7%d8%b2%d9%87-%d8%aa%d9%88%d8%b3/",
                  "https://partlasticgroup.com/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d9%85%d8%b4%d9%87%d8%af-%da%af%db%8c%d8%b1%d8%a8%da%a9%d8%b3/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d8%b3%db%8c%da%a9%d9%84%d9%85%d9%87/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d8%b9%d8%a7%db%8c%d9%82-%d8%ae%d9%88%d8%af%d8%b1%d9%88-%d8%aa%d9%88%d8%b3/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d9%be%d8%a7%d8%b1%d8%b3%d8%a7-%db%8c%d8%a7%d8%b1%d8%a7%d9%86/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d9%be%d9%88%db%8c%d8%a7%da%af%d8%b3%d8%aa%d8%b1-%d8%ae%d8%b1%d8%a7%d8%b3%d8%a7%d9%86/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d9%be%d8%a7%d8%b1%d8%aa-%d9%84%d8%a7%d8%b3%d8%aa%db%8c%da%a9/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d8%a8%d8%b3%d9%be%d8%a7%d8%b1-%d8%b3%d8%a7%d8%b2%d9%87-%d8%aa%d9%88%d8%b3/",
                  "https://partlasticgroup.com/product-category/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa-%d8%b1%db%8c%d9%86%da%af-%d8%b3%d8%a7%d8%b2%db%8c-%d9%85%d8%b4%d9%87%d8%af/"]

    rules = (
        Rule(LinkExtractor(allow=()), callback="parse_page", follow=True),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def clean_text(self, html):
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[\r\n\t]+", " ", text)
        return text.strip()

    def parse_page(self, response):
        text = self.clean_text(response.text)
        if len(text) > 300 and re.search(r"[\u0600-\u06FF]", text):  # فقط صفحات فارسی و دارای متن
            os.makedirs("documents", exist_ok=True)
            filename = re.sub(r"[^a-zA-Z0-9]+", "_", response.url)[:80] + ".txt"
            path = os.path.join("documents", filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self.log(f"✅ Saved clean text: {path}")
