function doPost(e){
            //来源消息&指令
            var body = JSON.parse(e.postData.contents);
            //执行回复响应主函数
            var payload = preparePayload(body);
            //TG数据封装与转换
            var data = {
                "method": "post",
                "payload": JSON.stringify(payload),
                "contentType": 'application/json',
            }

            UrlFetchApp.fetch("https://api.telegram.org/bot{BOT_TOKEN}}/", data);
}
//主函数
function preparePayload(body){
	var payload;
  var valid_user=['sb'];

	//message
	if (body.message) {
    if(valid_user.indexOf(body.message.chat.username)!=-1||body.message.chat.id=="-123456789"){
      body.message.chat.id = body.message.chat.id + '';
      body.message.text=body.message.text.replace("@xxxxx_bot","");

      if (body.message.text == "/startup") {
        // 发送消息
        var payload = {
          "method": "sendMessage",
          "chat_id": body.message.chat.id,
          "text": "临时通道服务开启..\nhttp://xxxxx:8000"
        };

        // 访问API地址
        var apiUrl = "http://{host}/abcd?s=start";
        var options = {
          'muteHttpExceptions': false,
          'fetchTimeoutSeconds': 359 // 设置超时时间为 6 秒
        };

        try {
          var response = UrlFetchApp.fetch(apiUrl, options);
          Logger.log(response.getContentText());
          // 处理服务器的响应
        } catch (e) {
          Logger.log("请求发送中断：" + e);
          // 处理请求发送失败的情况
        }
      }else if (body.message.text == "/stop") {
        // 发送消息
        var payload = {
          "method": "sendMessage",
          "chat_id": body.message.chat.id,
          "text": "临时服务关闭.."
        };

        // 访问API地址
        var apiUrl = "http://{host}/abcd?s=stop";
        var response = UrlFetchApp.fetch(apiUrl);
        Logger.log(response.getContentText());
      }else if (body.message.text == "/backup") {
        // 发送消息
        var payload = {
          "method": "sendMessage",
          "chat_id": body.message.chat.id,
          "text": "本次调用地址： http://{host}/abcd?s=backup"
        };


        // 访问API地址
        // var apiUrl = "http://{host}/abcd?s=backup";
        // var options = {
        //   'muteHttpExceptions': false,
        //   'fetchTimeoutSeconds': 359 // 设置超时时间为 6 秒
        // };

        // try {
        //   var response = UrlFetchApp.fetch(apiUrl, options);
        //   Logger.log(response.getContentText());
        //   // 处理服务器的响应
        // } catch (e) {
        //   Logger.log("请求发送中断：" + e);
        //   // 处理请求发送失败的情况
        // }

      }
    }
  }
  return payload
}

