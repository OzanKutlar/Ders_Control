function getStudents(){
	let elementsMatrix = [];
	
	document.querySelectorAll('[id^="mod_assign_grading-"]').forEach(el => {
		let match = el.id.match(/^mod_assign_grading-\d+_r(\d+)$/);
		if (match) {
			let rowIndex = parseInt(match[1], 10);
			elementsMatrix[rowIndex] = [];
			
			Array.from(el.children).forEach((child, colIndex) => {
				elementsMatrix[rowIndex][colIndex] = child;
			});
		}
	});
	
	return elementsMatrix;
}

function processStudentMatrix(matrix) {
	const relevantIndexes = [2, 3, 4, 8, 9];
	
	let filteredMatrix = matrix.filter(student => student[5].innerText.startsWith("Submitted for grading"));
	// let filteredMatrix = matrix.filter(student => return true);
	
	let cleanedMatrix = filteredMatrix.map(student => relevantIndexes.map(index => student[index]));
	
	cleanedMatrix.forEach(student => {
		cleanStudent(student);
	});
	
	
	return cleanedMatrix;
}

function cleanStudent(arr) {
	const link = arr[4].querySelector('a');
	if (link) {
		arr[4] = link.href;
	} else {
		console.log('No <a> tag found in the provided element.');
	}
	
	// Name
	arr[0] = arr[0].innerText;
	
	// ID
	arr[1] = arr[1].innerText;
	
	// Email
	arr[2] = arr[2].innerText;

	// Time
	arr[3] = arr[3].innerText;
	
	
}

function downloadMatrixAsJson(matrix) {
	const replacer = (key, value) => {
		if (Array.isArray(value) && value.length === 5) {
			return {
				name: value[0],
				id: value[1],
				email: value[2],
				time: value[3],
				link: value[4]
			};
		}
		return value;
	};
	
	const jsonText = JSON.stringify(matrix, replacer, 2);
	
	const blob = new Blob([jsonText], { type: 'application/json' });
	
	const link = document.createElement('a');
	
	const url = URL.createObjectURL(blob);
	
	link.href = url;
	link.download = 'matrix.json';
	
	document.body.appendChild(link);
	link.click();
	
	document.body.removeChild(link);
	URL.revokeObjectURL(url);
}




temp = getStudents();

console.log(temp.length);

temp = processStudentMatrix(temp);

if(temp.length != 0){
	downloadMatrixAsJson(temp);
}
else{
	alert("No submitted file found.");
}
