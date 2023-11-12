from flask import Flask, render_template, jsonify
from ebooklib import epub
import ebooklib

app = Flask(__name__)

@app.route('/')
def index():
    # Render the reader template
    return render_template('reader.html')

@app.route('/chapters')
def chapters():
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

    return jsonify(chapters_list)

@app.route('/chapter/<int:chapter_index>')
def chapter(chapter_index):
    # TODO: Retrieve the chapter content based on the chapter_index
    chapter_content = '<h2>Chapter {}</h2><p>Content of the chapter goes here...</p>'.format(chapter_index + 1)
    return jsonify({'content': chapter_content})

if __name__ == '__main__':
    app.run(debug=True)