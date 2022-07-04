from moviepy.editor import*
import helper
import clip_manager

video = helper.path
clip = VideoFileClip(video)
folder = helper.SaveFolder

def create_clip():
    video = helper.path
    clip = VideoFileClip(video)
    folder = helper.SaveFolder
    for k, v in clip_manager.dictClips.items():
        for n,i in v.items():
            if not n == "name":
                clip1=clip.subclip(i["start"],i["end"])
                final_clip=concatenate_videoclips([clip1])
                final_clip.write_videofile(folder + "/" + str(n) + ".mp4")

def main():
    clip_manager.__init__()
    clip_manager.add_clip("HPbar","adad",55,60)
    clip_manager.add_clip("HPbar","clip",50,66)
    create_clip()

if __name__ == "__main__":
    main()