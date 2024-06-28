import requests
from bs4 import BeautifulSoup

BASE_URL = "https://rustlabs.com"

CRAFTING_TAB_INDEX = None


def scrape_base(suffix):
    global CRAFTING_TAB_INDEX
    r = requests.get(f"{BASE_URL}{suffix}")
    soup = BeautifulSoup(r.text, "html.parser")
    CRAFTING_TAB_INDEX = get_crafting_tab_index(soup)
    return soup


def get_crafting_tab_index(html):
    ol_tabs = html.find("ol", class_="tabs no-select")

    print(ol_tabs.prettify())
    iter = 0
    for ol_tab in ol_tabs:
        if "Craft" in ol_tab.text:
            print(f"FOUND: {iter} ")
            return iter

        iter += 1

    print("TAB STATUS: NOT FOUND")
    return None


def extract_data(html):
    blueprint_list = []
    ingredient_list = []
    resulting_ingredient_amount_list = []
    time_list = []
    wb_lvl_list = []

    # Base table
    base_table = html.findAll("div", class_={"tab-page tab-table"})[
        CRAFTING_TAB_INDEX - 1
    ]

    # Extract the blueprints
    blueprints = base_table.findAll("td", {"class": "left padding"})

    # Extract the ingredients
    ingredients_table = base_table.findAll("td", {"class": "no-padding"})[0]

    ingredients = ingredients_table.findAll("img")
    for ingredient in ingredients:
        if ingredient.get("title") == "":
            continue
        ingredient_list.append(ingredient.get("title"))

    for ingredient in ingredients_table.findAll("span"):
        resulting_ingredient_amount_list.append(ingredient.text)

    # Extract the time
    times = base_table.findAll("td", class_=None)

    # Extract the wb lvl
    wb_lvl = base_table.findAll("td", {"class": "no-padding"})[1]

    for blueprint in blueprints:
        blueprint_list.append(blueprint.text)

    for ingredient in ingredients:
        ingredient_list.append(ingredient.text)

    for time in times:
        time_list.append(time.text)

    for wb_lvl in wb_lvl:
        wb_lvl_list.append(wb_lvl.title)

    print("Blueprints: " + str(blueprint_list))
    print("Ingredients: " + str(ingredient_list))
    print("Resulting ingredients: " + str(resulting_ingredient_amount_list))
    print("Time: " + str(time_list))
    print("Wb lvl: " + str(wb_lvl_list))


extract_data(scrape_base("/item/assault-rifle#tab=craft"))
