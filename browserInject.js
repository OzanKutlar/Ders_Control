function getClasses(){
	let elementsMatrix = [];
	
	document.querySelectorAll('[id*="moduleTable-"]').forEach(el => {
		// console.log("Checking " + el.id);
		let match = el.id.match(/__item\d+-__xmlview\d+--moduleTable-(\d+)$/m);
		if (match) {
			// console.log("Matched " + match[1]);
			let rowIndex = parseInt(match[1], 10);
			elementsMatrix[rowIndex] = [];
			
			Array.from(el.children).forEach((child, colIndex) => {
				elementsMatrix[rowIndex][colIndex] = child;
			});
		}
	});
	
	return elementsMatrix;
}

function processDates(input) {
    let regex = /\s*([A-Z]{3})\s*:\s*/g;
    let matches = [...input.matchAll(regex)];
    
    let result = [];
    
    for (let i = 0; i < matches.length; i++) {
        let startIndex = matches[i].index;
        let endIndex = (i + 1 < matches.length) ? matches[i + 1].index : input.length;
        let entry = input.substring(startIndex, endIndex).trim();
        
        // Remove trailing "-"
        entry = entry.replace(/\s*-\s*$/, '');
        
        result.push(entry);
    }

    return result;
}


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

function processStudentMatrix(matrix) {
	const relevantIndexes = [3, 2, 5, 6,7,8];
	
	let cleanedMatrix = matrix.map(student => relevantIndexes.map(index => student[index]));
	
	cleanedMatrix.forEach(student => {
		cleanStudent(student);
	});
	
	
	return cleanedMatrix;
}

function cleanStudent(arr) {
    for (let i = 0; i < arr.length; i++) {
        arr[i] = arr[i].innerText;
    }

    arr[3] = processDates(arr[3]);
}


function downloadMatrixAsJson(matrix) {
	const replacer = (key, value) => {
		if (Array.isArray(value) && value.length === 5) {
			return {
				name: value[0],
				section: value[1],
				teacher: value[2],
				time: value[3],
			};
		}
		return value;
	};
	
	const jsonText = JSON.stringify(matrix, replacer, 2);
	
	const blob = new Blob([jsonText], { type: 'application/json' });
	
	const link = document.createElement('a');
	
	const url = URL.createObjectURL(blob);
	
	// Ask user for filename
	let filename = prompt("Enter the file name (without extension):", "matrix");
	if (!filename) {
		filename = "matrix"; // fallback default
	}
	
	link.href = url;
	link.download = filename + ".json";
	
	document.body.appendChild(link);
	link.click();
	
	document.body.removeChild(link);
	URL.revokeObjectURL(url);
}



for (let i = 0; i < 200; i++) {
	// replaceEmptySpans(startNo + i);
	replaceEmptySpans(i);
}


temp = getClasses();

console.log(temp.length);

temp = processStudentMatrix(temp);

if(temp.length != 0){
	downloadMatrixAsJson(temp);
}
else{
	alert("No classes found.");
}
