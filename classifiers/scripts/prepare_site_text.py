import json
from html2text import html2text


in_path = "/media/sf_temp/func_class_items.jl"
out_path = "/media/sf_temp/func_class_items_texts.json"
cnt = 0

with open(in_path, "r") as fin:
    with open(out_path, "w") as fout:
        first_item = True
        fout.write("[")
        for text_line in fin:
            try:
                item = json.loads(text_line)
                if "html_code" not in item:
                    continue
                cats = [x.replace("\r\n\r\n", "").strip() for x in item.get("categories",[])]
                cats = [x for x in cats if x and len(x)>1]
                cats = cats[:-1]
                # print cats
                out_item = {
                        "categories": cats,
                        "category": item["category"],
                        "category1": item.get("category1", ""),
                        "site_text": html2text(item["html_code"])
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
