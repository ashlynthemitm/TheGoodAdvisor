document.getElementById("submitButton").addEventListener("click", function() {
    var selectedStudentType = document.querySelector('input[name="student-type"]:checked');
    var inputMessageField = document.getElementById("inputMessageField");
    var outputMessageField = document.getElementById("outputMessageField");
    var rightTabHeading = document.querySelector('.right-tab h2');
    var incomingFreshmanOptions = document.getElementById("incoming-freshman-options");
    var existingCreditsOptions = document.getElementById("existing-credits-options");
    var existingOptions = document.getElementById("existing-credits-container");
    var fourYearPlanOption = document.querySelector('input[name="student-option"][value="four-year-plan"]');
    var softwareEngineeringCourseworkOption = document.querySelector('input[name="student-option"][value="software-engineering1"]');
    var preReqForCourseOption = document.querySelector('input[name="student-option"][value="prerequisites1"]');
    var dataScienceCertificateOption = document.querySelector('input[name="student-option"][value="data-science-certificate"]');
    var cyberSecurityCertificateOption = document.querySelector('input[name="student-option"][value="cybersecurity-certificate"]');
    var existingDataScienceCertificateOption = document.querySelector('input[name="existing-option"][value="datascience-cert"]');
    var existingCyberSecurityCertificateOption = document.querySelector('input[name="existing-option"][value="cyber-security-cert"]');
    outputMessageField.textContent = ""; // Clear existing output message


    outputMessageField.style.display = "block";


    if (selectedStudentType) {
        var selectedValue = selectedStudentType.value;

        if (selectedValue === "incoming-freshman") {
            if(selectedValue==="incoming-freshman") {
                inputMessageField.value = "Incoming Freshman";
                outputMessageField.textContent = "Welcome to Georgia State University! We are excited to have you join our incoming freshman class.";
                rightTabHeading.textContent = "How May I Assist You?";
                var studentTypeContainer = document.querySelector('.radio-group');
                studentTypeContainer.innerHTML = '';


                incomingFreshmanOptions.style.display = "block";
                existingCreditsOptions.style.display = "none";

                var sendButton1 = document.getElementById('submitButton');
                sendButton1.addEventListener('click', function (){
                    if (fourYearPlanOption && fourYearPlanOption.checked) {

                        outputMessageField.textContent = "Here is your four year plan";
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.style.display = "none";
                        var statusMessage = document.getElementById('statusMessageField');
                        statusMessage.textContent = '';

                    }
                    else if (softwareEngineeringCourseworkOption && softwareEngineeringCourseworkOption.checked) {
                        outputMessageField.textContent = "Here is your Software Engineering Coursework.";
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.style.display = "none";
                        var statusMessage = document.getElementById('statusMessageField');
                        statusMessage.textContent = '';
                    }

                    else if (preReqForCourseOption && preReqForCourseOption.checked) {
                        inputMessageField.value = "Pre-requisite for Course";
                        outputMessageField.textContent = "Select and send the course you would like a pre-requisite for on the right tab.";
                        rightTabHeading.textContent = "Select The Course";
                        incomingFreshmanOptions.style.display = "none";
                        existingCreditsOptions.style.display = "none";

                        var preReqForCourseOptionsContainer = document.getElementById("pre-req-options-container");
                        var sendButton = document.getElementById('submitButton');
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.appendChild(preReqForCourseOptionsContainer); // Append pre-requisite radio buttons to the right tab
                        preReqForCourseOptionsContainer.style.display = "block";

                        sendButton.style.position = 'absolute';
                        sendButton.style.bottom = '1rem'; // Set desired bottom position
                        sendButton.style.left = '50%'; // Set left position to the center
                        sendButton.style.transform = 'translateX(-50%)';
                        sendButton.style.width = ''; // Reset width to default (if overridden)
                        sendButton.style.height = '';
                        var preReqSelected = document.querySelector('input[name="course-taken"]:checked');

                        if (preReqSelected) {
                            var selectedCourse = preReqSelected.value;

                            // Display pre-requisites for the selected course in the output message field
                            inputMessageField.value = "Pre-requisite for Course";
                            outputMessageField.textContent = `Here are the pre-requisites for ${selectedCourse}: [List your pre-requisites here]`;

                            // Hide the right tab
                            var rightTab = document.querySelector('.right-tab');
                            rightTab.style.display = "none";

                            // Clear any existing status or messages
                            var statusMessage = document.getElementById('statusMessageField');
                            statusMessage.textContent = '';
                        }
                    }

                    else if (dataScienceCertificateOption && dataScienceCertificateOption.checked) {
                        outputMessageField.textContent = "Here is your Data Science Certificate Coursework.";
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.style.display = "none";
                        var statusMessage = document.getElementById('statusMessageField');
                        statusMessage.textContent = '';
                    }
                    else if (cyberSecurityCertificateOption && cyberSecurityCertificateOption.checked) {
                        outputMessageField.textContent = "Here is your CyberSecurity Certificate Coursework.";
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.style.display = "none";
                        var statusMessage = document.getElementById('statusMessageField');
                        statusMessage.textContent = '';
                    }
                    else{
                        // Handle the case if no course is selected for pre-requisites
                        outputMessageField.textContent = "Please select a course for pre-requisites.";
                    }
                })



            }
        } else if (selectedValue === "existing-credits") {
            if (selectedValue === "existing-credits") {
                inputMessageField.value = "Existing Credits";
                outputMessageField.textContent = "Please select the courses you have already taken.";
                rightTabHeading.textContent = "Select Courses Taken";

               var studentTypeContainer = document.querySelector('.radio-group');
               studentTypeContainer.innerHTML = '';
                incomingFreshmanOptions.style.display = "none";
                existingCreditsOptions.style.display = "block";

                // Checkboxes logic when at least one checkbox is selected and "Send" is clicked
                var sendButton2 = document.getElementById('submitButton');
                sendButton2.addEventListener('click', function () {var checkboxes = document.querySelectorAll('input[name="course-taken"]:checked');
                    if (checkboxes.length > 0) {
                        inputMessageField.value = "Pre-requisite for Course";
                        outputMessageField.textContent = "Select an option on the right tab";
                        rightTabHeading.textContent = "Select An Option";
                        incomingFreshmanOptions.style.display = "none";
                        existingCreditsOptions.style.display = "none";

                        // Assuming there's a container for the new options
                        var existingCredits2Options = document.getElementById("ExistingCredits2-options");
                        var rightTab = document.querySelector('.right-tab');
                        rightTab.appendChild(existingCredits2Options); // Append the new options to the right tab
                        existingCredits2Options.style.display = "block";
                        var softwareEngineeringInternshipOption = document.querySelector('input[name="existing-option"][value="Software Engineering Internship"]');
                        var remainingPlanOption = document.querySelector('input[name="existing-option"][value="Remaining Plan"]');
                        var prereqoption = document.querySelector('input[name="existing-option"][value="Pre-Req For Course"]');
                        if (softwareEngineeringInternshipOption && softwareEngineeringInternshipOption.checked) {
                            outputMessageField.textContent = "Here is the track to prepare for a SWE Internship.";
                            // Additional logic if needed for the SWE Internship track
                        } else if (remainingPlanOption && remainingPlanOption.checked) {
                            outputMessageField.textContent = "Here are the list of courses needed in order for you to graduate.";
                            // Additional logic for the remaining plan
                        } else if (prereqoption && prereqoption.checked) {                        inputMessageField.value = "Pre-requisite for Course";
                            outputMessageField.textContent = "Select and send the course you would like a pre-requisite for on the right tab.";
                            rightTabHeading.textContent = "Select The Course";
                            incomingFreshmanOptions.style.display = "none";
                            existingCreditsOptions.style.display = "none";

                            var preReqForCourseOptionsContainer = document.getElementById("pre-req-options-container");
                            var sendButton = document.getElementById('submitButton');
                            var rightTab = document.querySelector('.right-tab');
                            rightTab.appendChild(preReqForCourseOptionsContainer); // Append pre-requisite radio buttons to the right tab
                            preReqForCourseOptionsContainer.style.display = "block";

                            sendButton.style.position = 'absolute';
                            sendButton.style.bottom = '1rem'; // Set desired bottom position
                            sendButton.style.left = '50%'; // Set left position to the center
                            sendButton.style.transform = 'translateX(-50%)';
                            sendButton.style.width = ''; // Reset width to default (if overridden)
                            sendButton.style.height = '';
                            var preReqSelected = document.querySelector('input[name="course-taken"]:checked');

                            if (preReqSelected) {
                                var selectedCourse = preReqSelected.value;

                                // Display pre-requisites for the selected course in the output message field
                                inputMessageField.value = "Pre-requisite for Course";
                                outputMessageField.textContent = `Here are the pre-requisites for ${selectedCourse}: [List your pre-requisites here]`;

                                // Hide the right tab
                                var rightTab = document.querySelector('.right-tab');
                                rightTab.style.display = "none";

                                // Clear any existing status or messages
                                var statusMessage = document.getElementById('statusMessageField');
                                statusMessage.textContent = '';
                            }

                        }
                        else if (existingDataScienceCertificateOption && existingDataScienceCertificateOption.checked) {
                            outputMessageField.textContent = "Here is your Data Science Certificate Coursework.";
                            var rightTab = document.querySelector('.right-tab');
                            rightTab.style.display = "none";
                            var statusMessage = document.getElementById('statusMessageField');
                            statusMessage.textContent = '';
                        }
                        else if (existingCyberSecurityCertificateOption && existingCyberSecurityCertificateOption.checked) {
                            outputMessageField.textContent = "Here is your CyberSecurity Certificate Coursework.";
                            var rightTab = document.querySelector('.right-tab');
                            rightTab.style.display = "none";
                            var statusMessage = document.getElementById('statusMessageField');
                            statusMessage.textContent = '';
                        }
                        else {
                            // Handle the case if no checkboxes are selected
                            outputMessageField.textContent = "Please select at least one course taken.";
                        }
                    }
                })
            }
        }



        // Show the input and output fields only after clicking send
        inputMessageField.style.display = "block";
        outputMessageField.style.display = "block";



    }

    // sendRequestToServer('/generate-four-year-plan', requestData);
    // sendRequestToServer('/find-prerequisite', requestData);
   function sendReuestToServer(url, requestData) {
        fetch(url, {
            method:'POST',
            headers: {
                'Content-type':'application/json',
            },
            body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(data=>
            { document.getElementById("outputMessageField").textContent = JSON.stringify(data);
    })
    .catch(error=>{
        console.error('Error:', error)
        document.getElementById("outputMessageField").textContent = 'An error occurred';
    })
   }

})

