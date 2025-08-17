async function deleteEmployee(pk) {
    if (confirm('Are you sure you want to delete this employee?')) {
        try {
            const response = await fetch(`/employee/${pk}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': employeeListConfig.csrfToken
                }
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            } else {
                alert('Error deleting employee');
            }
        } catch (error) {
            alert('An error occurred: ' + error.message);
        }
    }
}