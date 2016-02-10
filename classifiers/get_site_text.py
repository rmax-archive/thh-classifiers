import json
import scrapinghub


max_count = 50000
job_id = "34110/1/8"
SH_API_KEY = ""

conn = scrapinghub.Connection(SH_API_KEY)
project = conn["34110"]
out_path = "/media/sf_temp/items_dmoz_8.json"

job = project.job(job_id)
first_item = True
cnt = 0
with open(out_path, "w") as fout:
    # fout.write("[")
    for item in job.items():
        # if not first_item:
        #     fout.write(",")
        # first_item = False
        fout.write(json.dumps(item)+"\n")
        cnt += 1
        if cnt % 100 ==0:
            print cnt
        if cnt > max_count:
            break
    # fout.write("]")
            