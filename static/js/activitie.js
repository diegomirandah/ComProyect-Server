function setProgresBar(key){
    progresbar  = document.getElementById("progressBar")
    switch (key) {
        case 1:
            progresbar.style.width = "1%";
            progresbar.classList.add("progress-bar-striped");
            progresbar.classList.add("progress-bar-animated");
            break;

        case 100:
            progresbar.style.width = "100%";
            progresbar.classList.remove("progress-bar-striped");
            progresbar.classList.remove("progress-bar-animated");
            break;
    
        default:
            if (key >1 && key < 100) {
                progresbar.style.width = key+"%";
            } else {
                progresbar.style.width = key+"1%";         
            }
            break;
    }
}

processOpenPose.onclick = async (e) => {
    console.log("processOpenPose")
    e.preventDefault();
    setProgresBar(1);
    let formData = new FormData();
    formData.append('act_id', document.getElementById("actId").value);
    formData.append('user_id', 1);
    formData.append('input', document.getElementById("video1").value);
    formData.append('output', document.getElementById("video1output").value);
    var start = new Date();
    var time = null
    let response = await fetch('/processOpenPose', { method: 'POST', body: formData });
    let data = await response.json();
    time = new Date() - start;
    setProgresBar(25);
    //console.log(time)
    formData.set("user_id",2)
    formData.set("input",document.getElementById("video2").value)
    formData.set("output",document.getElementById("video2output").value)
    response = await fetch('/processOpenPose', { method: 'POST', body: formData });
    data = await response.json();
    time = new Date() - start;
    setProgresBar(50);
     //console.log(time)
    formData.set("user_id",3)
    formData.set("input",document.getElementById("video3").value)
    formData.set("output",document.getElementById("video3output").value)
    response = await fetch('/processOpenPose', { method: 'POST', body: formData });
    data = await response.json();
    time = new Date() - start;
    setProgresBar(75);
     //console.log(time)
    formData.set("user_id",4)
    formData.set("input",document.getElementById("video4").value)
    formData.set("output",document.getElementById("video4output").value)
    response = await fetch('/processOpenPose', { method: 'POST', body: formData });
    data = await response.json();
    time = new Date() - start;
    setProgresBar(100);
     //console.log(time)
    
};

processPostures.onclick = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    setProgresBar(1);
    formData.append('act_id', document.getElementById("actId").value);
    formData.append('user_id', 1);
    let response = await fetch('/processPostures', { method: 'POST', body: formData });
    let data = await response.json();
    setProgresBar(25);
    formData.set("user_id",2)
    response = await fetch('/processPostures', { method: 'POST', body: formData });
    data = await response.json();
    setProgresBar(50);
    formData.set("user_id",3)
    response = await fetch('/processPostures', { method: 'POST', body: formData });
    data = await response.json();
    setProgresBar(75);
    formData.set("user_id",4)
    response = await fetch('/processPostures', { method: 'POST', body: formData });
    data = await response.json();
    setProgresBar(100);
};