import json


if __name__ == "__main__":
    in_path = "/media/sf_temp/func_class_items2.jl"
    out_path = "./full_urls.json"
    cnt = 0
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
                    out_item = {}
                    out_item["pagetype"] = item["category"]
                    out_item["url"] = item["url"]
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

