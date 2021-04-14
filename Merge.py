from PIL import Image

def get_concat_h_cut(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, min(im1.height, im2.height)))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v_cut(im1, im2):
    dst = Image.new('RGB', (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def callThis():
    im1 = Image.open('q0.png')
    im2 = Image.open('q1.png')
    im3 = Image.open('q2.png')
    im4 = Image.open('q3.png')
    get_concat_h_cut(im1, im2).save('Top Half.png')
    print('Saving top half')
    get_concat_h_cut(im3, im4).save('Lower Half.png')
    print('Saving lower half')


    im1 = Image.open('Top Half.png')
    im2 = Image.open('Lower Half.png')
    print('Saving Final Image')
    get_concat_v_cut(im1, im2).save('Final Segmented.png')
