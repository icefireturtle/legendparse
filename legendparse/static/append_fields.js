const getURL = window.location.pathname;
const basePath = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
const [lead, view, record] = getURL.split("/");
const apiURL = `${basePath}/api/${record}`;
console.log(apiURL);
let elementCount = 0;

async function fetchAndCount(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const rows = Array.isArray(data) ? data : (data.rows ?? []);
    elementCount = rows.length;
    console.log(data);
    console.log(rows);
    console.log(elementCount);
    return elementCount;
}

fetchAndCount(apiURL)
    .then(count => { console.log('Rows:', count); 
    })
    .catch(err => console.error(err));

document.getElementById('addForm').addEventListener('click', function(event){
event.preventDefault();
elementCount+=1;
console.log(elementCount);

const newFormEntry = document.getElementById('newFormEntry');

const form = document.createElement('form');
form.className = 'newForm';
form.action = `/append_fields/${record}`;
form.method = 'POST';

const newTable = document.createElement('table');

const newTableHead = document.createElement('thead');

newTable.append(newTableHead);

const newTableHeaderFName = document.createElement('th');
newTableHeaderFName.textContent ='Field Name';

const newTableHeaderFDesc = document.createElement('th');
newTableHeaderFDesc.textContent = 'Field Description';

const newTableHeaderFLen = document.createElement('th');
newTableHeaderFLen.textContent ='Field Length';

newTableHead.append(newTableHeaderFName);
newTableHead.append(newTableHeaderFDesc);
newTableHead.append(newTableHeaderFLen);

const row = document.createElement('tr');
row.className = 'addFieldsWrapper';

var newFieldNameCell = document.createElement('td');
var newFieldDescCell = document.createElement('td');
var newFieldLengthCell = document.createElement('td');

var newFieldNameInput = document.createElement('input');
var newFieldDescInput = document.createElement('input');
var newFieldLengthInput = document.createElement('input');

newFieldNameInput.type = 'text';
newFieldNameInput.name = 'fieldName';
newFieldNameInput.id = 'fieldName' + (elementCount);
newFieldNameInput.placeholder = 'Field Name ' + (elementCount);

newFieldDescInput.type = 'text';
newFieldDescInput.name = 'fieldDesc';
newFieldDescInput.id = 'fieldDesc' + (elementCount);
newFieldDescInput.placeholder = 'Field Description ' + (elementCount);

newFieldLengthInput.type = 'text';
newFieldLengthInput.name = 'fieldLength';
newFieldLengthInput.id = 'fieldLength' + (elementCount);
newFieldLengthInput.placeholder = 'Field Length ' + (elementCount);

row.append(newFieldNameCell);
row.append(newFieldDescCell);
row.append(newFieldLengthCell);

newFieldNameCell.appendChild(newFieldNameInput);
newFieldDescCell.appendChild(newFieldDescInput);
newFieldLengthCell.appendChild(newFieldLengthInput);

var removeButton = document.createElement('button');
removeButton.textContent = 'Remove';
removeButton.classList.add('removeField','btn','btn-outline-danger','btn-sm');
removeButton.addEventListener('click', function(event) {
    event.preventDefault();
    event.currentTarget.parentElement.remove(); 
    console.log(event.currentTarget.parentElement, event.currentTarget.closest('.addFieldsWrapper'));
    elementCount-=1;
});

row.appendChild(removeButton);

var extendAppendRow = document.createElement('tr');
extendAppendRow.className = 'appendWrapper';
extendAppendRow.id = 'appendWrapper';
var extendAppendCol = document.createElement('td');

extendAppendCol.colSpan = '4';

var appendButton = document.createElement('button');
appendButton.textContent = 'Append Fields';
appendButton.classList.add('appendField', 'btn', 'btn-outline-success', 'btn-sm');
appendButton.type = 'submit';

extendAppendCol.appendChild(appendButton);

newTable.appendChild(newTableHead);
newTable.appendChild(row);
newTable.appendChild(extendAppendRow);
newTable.appendChild(extendAppendCol);
form.appendChild(newTable);
newFormEntry.appendChild(form);

});
