function getStudents(){
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

function processStudentMatrix(matrix) {
	const relevantIndexes = [3, 2, 5, 6];
	
	let cleanedMatrix = matrix.map(student => relevantIndexes.map(index => student[index]));
	
	cleanedMatrix.forEach(student => {
		cleanStudent(student);
	});
	
	
	return cleanedMatrix;
}

function cleanStudent(arr) {
	
	// Ders Kodu
	arr[0] = arr[0].innerText;
	
	// Section
	arr[1] = arr[1].innerText;
	
	// Hoca
	arr[2] = arr[2].innerText;

	// Time
	arr[3] = arr[3].innerText;
	
	
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
	alert("No classes found.");
}
