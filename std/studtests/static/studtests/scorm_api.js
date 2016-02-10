function findAPI(win) { //ищем в родительских окнах объект с названием API.
            var findAPITries=0; //будем считать количество попыток, чтобы поиск не был бесконечным.
            while ((win.API_1484_11 == null) && (win.parent != null) && (win.parent != win)) {
                findAPITries++;
                if (findAPITries > 20) return null; //число 20 взято условно, теоретически его может и не хватить.
                win = win.parent;
            }
            return win.API_1484_11;
        }
function getAPI() { //получаем объект API для текущего SCO.
    var theAPI = findAPI(window); //сначала пробуем искать в родителях текущего окна.
    if ((theAPI == null)) { //если не нашли в родителях текущего окна,
        if ((window.opener != null) && (typeof(window.opener) != "undefined"))
            theAPI = findAPI(window.opener); //то попробуем найти в родителях окна, открывшего текущее.
    }
    return theAPI;
}
function start() { //эта функция сработает в момент открытия SCO.
    var api = getAPI();
    if (api!=null) {
        api.Initialize("");
        value=api.GetValue("cmi.learner_name"); //запрашиваем у системы имя учащегося,
        document.write("Имя учащегося: "+value); //и выводим его на экран.
    }
    else document.write("Не удаётся подключиться к API системы.");
}
function stop() { //эта функция сработает в момент закрытия SCO.
    var api = getAPI();
    if (api!=null) api.Terminate("");
}