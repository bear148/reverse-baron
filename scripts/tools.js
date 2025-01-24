function reverseTimestampOperation() {
    // Convert seconds to milliseconds
    let milliseconds = document.getElementById("timestamp_conversion_r").value * 1000;
    // Add 5 hours (in milliseconds) back to the timestamp
    let adjustedTime = milliseconds + 5 * 60 * 60 * 1000;
  
    // Convert the adjusted time back to a Date object
    let originalDate = new Date(adjustedTime);
  
    document.getElementById("final_time_r").innerText = originalDate;

    return originalDate;
}

function timestampOperation() {
    // Subtract 5 hours (in milliseconds) from the input date
    let date = new Date(document.getElementById("timestamp_conversion_t").value);
    let adjustedDate = new Date(date - 5 * 60 * 60 * 1000);
  
    // Convert the adjusted date to seconds since the Unix epoch and round it
    let timestampInSeconds = Math.round(adjustedDate.getTime() / 1000);
  
    document.getElementById("final_time_t").innerText = timestampInSeconds;

    return timestampInSeconds;
  }