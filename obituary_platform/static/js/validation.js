(function () {
    const form = document.getElementById("obituaryForm");
    if (!form) {
        return;
    }

    const fields = {
        name: document.getElementById("name"),
        date_of_birth: document.getElementById("date_of_birth"),
        date_of_death: document.getElementById("date_of_death"),
        content: document.getElementById("content"),
        author: document.getElementById("author"),
    };

    function showError(fieldName, message) {
        const messageBox = form.querySelector(`[data-error-for="${fieldName}"]`);
        fields[fieldName].classList.toggle("invalid", Boolean(message));
        messageBox.textContent = message;
    }

    function validate() {
        let valid = true;
        Object.keys(fields).forEach((fieldName) => showError(fieldName, ""));

        if (!fields.name.value.trim()) {
            showError("name", "Please enter the person's name.");
            valid = false;
        }

        if (!fields.date_of_birth.value) {
            showError("date_of_birth", "Please enter the date of birth.");
            valid = false;
        }

        if (!fields.date_of_death.value) {
            showError("date_of_death", "Please enter the date of death.");
            valid = false;
        }

        if (fields.date_of_birth.value && fields.date_of_death.value) {
            const birth = new Date(fields.date_of_birth.value);
            const death = new Date(fields.date_of_death.value);
            if (death < birth) {
                showError("date_of_death", "Date of death cannot be earlier than date of birth.");
                valid = false;
            }
        }

        if (fields.content.value.trim().length < 20) {
            showError("content", "Please write at least 20 characters.");
            valid = false;
        }

        if (!fields.author.value.trim()) {
            showError("author", "Please enter the author's name.");
            valid = false;
        }

        return valid;
    }

    form.addEventListener("submit", function (event) {
        if (!validate()) {
            event.preventDefault();
        }
    });
})();
