from parsel import Selector
import requests
import rich.traceback
from bs4 import BeautifulSoup


rich.traceback.install()

BASE_URL = "https://rustlabs.com"


def scrape(url):
    r = requests.get(url + "/group=itemlist")
    sel = Selector(text=r.text)
    # get the div with the class info-block
    info_block = sel.css("div.info-block")
    iter = 0
    info_list = []
    for link in info_block.css("a"):
        iter += 1
        if iter == 2:
            break
        curr_page_info = scrape_item_page(link.attrib["href"])
        info_list.append(curr_page_info)

    return info_list


def scrape_item_craft_table(url):
    print("Scraping: " + url)
    r = requests.get(url)
    sel = Selector(text=r.text)

    # Desired table
    table = sel.css("table").extract()[2]

    item_list = assemble_item_list(table)

    return item_list


# TODO: Fix shit
def assemble_item_list(scraped_table_html):
    print("Scraped: " + scraped_table_html)
    ingredient_title_list = []
    ingredient_amount_list = []
    ingredient_efficiency_list = []

    table = Selector(text=scraped_table_html)

    # Get the ingredients title
    for td in table.css("tbody"):
        for text in td.css("td"):
            for item_name in text.css("td.left"):
                selector = Selector(text=item_name.extract())
                text = selector.xpath("//a/text()").get()
                ingredient_title_list.append(text)

    for td in table.css("tbody"):
        for text in td.css("td"):
            for item_name in text.css("td.no-padding"):
                selector = Selector(text=item_name.extract())
                text = selector.xpath("//span/text()").get()
                ingredient_amount_list.append(text)

    for td in table.css("tbody"):
        for text in td.css("td"):
            for item_name in text.css("td"):
                selector = Selector(text=item_name.extract())
                text = selector.xpath("//td/text()").get()
                if text is not None:
                    ingredient_efficiency_list.append(text)

    # print("TABLE CONTENT: ", table.get())
    # print("INGREDIENTS TITLE LIIIIIIIIIIIIIIIIIIIIIIIISTT: ", ingredient_title_list)
    # print("INGREDIENTS AMOUNT LIIIIIIIIIIIIIIIIIIIIIIIISTT: ", ingredient_amount_list)
    # print(
    #     "INGREDIENTS EFFICIENCY LIIIIIIIIIIIIIIIIIIIIIIIISTT: ",
    #     ingredient_efficiency_list,
    # )

    # TODO: Mount the fucking object
    for item in ingredient_title_list:
        final_object = {
            "title": item,
            "amount": ingredient_amount_list[ingredient_title_list.index(item)],
            "efficiency": ingredient_efficiency_list[ingredient_title_list.index(item)],
        }

        print("FINAL OBJECT: ", final_object)
    return ingredient_title_list


def scrape_item_recycle_table(url):
    print("Scraping: " + url)
    r = requests.get(url)
    sel = Selector(text=r.text)

    table = sel.css("table").extract()[3]

    item_list = assemble_item_list(table)

    return item_list


def scrape_single_item(item_url):
    r = requests.get(item_url)
    sel = Selector(text=r.text)

    # get the ol with the classes tabs and no-select
    ol = sel.css("ol.tabs.no-select")

    # all the tabs
    tab_list = []
    for li in ol.css("li"):
        tab_list.append(li.attrib["data-name"])

    for item in tab_list:
        print("Item: " + item)
        if item == "craft":
            scrape_item_craft_table(item_url + "#tab=craft")

        if item == "recycle":
            scrape_item_recycle_table(item_url + "#tab=recycle")

    return r.text


def scrape_item_page(suffix: str):
    item_info = "Item info: " + scrape_single_item(BASE_URL + suffix)

    return item_info


def main():
    scrape(BASE_URL)


if __name__ == "__main__":
    main()
