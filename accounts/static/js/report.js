function hiddendiscription(){
    td = document.getElementById("td-desc")
    th = document.getElementById("th-desc")
    if (td.hidden == true && th.hidden==true){
        td.removeAttribute('hidden')
        th.removeAttribute('hidden')
    }
    else{
        td.setAttribute('hidden',true)
        th.setAttribute('hidden',true)
    }   
}