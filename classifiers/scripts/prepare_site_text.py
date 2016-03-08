import json
from html2text import html2text
from mcc.utils import get_text_from_html


if __name__ == "__main__":
    in_path = "/media/sf_temp/func_class_items2.jl"
    out_path = "/media/sf_temp/func_class_items_texts2.json"
    cnt = 0
    use_markdown = True
    processed_urls = set([])

    with open(in_path, "r") as fin:
        with open(out_path, "w") as fout:
            first_item = True
            fout.write("[")
            for text_line in fin:
                try:
                    item = json.loads(text_line)
                    if "html_code" not in item:
                        continue
                    if item["url"] in processed_urls:
                        continue
                    processed_urls.add(item["url"])
                    cats = [x.replace("\r\n\r\n", "").strip() for x in item.get("categories",[])]
                    cats = [x for x in cats if x and len(x)>1]
                    cats = cats[:-1]
                    # print cats
                    out_item = {
                            "categories": cats,
                            "category": item["category"],
                            "category1": item.get("category1", ""),
                            "site_text": get_text_from_html(item["html_code"], use_markdown)
                    }
                    if not first_item:
                        fout.write(",")
                    first_item = False
                    fout.write(json.dumps(out_item, indent=4)+"\n")
                    # break
                    cnt += 1
                    if cnt % 100 == 0:
                        print cnt
                    # if cnt > 5000:
                    #     break
                except Exception as ex:
                    print ex
            fout.write("]")
    print "Completed"

