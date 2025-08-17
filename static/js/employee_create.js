<<<<<<< HEAD
document.getElementById('employeeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = this;
    const formData = new FormData(form);
    const data = {
        form_data: Object.fromEntries(formData),
        extra_fields: employeeFormFields.reduce((acc, field) => {
            acc[field.name] = {
                type: field.type,
                label: field.label,
                required: field.required,
                options: field.options || []
            };
            return acc;
        }, {}),
        heading: "{{ form_heading|default:'Employee Information Form' }}"
    };

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.status === 'success') {
            window.location.href = '{% url "employee_list" %}';
        } else {
            alert('Error: ' + JSON.stringify(result.errors));
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    }
});
=======
>>>>>>> 8baf7ad (revert some changes)
