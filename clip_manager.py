import helper


dictClips = {}
def __init__():
    create_clips_dictionary()

def create_clips_dictionary():
    for k, v in helper.dictBox.items():
        dictClips.update({v["label"]:{"name":{"start":0,"end":0}}})
    print("created clip dictionary")


def add_clip(label,name,start,end):
    for k,v in dictClips.items():
        if k == label:
            lastName = (list(v.keys())[-1])
            lastKey = v[lastName]
            if start >= lastKey["end"]:
                print("adding clip")
                v.update({name:{"start":start,"end":end}})
            elif start < lastKey["end"]:
                print("adding clip")
                v.update({lastName:{"start":lastKey["start"],"end":end}})
    




def main():
    __init__()
    add_clip("HPbar","adad",55,60)
    add_clip("HPbar","clip",50,66)
    print(dictClips)


if __name__ == "__main__":
    main()