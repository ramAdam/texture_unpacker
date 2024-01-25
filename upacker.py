from PIL import Image
import os, pdb

def parse_atlas(atlas_file, image_file, output_dir, skip_lines=0):
    with open(atlas_file, 'r') as f, Image.open(image_file) as img:
         # Skip the first 'skip_lines' lines
        for _ in range(skip_lines):
            next(f, None)

        texture = None
        for line in f:
            if not line.startswith('  '):  # new texture
                if texture:  # save previous texture
                    save_texture(texture, img, output_dir)
                texture = {'name': line.strip()}
            else:  # property of current texture
                key, value = line.strip().split(': ')
                if ',' in value:  # convert "x, y" to (x, y)
                    value = tuple(map(int, value.split(', ')))
                else:  # convert to int or bool
                    try:
                        value = int(value)
                    except ValueError:
                        value = value.lower() == 'true'
                texture[key] = value
        if texture:  # save last texture
            save_texture(texture, img, output_dir)

def save_texture(texture, img, output_dir):
    try:
        x, y = texture['xy']
        w, h = texture['size']
        texture_img = img.crop((x, y, x + w, y + h))
        
        base_name = f'{output_dir}/{texture["name"]}'
        extension = '.png'
        counter = 1
        while os.path.isfile(f'{base_name}_{counter}{extension}'):
            counter += 1

        texture_img.save(f'{base_name}_{counter}{extension}')
    except KeyError:
        print(f'Error: {texture["name"]} is missing xy or size property')

# usage
parse_atlas('pack.atlas', 'pack.png', 'output', skip_lines=6)
