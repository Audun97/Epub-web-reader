window.onload = function() {
    loadChapters();
    loadChapterContent();
};

function loadChapters() {
    // Fetch the list of chapters from the server
    fetch('/chapters')
        .then(response => response.json())
        .then(chapters => {
            const chaptersList = document.getElementById('chapters');
            chapters.forEach(chapter => {
                let listItem = document.createElement('li');
                let link = document.createElement('a');
                link.href = '#';
                link.textContent = chapter.title;
                link.onclick = function() { loadChapterContent(chapter.index); };
                // Set the CSS margin based on the chapter level
                link.style.marginLeft = (chapter.level * 20) + 'px';
                listItem.appendChild(link);
                chaptersList.appendChild(listItem);
            });
        });
}

function loadChapterContent(chapterIndex) {
    // TODO: Fetch chapter content from the server based on chapterIndex
    const contentDiv = document.getElementById('content');
    // This is a placeholder for the chapter content
    contentDiv.innerHTML = '<h2>Chapter ' + (chapterIndex + 1) + '</h2><p>Content of the chapter goes here...</p>';
}