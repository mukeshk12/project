from linkpreview import Link, LinkPreview, LinkGrabber

url = "http://github.com"
grabber = LinkGrabber(
    initial_timeout=20, maxsize=1048576, receive_timeout=10, chunk_size=1024,
)
content = grabber.get_content(url)
link = Link(url, content)

preview = LinkPreview(link, parser="lxml")
print(preview)
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)