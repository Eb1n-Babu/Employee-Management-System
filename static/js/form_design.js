document.getElementById('fieldType').addEventListener('change', function() {
    const optionsInput = document.getElementById('fieldOptions');
    optionsInput.style.display = this.value === 'select' ? 'block' : 'none';
});

function addField() {
    const label = document.getElementById('fieldLabel').value;
    const type = document.getElementById('fieldType').value;
    const required = document.getElementById('fieldRequired').checked;
    const optionsInput = document.getElementById('fieldOptions').value;
    const options = type === 'select' && optionsInput ? optionsInput.split(',').map(opt => opt.trim()) : [];

    if (!label || !type) {
        alert("Please enter a label and select a type");
        return;
    }

    const fieldName = label.toLowerCase().replace(/\s+/g, '_');

    // Prevent adding a field with a name that matches a default field
    if (formDesignerConfig.defaultFields.includes(fieldName)) {
        alert("Field name conflicts with a default field. Please choose a different label.");
        return;
    }

    // Prevent duplicate dynamic field names
    if (formDesignerConfig.fields.some(field => field.name === fieldName)) {
        alert("A field with this name already exists. Please choose a different label.");
        return;
    }

    formDesignerConfig.fields.push({ name: fieldName, label: label, type: type, required: required, options: options });

    // Add to field list
    const li = document.createElement('li');
    li.setAttribute('data-name', fieldName);
    li.innerHTML = `
        ${label} (${type})${required ? ' (Required)' : ''}${options.length ? ' Options: ' + options.join(', ') : ''}
        <button onclick="removeField('${fieldName}')" class="text-red-500 ml-2">Remove</button>
    `;
    document.getElementById('field彼此

System: * Today's date and time is 03:03 PM IST on Sunday, August 17, 2025.