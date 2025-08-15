document.getElementById('employee-form').addEventListener('submit', (e) => {
    e.preventDefault();
    fetch(`{% if pk %}/employee/update/{{ pk }}/{% else %}/employee/create/{% endif %}`, {
        method: 'POST',
        body: new FormData(e.target),
    }).then(response => response.json()).then(data => console.log(data));
});