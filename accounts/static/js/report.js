function hiddendiscription(){
    td = document.getElementsByClassName("td-desc")
    th = document.getElementById("th-desc")

    if (td[0].hidden == true && th.hidden==true){
    for(i=0;i<td.length;i++){
        td[i].removeAttribute('hidden')
    }
    th.removeAttribute('hidden')
    }
    else{
     for(i=0;i<td.length;i++){
        td[i].setAttribute('hidden',true)
    }
    th.setAttribute('hidden',true)
    }   
}
