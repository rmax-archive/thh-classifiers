import json
from html2text import html2text


in_path = "/media/sf_temp/items_dmoz_8.json"
out_path = "/media/sf_temp/items_dmoz_8_clf_l.json"
# out_path = "./items_dmoz_6_clf_sample.json"
result = []
cnt = 0

with open(in_path, "r") as fin:
    with open(out_path, "w") as fout:
        first_item = True
        fout.write("[")
        for text_line in fin:
            try:
                item = json.loads(text_line)
                cats = [x.replace("\r\n\r\n", "").strip() for x in item["categories"]]
                cats = [x for x in cats if x and len(x)>1]
                cats = cats[:-1]
                # print cats
                out_item = {
                        "categories": cats,
                        "category": item["category"],
                        "category1": item["category1"],
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
            except Exception, ex:
                print ex
        fout.write("]")
print "Completed"

