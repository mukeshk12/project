from link_preview import link_preview
dict_elem = link_preview.generate_dict("https://www.youtube.com/") # this is a dict()

# Access values
title = dict_elem['title']
description = dict_elem['description']
image = dict_elem['image']
website = dict_elem['website']

print(title)
print(description)
print(image)
print(website)