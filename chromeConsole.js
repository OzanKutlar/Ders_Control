(function() {
    function replaceEmptySpans(textNo) {
        // Select all span elements that have a specific set of attributes
        const spans = document.querySelectorAll('span[id^="__text' + textNo + '-"][data-sap-ui^="__text' +  + textNo + '-"]');

        spans.forEach(span => {
            // Check if the span's content is empty or contains only whitespace
            if (span.textContent.trim() === '') {
                span.textContent = 'NULL';
            }
        });
    }

    // Run the function
    replaceEmptySpans(9);
	replaceEmptySpans(10);
	replaceEmptySpans(11);
	replaceEmptySpans(12);
	replaceEmptySpans(13);
	replaceEmptySpans(14);
	replaceEmptySpans(15);
	replaceEmptySpans(16);
	
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