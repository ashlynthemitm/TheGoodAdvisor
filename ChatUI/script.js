document.getElementById("submitButton").addEventListener("click", function () {
    var selectedStudentType = document.querySelector('input[name="student-type"]:checked');
    var inputMessageField = document.getElementById("inputMessageField");
    var outputMessageField = document.getElementById("outputMessageField");
    var rightTabHeading = document.querySelector('.right-tab h2');
    var incomingFreshmanOptions = document.getElementById("incoming-freshman-options");
    var existingCreditsOptions = document.getElementById("existing-credits-options");

     // Determine the request type based on user selection
     var findPrerequisite = false;
     var findFourYearPlan = false;
     var findSWECoursework = false;
     var completedCourses = [];

    if (selectedStudentType) {
        var selectedValue = selectedStudentType.value;

        if (selectedValue === "incoming-freshman") {
            inputMessageField.value = "Incoming Freshman";
            rightTabHeading.textContent = "How May I Assist You?";
            outputMessageField.textContent = "Welcome to Georgia State University! I am The Good Advisor! I have a few follow-up questions. Please select an option using the right tab.";
            var studentTypeContainer = document.querySelector('.radio-group');
            studentTypeContainer.innerHTML = '';
            incomingFreshmanOptions.style.display = "block";
            existingCreditsOptions.style.display = "none";
        } else if (selectedValue === "existing-credits") {
            inputMessageField.value = "Existing Credits";
            rightTabHeading.textContent = "Select Courses Taken";
            outputMessageField.textContent = "Welcome to Georgia State University! I am The Good Advisor! Please select the courses you have taken.";
            var studentTypeContainer = document.querySelector('.radio-group');
            studentTypeContainer.innerHTML = '';
            incomingFreshmanOptions.style.display = "none";
            existingCreditsOptions.style.display = "block";
        }

        // Show the input and output fields
        inputMessageField.style.display = "block";
        outputMessageField.style.display = "block";
    } else {
        outputMessageField.textContent = "Select a student type first.";
    }

   
});
