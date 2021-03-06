var type = null;
var expId = null;
var nReady = null;
var nBusy = null;
var nError = null;

function freeCompile(freeExpId, doc, other_file_name, docChange) {
    let data = new FormData();
    data.append("freeExpId", freeExpId);
    data.append("topModuleName", $("#"+doc).val());
    data.append("fileNameOther", $("#"+other_file_name).val())
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/experiment/free_compile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            if (ifDebugex) console.log(req)
            if(req.state !== "ERROR") {
                alert("编译提交成功！请等待编译（5分钟）");
                // let text = "<div class=\"input-group\" id=\"freeFile_"+req.trueFileName+"\">\n" +
                //         "              <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
                //         "              <div class=\"input-group-btn\">\n" +
                //         "                <button type=\"button\" class=\"btn btn-default\">\n" +
                //         "                  <a href=\"/home/downloadfreefile/"+req.fileId+"\">\n" +
                //         "                  下载</a>\n" +
                //         "                </button>"+
                //         "                <button type=\"button\" class=\"btn btn-default\"\n" +
                //         "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
                //         "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
                //         "                  删除\n" +
                //         "                </button>\n" +
                //         "              </div>\n" +
                //         "            </div>"
                // $("#" + docChange).append(text);
            } else{
                alert(req.info);
            }
        }
    })
}

function getCompileStatus(expId, docChange) {
    let data = new FormData();
    data.append('expId', expId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/experiment/get_compile_status/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (req) {
            if (req.state !== "ERROR") {
                let table = document.getElementById(docChange)
                let nodeList = table.childNodes;
                for(let i=nodeList.length-1; i>=0; i--){
                    table.removeChild(nodeList[i]);
                }
                console.log(req.compileStatus)
                for (let i = 0; i < req.compileStatus.length; i += 1) {
                    var txt2 =
                        "<tr>" +
                        "<td>" + req.compileStatus[i].fileName + "</td>" +
                        "<td>" + req.compileStatus[i].startTime + "</td>" +
                        "<td>" + req.compileStatus[i].stopTime + "</td>" +
                        "<td>" + req.compileStatus[i].status + "</td>" +
                        "</tr>";
                    $("#"+docChange).append(txt2);
                }
            } else {
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
          if (ifDebugex) console.log("文件对象：", f_obj);
          if (ifDebugex) console.log("文件名称是：", f_obj.name);
          if (ifDebugex) console.log("文件大小是：", f_obj.size);
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
                        // "              <div class=\"input-group-btn\">\n" +
                        // "                <button type=\"button\" class=\"btn btn-default\">\n" +
                        // "                  <a href=\"/file/downloadfreefile/"+req.fileId+"\">\n" +
                        // "                  下载</a>\n" +
                        // "                </button>"+
                        // "                <button type=\"button\" class=\"btn btn-default\"\n" +
                        // "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
                        // "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
                        // "                  删除\n" +
                        // "                </button>\n" +
                        // "              </div>\n" +
                        "            </div>"
                    $("#" + docChange).append(text);
                } else {
                    alert(req.info);
                }
            }
        })
    }
}

function getFileContent(fileId, doc){
    let data = new FormData();
    data.append('fileId', fileId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/file/get_experiment_file_content/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (req) {
            if(req.state !== "ERROR") {
                // alert("OK");
                document.getElementById(doc).innerHTML = req.fileContent
            } else {
                alert(req.info);
            }
        }
    })
}

function editFile(fileId, doc){
    let data = new FormData();
    data.append('type', "class");
    data.append('fileId', fileId);
    data.append('fileContent', $("#"+doc).val());
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/file/edit_experiment_file/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (req) {
            if(req.state !== "ERROR") {
                alert("文件已经修改");
            } else {
                alert(req.info);
            }
        }
    })
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
            if (ifDebugex) console.log(req)
            if(req.state !== "ERROR") {
                alert("文件删除成功！");
                var idObject = document.getElementById(docChange);
                if (idObject != null) {
                    if (ifDebugex) console.log("delete");
                    idObject.parentNode.removeChild(idObject);
                }
            } else{
                alert(req.info);
            }
        }
    })
}

function deleteFreeExp(freeExpId) {
    let data = new FormData();
    data.append("expId", freeExpId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/experiment/deleteFreeExpProject/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            if (ifDebugex) console.log(req)
            if(req.state !== "ERROR") {
                alert("实验删除成功！");
                location.reload();
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
