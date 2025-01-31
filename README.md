# Reverse-Baron
This is a set of reverse engineering tools made for the browser puzzle game site [PuzzleBaron](https://puzzlebaron.com/). 


## Wordtwist Bookmarklet
```javascript
javascript:(function(){const e='https://raw.githubusercontent.com/bear148/reverse-baron/main/wordtwist/wordtwist.puzzlebaron.com/js/md5.js';fetch(e).then(e=>e.text()).then(e=>{const t=Array.from(document.getElementsByTagName('script')).find(e=>e.src.includes('md5.js'));t&&t.remove();const n=document.createElement('script');n.type='text/javascript',n.text=e,document.head.appendChild(n),console.log('MD5 replaced')}).catch(e=>console.error('MD5 replace failed:',e))})();
```

## Campsites Bookmarklet
```javascript
javascript:(function() {fetch('https://raw.githubusercontent.com/bear148/reverse-baron/main/campsites/auto-place.js').then(response => response.text()).then(scriptText => {let script = document.createElement('script');script.textContent = scriptText + '\nautoPlaceTents();';document.body.appendChild(script);}).catch(error => console.error('Failed to load script:', error));})();
```

## Typing.com Bookmarklet
```javascript
javascript:(function() {fetch('https://raw.githubusercontent.com/bear148/reverse-baron/main/typing.com/auto-type.js').then(response => response.text()).then(scriptText => {let script = document.createElement('script');script.textContent = scriptText + '\nautoTypeWords();';document.body.appendChild(script);}).catch(error => console.error('Failed to load script:', error));})();
```
