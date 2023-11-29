// Show all options when the search box is clicked
function showAllOptions() {
    var dropdown = document.getElementById("myDropdown");
    dropdown.classList.toggle("show");
    document.addEventListener("click", hideOptionsOutsideClick);
}

// Function to filter options based on user input
function filterOptions() {
    var input, filter, div, a, i;
    input = document.getElementById("dropdownInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
    div.classList.add("show");
}

// Function to handle the click event on dropdown options
function selectOption(event) {
    var selectedOption = event.target.textContent;
    document.getElementById("dropdownInput").value = selectedOption;
    hideOptions();
}

// Hide the dropdown options when clicking outside of the dropdown
function hideOptionsOutsideClick(event) {
    var dropdown = document.getElementById("myDropdown");
    if (!event.target.closest('.dropdown')) {
        dropdown.classList.remove("show");
        document.removeEventListener("click", hideOptionsOutsideClick);
    }
}

// Hide the dropdown options
function hideOptions() {
    var dropdown = document.getElementById("myDropdown");
    dropdown.classList.remove("show");
    document.removeEventListener("click", hideOptionsOutsideClick);
}

