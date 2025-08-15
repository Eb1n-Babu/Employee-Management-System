document.addEventListener('DOMContentLoaded', () => {
    new Sortable(document.getElementById('fields-container'), { animation: 150 });
    document.getElementById('add-field').addEventListener('click', () => {
        const field = document.createElement('div');
        field.className = 'field';
        field.innerHTML = `<input type="text" class="label" placeholder="Label"><select class="type"><option value="text">text</option><option value="number">number</option><option value="date">date</option><option value="password">password</option></select>`;
        document.getElementById('fields-container').appendChild(field);
    });
    document.getElementById('save-form').addEventListener('click', () => {
        const fields = Array.from(document.querySelectorAll('.field')).map(f => `${f.querySelector('.label').value},${f.querySelector('.type').value}`);
        fetch('/form-design/', {
            method: 'POST',
            body: new URLSearchParams({ 'fields[]': fields }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).then(response => response.json()).then(data => console.log(data));
    });
});