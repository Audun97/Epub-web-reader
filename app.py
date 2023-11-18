from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ebooklib import epub
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Render the reader template
    return templates.TemplateResponse("reader.html", {"request": request})

@app.get("/chapters")
async def chapters():
    # Read the EPUB file
    book = epub.read_epub('samples/test.epub')

    # Function to extract chapters from TOC
    def extract_chapters(toc, index=0, level=0):
        chapters = []
        for item in toc:
            if isinstance(item, tuple):
                # If the item is a tuple, it has sub-elements
                link, sub_items = item
                chapters.append({'title': link.title, 'index': index, 'level': level})
                index += 1
                # Recursively extract chapters from sub-elements
                sub_chapters, index = extract_chapters(sub_items, index, level + 1)
                chapters.extend(sub_chapters)
            else:
                # If the item is not a tuple, it's a Link object
                chapters.append({'title': item.title, 'index': index, 'level': level})
                index += 1
        return chapters, index

    # Retrieve the list of chapters from the TOC
    chapters_list, _ = extract_chapters(book.toc)

    # Print the chapter titles to the console
    for chapter in chapters_list:
        print(f"Chapter index: {chapter['index']}, title: {chapter['title']}, level: {chapter['level']}")

    return chapters_list