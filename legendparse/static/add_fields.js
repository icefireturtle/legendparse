let elementCount = 0;

document.getElementById('addFields').addEventListener('click', function(event){
event.preventDefault();
elementCount+=1;

const paramsContainer = document.getElementById('paramsContainer');
const wrapper = document.createElement('tr');
wrapper.className = 'paramsWrapper'; 

var newFieldNameCell = document.createElement('td');
var newFieldLengthCell = document.createElement('td');
var newFieldDescCell = document.createElement('td');

var newFieldNameInput = document.createElement('input');
var newFieldLengthInput = document.createElement('input');
var newFieldDescInput = document.createElement('input');

newFieldNameInput.type = 'text';
newFieldNameInput.name = 'fieldName';
newFieldNameInput.id = 'fieldName' + (elementCount + 1);
newFieldNameInput.placeholder = 'Field Name ' + (elementCount + 1);

newFieldLengthInput.type = 'text';
newFieldLengthInput.name = 'fieldLength';
newFieldLengthInput.id = 'fieldLength' + (elementCount + 1);
newFieldLengthInput.placeholder = 'Field Length ' + (elementCount + 1);

newFieldDescInput.type = 'text';
newFieldDescInput.name = 'fieldDesc';
newFieldDescInput.id = 'fieldDesc' + (elementCount + 1);
newFieldDescInput.placeholder = 'Field Description ' + (elementCount + 1);

wrapper.append(newFieldNameCell);
wrapper.append(newFieldLengthCell);
wrapper.append(newFieldDescCell);

newFieldNameCell.appendChild(newFieldNameInput);
newFieldLengthCell.appendChild(newFieldLengthInput);
newFieldDescCell.appendChild(newFieldDescInput);

var removeButton = document.createElement('button');
removeButton.textContent = 'Remove';
removeButton.classList.add('removeField','btn','btn-outline-danger','btn-sm');
removeButton.addEventListener('click', function(event) {
    event.preventDefault();
    event.currentTarget.parentElement.remove();
    console.log(event.currentTarget.parentElement, event.currentTarget.closest('.paramsWrapper'));
    elementCount-=1;
});

wrapper.appendChild(removeButton);
paramsContainer.appendChild(wrapper);
});