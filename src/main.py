import json
from bs4 import BeautifulSoup
from art import *
from bs2json import bs2json


def remove_duplicates(og_list: list) -> list:
    res = []
    [res.append(x) for x in og_list if x not in res]
    return res


if __name__ == "__main__":
    path = "../res/"

    with open(path + "opml_test_export.opml", 'r') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, features='html.parser')  # html.parser worked best during development as
        # opposed to lxml

        converter = bs2json()

        tags = soup.findAll('outline')
        json_list = converter.convertAll(tags)
        json_dict = json_list[0]

        json_object = json.dumps(json_dict, indent=4)
        print(json_object)

        with open("../out/sample.json", "w") as outfile:
            json.dump(json_dict, outfile, indent=4)


        child_elements = []

        for child in soup.recursiveChildGenerator():
            if child.name:
                child_elements.append(str(child.name))
                # print(child.name)

        print("child elements: ")
        child_elements_no_dupes = remove_duplicates(child_elements)
        print(str(child_elements_no_dupes))

        for element in child_elements_no_dupes:
            tprint(element)
            print(getattr(soup, element))

        """
        if "outline" in child_elements_no_dupes:
            outline_elements = str(soup.outline)

            outline_soup = BeautifulSoup(outline_elements, "lxml")

            outline_elements_children = []

            repElemList = outline_soup.find_all('outline')
            for repElem in repElemList:
                repElemText = repElem.get('text')
                outline_elements_children.append(repElemText)

            print(outline_elements_children)

            tprint("test")
            test = outline_soup.outline
            
            print(outline_soup.outline)
        """
        """
        outline_children = list(outline_elements.children)
        tprint("outline_children")
        print(outline_children)
        """
