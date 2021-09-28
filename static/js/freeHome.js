var type = null;
var expId = null;
var nReady = null;
var nBusy = null;
var nError = null;

function freeCompile(freeExpId, doc, docChange) {
    let data = new FormData();
    data.append("freeExpId", freeExpId);
    data.append("topModuleName", $("#"+doc).val());
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/experiment/freecompile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("文件编译成功！");
                let text = "<div class=\"input-group\" id=\"freeFile_"+req.trueFileName+"\">\n" +
                        "              <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
                        "              <div class=\"input-group-btn\">\n" +
                        "                <button type=\"button\" class=\"btn btn-default\">\n" +
                        "                  <a href=\"/home/downloadfreefile/"+req.fileId+"\">\n" +
                        "                  下载</a>\n" +
                        "                </button>"+
                        "                <button type=\"button\" class=\"btn btn-default\"\n" +
                        "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
                        "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
                        "                  删除\n" +
                        "                </button>\n" +
                        "              </div>\n" +
                        "            </div>"
                $("#" + docChange).append(text);
            } else{
                alert(req.info);
            }
        }
    })
}

function uploadFreeFile(freeExpId, doc, docChange) {
    let obj = $("#"+doc);
    if (obj.get(0).files.length !== 0) {
        let data = new FormData();                                      //创建formdata对象，便于将文件传输到后端
        data.append('freeExpId', freeExpId);
        for(let i = 0; i<obj.get(0).files.length; i+=1){
          let f_obj = obj.get(0).files[i];                       //获取上传文件信息
          console.log("文件对象：", f_obj);
          console.log("文件名称是：", f_obj.name);
          console.log("文件大小是：", f_obj.size);
          data.append('uploadFile', f_obj);
        }
        data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());//在formdata对象中添加(封装)文件对象

        $.ajax({
            url: '/file/uploadfreeexpfile/',
            type: 'POST',
            data: data,
            cache: false,                                               //上传文件无需缓存
            processData: false,                                          //不对数据做序列化操作
            contentType: false,                                          //不定义特殊连接类型
            success: function (req) {
                if(req.state !== "ERROR") {
                    alert("文件已经上传成功，点击确定刷新页面");
                    //location.reload();
                    let text = "<div class=\"input-group\" id=\"freeFile_"+req.trueFileName+"\">\n" +
                        "              <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
                        "              <div class=\"input-group-btn\">\n" +
                        "                <button type=\"button\" class=\"btn btn-default\">\n" +
                        "                  <a href=\"/file/downloadfreefile/"+req.fileId+"\">\n" +
                        "                  下载</a>\n" +
                        "                </button>"+
                        "                <button type=\"button\" class=\"btn btn-default\"\n" +
                        "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
                        "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
                        "                  删除\n" +
                        "                </button>\n" +
                        "              </div>\n" +
                        "            </div>"
                    $("#" + docChange).append(text);
                } else {
                    alert(req.info);
                }
            }
        })
    }
}
function deleteFreeFile(freeExpId, freeFileId, docChange) {
    let data = new FormData();
    data.append("freeExpId", freeExpId);
    data.append("freeFileId", freeFileId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/file/deletefreefile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("文件删除成功！");
                var idObject = document.getElementById(docChange);
                if (idObject != null) {
                    console.log("delete");
                    idObject.parentNode.removeChild(idObject);
                }
            } else{
                alert(req.info);
            }
        }
    })
}

function startToExp(t, id, btnDoc) {
  document.getElementById(btnDoc).setAttribute('disabled', 'disabled')
  setTimeout(function () {
    testLJW();//建立连接
    setTimeout(function () {
      setTimeout(function () {
        document.getElementById('deviceInfo').innerText = "可用设备 " + nReady + ", 忙碌设备 " + nBusy + ", 故障设备 " + nError;
        if(nReady > 0){
            document.getElementById(btnDoc).removeAttribute('disabled')
        }
      }, 500)
    }, 300)
  }, 300)
  type = t
  expId = id
}

function getDevice() {
    if(type == null || expId == null){
        alert("网页错误，请重新尝试！");
        return;
    }
    window.location.href="/experiment/experiment/?type="+type+"&expId="+expId;
}
