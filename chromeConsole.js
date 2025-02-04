(function() {
    function replaceEmptySpans(textNo) {
        // Select all span elements that have a specific set of attributes
        const spans = document.querySelectorAll('span[id^="__text' + textNo + '-"]');

        spans.forEach(span => {
            // Check if the span's content is empty or contains only whitespace
            if (span.textContent.trim() === '') {
                span.textContent = 'NULL';
            }
        });
    }

    // Run the function
	// const startNo = 1;
	for (let i = 0; i < 200; i++) {
		// replaceEmptySpans(startNo + i);
		replaceEmptySpans(i);
	}

	
})();


(function() {
    // Retrieve the text content of the entire page
    var textContent = document.body.innerText || document.body.textContent;

    // Copy the text content to the clipboard
    navigator.clipboard.writeText(textContent)
        .then(() => {
            console.log('Text copied to clipboard');
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
        });
})();