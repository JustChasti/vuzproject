const http = require("http");
const fs = require("fs");
  
http.createServer(function(request, response){
      
    console.log(`Запрошенный адрес: ${request.url}`);
    // получаем путь после слеша
    const filePath = request.url.substr(1);
    // смотрим, есть ли такой файл
    fs.access(filePath, fs.constants.R_OK, err => {
        // если произошла ошибка - отправляем статусный код 404
        if(err){
            response.statusCode = 404;
            response.end("Resourse not found!");
        }
        else{

            fs.readFile(filePath, "utf8", function(error, data){
                 
                let header = "Главная страница";
                let headerT = "Страница товаров";

                const tovarsArr = require('./data.json');
                var arrName = [];

                for (var i = 0; i < tovarsArr.length; i++) {//вывод tovarov
                    arrName[i] ='<li>' + tovarsArr[i].name; + '</li>';
                  };


                data = data.replace("{header}", header).replace("{headerT}", headerT).replace("{arrName}", arrName);
                response.end(data);
            });

            //fs.createReadStream(filePath).pipe(response);

        }
      });
}).listen(3000, function(){
    console.log("Server started at 3000");
});
