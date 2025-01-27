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