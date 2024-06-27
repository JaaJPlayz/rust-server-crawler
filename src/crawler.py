from parsel import Selector
import requests
import rich.traceback


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
        if iter == 5:
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
    print(table)

    print("Scraped: " + table)


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
        if item == "craft":
            scrape_item_craft_table(item_url + "#tab=craft")

        if item == "recycle":
            scrape_item_craft_table(item_url + "#tab=recycle")

    return r.text


def scrape_item_page(suffix: str):
    item_info = "Item info: " + scrape_single_item(BASE_URL + suffix)

    return item_info


def main():
    scrape(BASE_URL)


if __name__ == "__main__":
    main()
