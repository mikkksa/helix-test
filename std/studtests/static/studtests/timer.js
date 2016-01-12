var chid = 4;
var mmoved = false;
var once = false;
var moved1 = false;

/*Timer code beginnig*/
//Объявим переменную
var stopTimer;
//Функция для старта
function testTimer(startTime, id) {
if(!once) {
    timebeg(id);
    once = true;
}
var gettest = document.getElementById("gettest");
//для повторного запуска очистим rezult
document.getElementById("rezult").innerHTML = '';
//выключим кнопку запуска
var bot = document.getElementById("bot");
bot.parentNode.removeChild(bot);
gettest.style.display = "";
//bot.style.display = "none";
//сколько будет длится обратный отчет
var time = startTime;
//определим сколько минут
var min = parseInt(time / 60);
if ( min < 1 ) min = 0;
	time = parseInt(time - min * 60);
if ( min < 10 ) min = '0'+min;
//определим сколько секунд
var seconds = time;
if ( seconds < 10 ) seconds = '0'+seconds;
//отрисовываем время
document.getElementById("time").innerHTML='<span>Осталось времени- '+min+' мин '+seconds+' секунд</span>';
//уменьшаем общее время на одну секунду
startTime--;
//смотрим время не закончилось
if ( startTime  >= 0 ) {
		//если нет то повторяем процедуру заново
       stopTimer  =  setTimeout(function(){testTimer(startTime); }, 1000);
	   //если закончилось, то выводим сообщение на экран, и делаем кнопку запуска активной
  } else {
     document.getElementById("time").innerHTML='<span>Осталось времени- 00 мин 00 секунд</span>';
     var rezult = document.getElementById("rezult");
     rezult.innerHTML ="Время вышло";
     //clearTimeout(stopTimer);
     //var bot = document.getElementById("bot");
     //bot.removeAttribute("disabled","disabled");
     //bot.removeChild(bot.childNodes[0]);
     //var text = document.createTextNode("Начать заново");
     //bot.appendChild(text);
   }
}
//Функция для остановки обратного отчета
function stop(){
    var gettest = document.getElementById("gettest");
    gettest.style.display = "none";
	//очистим переменную с таймером
	clearTimeout(stopTimer);
}
/*Timer code ending*/


//Functions for raitings
function rait(st){
document.getElementById('tdrat'+st).style.display = 'inline-block';
document.getElementById('tdentrat'+st).style.display = 'inline-block';
}

function edit(st){
document.getElementById('edrat'+st).style.display = 'inline-block';
document.getElementById('edentrat'+st).style.display = 'inline-block';
}
//Adding more choices to question
function addchoice() {
    chid++;
    var newDiv = document.createElement('div');
    var newinp = document.createElement('input');
    var newch = document.createElement('input');
    var name = "id"+chid.toString();
    newDiv.className='inl';
    newinp.type = 'text';
    newinp.name = 'choice_'+chid;
    newinp.id='choice_'+chid;

    newch.type='checkbox';
    newch.name=name;
    newch.id=name;

    newDiv.appendChild(newinp);
    newDiv.appendChild(newch);

    block = document.getElementById('choices');
    block.appendChild(newDiv);
}

function chname(id){
    elem = document.getElementById('d'+String(id));
    elem.name += 'c';
}

//Ajax crossplatform
function getXmlHttp(){
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
}

//Ajax menu
function dropdownsubjects()
{
    var responseserv;
    var schools;
    if(!mmoved) {
        var req = getXmlHttp();
        var el = document.getElementById("drin");
        mmoved = true;
        req.onreadystatechange = function() {

        if (req.readyState == 4) {

            if(req.status == 200) {
                responseserv = req.responseText;
                schools = responseserv.split(',');
                addschools(schools);
            }
        }
    };
        req.open('GET', '/ajtry', true);
        req.send(null);
    }
}

function addschools(schools)
{
    var el = document.getElementById("drin");
    var sub;
    for(var i = 0; i < schools.length; i++)
    {
        if(i % 2 == 0)
        {
            sub = schools[i];
        }
        else {
            var newli = document.createElement('li');
            var newa = document.createElement('a');
            newa.href = "/studtests/subjects/" + schools[i] + "/";
            newa.innerHTML = sub;
            newli.appendChild(newa);
            el.appendChild(newli);
        }
    }
}

function timebeg(id)
{
    var req = getXmlHttp();
    var body = 'time=' + id.toString();
    var responseserv;
    req.open("POST", '/ajt/', true);
    req.onreadystatechange = function() {

        if (req.readyState == 4) {
            if(req.status == 200) {
                responseserv = req.responseText;
               // alert(responseserv);
            }
        }
    };
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.send(body);
}