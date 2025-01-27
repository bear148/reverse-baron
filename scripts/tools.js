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

function readFile(file) {
    return new Promise(function(resolve, reject) {
        let fr = new FileReader();

        fr.onload = function() {
            resolve(fr.result);
        }

        fr.onerror = function() {
            resolve(fr);
        }

        fr.readAsText(file);
    })
}

// md5Files is an array where the first value in the array is the md5File containing all of the md5Codes, and the
// second value in the array is the file with all the words and corresponding line number for the MD5 code.
function reverseLookupMD5(md5, md5Files) {
    let readers = [];
    let out = document.getElementById("md5_reversed");

    for(let i = 0;i < md5Files.length;i++){
        readers.push(readFile(md5Files[i]));
    }

    Promise.all(readers).then((values) => {
        let a_md5 = values[0].split(/\r?\n|\r|\n/g);
        let loc = 0; // LOC is the line number starting at 0, so the actual number is loc + 1
        for (let i = 0; i < a_md5.length; i++) {
            if (a_md5[i] == md5) {
                loc = i;
                break
            }
        }

        let a_w = values[1].split(/\r?\n|\r|\n/g);
        out.innerHTML = a_w[loc];
        console.log(`Word: ${a_w[loc]} | Line: ${loc+1}`);
    });
}