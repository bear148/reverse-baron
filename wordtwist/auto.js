function readFile(file) {
    return new Promise(function(resolve, reject) {
        let fr = new FileReader();

        fr.onload = function() {
            resolve(JSON.parse(fr.result));
        }

        fr.onerror = function() {
            reject(fr);
        }

        fr.readAsText(file);
    })
}

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function reverseLookupMD5(md5, dictionaryFile) {
    let out = document.getElementById("md5_reversed");

    readFile(dictionaryFile).then(async (dictionary) => {
        for (let word in dictionary) {
            if (dictionary[word] === md5) {
                out.innerHTML = word;
                break;
            }
            // await delay(50); // Add 10ms delay between words
        }
    }).catch(err => {
        console.error("Error reading dictionary:", err);
        out.innerHTML = "Error reading dictionary";
    });
}