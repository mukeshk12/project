from linkpreview import link_preview

url = "http://localhost"
content = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <!-- ... --->
        <title>a title</title>
    </head>
    <body>
    <!-- ... --->
    </body>
</html>
"""
preview = link_preview(url, content)
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)