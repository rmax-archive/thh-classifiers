# -*- coding: utf-8 -*-


def filter_rare_classes(data, class_field, min_class_size,
                        mode="remove", replace_class=None):
    class_cnt = data[class_field].value_counts()
    if mode == "remove":
        class_take = class_cnt.index[class_cnt >= min_class_size]
        data = data[data[class_field].isin(class_take)]
    elif mode == "rename":
        class_rename = class_cnt.index[class_cnt < min_class_size]
        data[class_field][class_rename] = replace_class
    return data