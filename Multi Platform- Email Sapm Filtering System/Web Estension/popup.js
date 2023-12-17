// document.addEventListener("DOMContentLoaded", function () {
//     // Load your model here using Pickle or any other method
  
//     // Handle the classify button click event
//     document.getElementById("classify-button").addEventListener("click", function () {
//       const emailText = document.getElementById("email-text").value;
  
//       // Perform feature extraction and classification using your model
//       const classificationResult = classifyEmail(emailText);
  
//       // Update the UI with the classification result
//       document.getElementById("classification-result").textContent = classificationResult;
//     });
  
//     // Function to classify the email (you need to implement this)
//     function classifyEmail(emailText) {
//       // Add your classification logic here
//       // Load your model and use it to predict if the email is spam or not
//       // Return 'Spam' or 'Ham' based on the prediction
//     }
//   });

document.addEventListener("DOMContentLoaded", function () {
    // Add an event listener to the classify button
    document.getElementById("classify-button").addEventListener("click", function () {
      const emailText = document.getElementById("email-text").value;
  
      // Perform a POST request to your Flask server to classify the email
      fetch("http://localhost:5000/classify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: emailText }),
      })
        .then((response) => response.json())
        .then((data) => {
          displayClassification(data.classification);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  
    function displayClassification(prediction) {
      const classificationResult = document.getElementById("classification-result");
  
      if (prediction === "spam") {
        classificationResult.textContent = "Prediction: This communication is spam.";
      } else if (prediction === "ham") {
        classificationResult.textContent = "Prediction: This mail is not spam.";
      } else {
        classificationResult.textContent = "Prediction: Unknown";
      }
    }
  });
  
  