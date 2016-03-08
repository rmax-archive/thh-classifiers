# -*- coding: utf-8 -*-
import json
import scrapinghub


# max_count = 500000
max_count = 0
# job_ids = ["34110/1/15"]
job_ids = ["34110/2/5", "34110/3/7", "34110/5/3",
           "34110/6/3", "34110/7/5", "34110/8/3",
           "34110/9/2", "34110/10/2", "34110/11/2",
           "34110/12/3","34110/13/1",
           ]
job_files = ["/media/sf_temp/ggl_wiki.json",
    "/media/sf_temp/ggl_blogs.json",
    "/media/sf_temp/ggl_search.json",
    "/media/sf_temp/ggl_news.json",
]
SH_API_KEY = ""

conn = scrapinghub.Connection(SH_API_KEY)
project = conn["34110"]
out_path = "/media/sf_temp/func_class_items2.jl"


first_item = True
cnt = 0
with open(out_path, "w") as fout:
    for job_id in job_ids:
        # fout.write("[")
        print job_id
        job = project.job(job_id)
        for item in job.items():
            # if not first_item:
            #     fout.write(",")
            # first_item = False
            fout.write(json.dumps(item)+"\n")
            cnt += 1
            if cnt % 100 ==0:
                print cnt
            if cnt > max_count and max_count:
                break
        # fout.write("]")
    for file in job_files:
        with open(file, "r") as fin:
            items = json.loads(fin.read())
            for item in items:
                fout.write(json.dumps(item)+"\n")
                cnt += 1
                if cnt % 100 ==0:
                    print cnt
                if cnt > max_count and max_count:
                    break

