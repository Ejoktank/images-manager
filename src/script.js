
// Устанавилваем новую картинку
function setImage(name) {
    return function(res) {
        res.blob()
            .then((blob) => {
                var reader = new FileReader() ;
                reader.onload = function(){ 
                    const img = document.getElementById(name);
                    img.src = this.result;
                } ; 
                reader.readAsDataURL(blob) ;
            });
    }
}

const fileinput = document.getElementById('customFile');
fileinput.onchange = function () {

    const data = new FormData()
    data.append('file', fileinput.files[0]);

    // Делаем запрос к серверу
    fetch('/upload', {
        method: 'POST',
        body: data
    })
    .then((res) => {
         // Делаем еще один запрос и устанавливаем оригинальную картинку
        fetch('/current').then(setImage('original-image')).catch('Все сломалось :(');

        // Устанавливаем уже отредактированную картинку
        setImage('edited-image')(res);
    })
    .catch((e) => {
        console.log("Все сломалось :(");
    });
};

