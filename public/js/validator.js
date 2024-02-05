import { f2 } from './Module_Chrono.js';
document.getElementById('flagSubmitForm').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/flagSubmit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            flag: document.getElementById('flag').value,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.querySelector('.response').innerText = `Error: ${data.error}`;
            document.querySelector('.response').style.color = 'red';
            document.getElementById('username').value = '';
            document.getElementById('flag').value = '';

        } else {
            document.querySelector('.response').innerText = `Success: ${data.success}`;
            document.querySelector('.response').style.color = 'green';
            document.getElementById('username').value = '';
            document.getElementById('flag').value = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
f2 ();

var textAreas = document.getElementsByTagName('textarea');
Array.prototype.forEach.call(textAreas, function(elem) {
    elem.placeholder = elem.placeholder.replace(/\\n/g, '\n');
});