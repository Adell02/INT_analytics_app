// Show all options when the search box is clicked
function showAllOptions(Id_container,class_container) {
    var dropdown = document.getElementById(Id_container);
    dropdown.classList.toggle("show");
    document.addEventListener("click", function(event){
        hideOptionsOutsideClick(event,Id_container,class_container);
    });
}

// Function to filter options based on user input
function filterOptions(Id_container,Id_input) {
    var input, filter, div, a, i;
    input = document.getElementById(Id_input);
    filter = input.value.toUpperCase();
    div = document.getElementById(Id_container);
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
function selectOption(event,Id_container,Id_input,class_container) {
    var selectedOption = event.target.textContent;
    document.getElementById(Id_input).value = selectedOption;
    hideOptions(Id_container,class_container);
}

// Hide the dropdown options when clicking outside of the dropdown
function hideOptionsOutsideClick(event,Id_container,class_container) {
    var dropdown = document.getElementById(Id_container);
    if (!event.target.closest(class_container)) {
        dropdown.classList.remove("show");
        document.removeEventListener("click", function(event){
            hideOptionsOutsideClick(event,Id_container,class_container);
        });
    }
}

// Hide the dropdown options
function hideOptions(Id_container,class_container) {
    var dropdown = document.getElementById(Id_container);
    dropdown.classList.remove("show");
    document.removeEventListener("click", function(event){
        hideOptionsOutsideClick(event,Id_container,class_container);
    });
}



// MULTIPLE SELECTION // 

// Show all options when the search box is clicked
function Multiple_showAllOptions(Id_container,class_container) {
    var dropdown = document.getElementById(Id_container);
    dropdown.classList.toggle("show");
    document.addEventListener("click", function(event){
        Multiple_hideOptionsOutsideClick(event,Id_container,class_container);
    });
}
// Function to handle the click event on dropdown options
function Multiple_selectOption(event, Id_container, Id_input, class_container) {
    var selectedOption = event.target;
    selectedOption.classList.toggle("selected");

    var selectedOptions = document.querySelectorAll("#" + Id_container + " a.selected");
    var selectedValues = Array.from(selectedOptions).map(option => option.textContent);

    document.getElementById(Id_input).value = selectedValues.join(', ');
}

// Function to hide the dropdown options when clicking outside of the dropdown
function Multiple_hideOptionsOutsideClick(event, Id_container, class_container) {
    var dropdown = document.getElementById(Id_container);
    if (!event.target.closest(class_container)) {
        dropdown.classList.remove("show");
        document.removeEventListener("click", function (event) {
            Multiple_hideOptionsOutsideClick(event, Id_container, class_container);
        });
    }
}

// Function to hide the dropdown options
function Multiple_hideOptions(Id_container, class_container) {
    var dropdown = document.getElementById(Id_container);
    dropdown.classList.remove("show");
    document.removeEventListener("click", function (event) {
        Multiple_hideOptionsOutsideClick(event, Id_container, class_container);
    });
}
