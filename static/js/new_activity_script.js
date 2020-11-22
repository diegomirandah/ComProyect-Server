act = null

h = 0;
m = 0;
s = 0;
document.getElementById("hms").innerHTML="00:00:00";

function init(){
    h = 0;
    m = 0;
    s = 0;
    document.getElementById("hms").innerHTML="00:00:00";
}

CreateActivity.onsubmit = async (e) => {
    e.preventDefault();

    await fetch('/new_activity/config', {
        method: 'POST',
        body: new FormData(CreateActivity)
    })
    .then(response => response.json())
    .then(data => {
        act = data
        console.log(data)
        document.getElementById("alert1success").hidden = false;
        document.getElementById("Activate").hidden = false;
    })
    .catch(error => {
        console.log(error)
        document.getElementById("alert1anger").hidden = false;
    });
};


startRecording.onclick = async (e) => {
    e.preventDefault();
    //console.log(act)
    let formData = new FormData();
    formData.append('data_act', JSON.stringify(act));
    console.log(act)
    await fetch('/new_activity/start', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data["out"] != ""){
            document.getElementById('terminal').innerHTML=data["out"];
            document.getElementById("startRecording").disabled = true;
            cronometrar()
        }
        if(data["err"] != ""){
            document.getElementById('terminal').innerHTML=data["err"];
            document.getElementById("startRecording").disabled = false;
            init()
        }
    })
    .catch(error => {
        console.log(error)
        init()
    });
};

stopRecording.onclick = async (e) => {
    e.preventDefault();
    //console.log(act)
    let formData = new FormData();
    formData.append('data_act', JSON.stringify(act));
    console.log(act)
    await fetch('/new_activity/stop', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        parar();
        if(data["out"] != ""){
            document.getElementById('terminal').innerHTML=data["out"];
            document.getElementById("startRecording").disabled = false;
            init()
        }
        if(data["err"] != ""){
            document.getElementById('terminal').innerHTML=data["err"];
            document.getElementById("startRecording").disabled = false;
            init()
        }
    })
    .catch(error => {
        console.log(error)
        init()
    });
};

testRecording.onclick = async (e) => {
    e.preventDefault();
    //console.log(act)
    let formData = new FormData();
    formData.append('data_act', JSON.stringify(act));
    console.log(act)
    await fetch('/new_activity/test', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.log(error)
    });
};

function cronometrar(){
    escribir();
    id = setInterval(escribir,1000);
}
function escribir(){
    var hAux, mAux, sAux;
    s++;
    if (s>59){m++;s=0;}
    if (m>59){h++;m=0;}
    if (h>24){h=0;}

    if (s<10){sAux="0"+s;}else{sAux=s;}
    if (m<10){mAux="0"+m;}else{mAux=m;}
    if (h<10){hAux="0"+h;}else{hAux=h;}

    document.getElementById("hms").innerHTML = hAux + ":" + mAux + ":" + sAux; 
    
    var minutos = (h * 60) + m;

    if(act["durationOfActivity"] == minutos){
        parar();
    }
}
function parar(){
    clearInterval(id);
    endRecording()
}

function endRecording() {
    let formData = new FormData();
    formData.append('data_act', JSON.stringify(act));
    console.log(act)
    fetch('/new_activity/end', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data["out"] != "")
            document.getElementById('terminal').innerHTML=data["out"];
        if(data["err"] != "")
            document.getElementById('terminal').innerHTML=data["err"];
    })
    .catch(error => {
        console.log(error)
    });
}