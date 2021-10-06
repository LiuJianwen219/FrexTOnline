function showFreeExp(index){
  closeByClassName("studentMiddleFree");
  closeByClassName("studentMiddleClass");
  openOrCloseByClassNameAndId("freeStudentExpList", index);
}

function showClassExp(index){
  closeByClassName("studentMiddleFree");
  closeByClassName("studentMiddleClass");
  openOrCloseByClassNameAndId("classStudentExpList", index);
}

function showFreeExpFile(ind, tp) {
    closeByClassName("studentMiddleClass");
    openOrCloseByClassNameAndId("studentMiddleFree", ind);
    if(tp === 'class') {
        closeByClassName("studentMiddleFree");
        openOrCloseByClassNameAndId("studentMiddleClass", ind);
    }
}

function showClassExpFile(ind, tp) {
    closeByClassName("studentMiddleFree");
    openOrCloseByClassNameAndId("studentMiddleClass", ind);
}



function createFreeExpProj(doc) {
    console.log("createFreeExpProj")
    let data = new FormData();
    data.append("freeExpName", $("#"+doc).val());
    data.append("csrfmiddlewaretoken", getCookie('csrfToken'));
    $.ajax({
        url: '/experiment/newFreeExpProject/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("实验创建成功，点击关闭刷新");
                location.reload();
            } else{
                alert(req.info);
            }
        }
    })
}



function uploadClassFile(homeworkId, doc, docChange) {
    let obj = $("#"+doc);
    if (obj.get(0).files.length !== 0) {
        let data = new FormData();                                      //创建formdata对象，便于将文件传输到后端
        data.append('homeworkId', homeworkId);
        for(let i = 0; i<obj.get(0).files.length; i+=1){
          let f_obj = obj.get(0).files[i];                       //获取上传文件信息
          console.log("文件对象：", f_obj);
          console.log("文件名称是：", f_obj.name);
          console.log("文件大小是：", f_obj.size);
          data.append('uploadFile', f_obj);
        }
        data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());//在formdata对象中添加(封装)文件对象

        $.ajax({
            url: '/file/upload_homework/',
            type: 'POST',
            data: data,
            cache: false,                                               //上传文件无需缓存
            processData: false,                                          //不对数据做序列化操作
            contentType: false,                                          //不定义特殊连接类型
            success: function (req) {
                if(req.state !== "ERROR") {
                    alert("文件已经上传成功，点击确定刷新页面");
                    //location.reload();
                    var text = "<div class=\"input-group\" id=\"classFile_"+req.trueFileName+"\">\n" +
                        "            <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
                        // "            <div class=\"input-group-btn\">\n" +
                        // "              <button type=\"button\" class=\"btn btn-default\">\n" +
                        // "                <a href=\"/home/downloadclassfile/"+req.fileId+"\">\n" +
                        // "                下载</a>\n" +
                        // "              </button>\n" +
                        // "              <button type=\"button\" class=\"btn btn-default\"\n" +
                        // "                      onclick=\"deleteClassFile(\'"+homeworkId+"\', \'"+req.fileId+"\',\n" +
                        // "                              'classFile_"+req.trueFileName+"\')\">\n" +
                        // "                删除\n" +
                        // "              </button>\n" +
                        // "            </div>\n" +
                        "          </div>"
                    $("#" + docChange).append(text);
                } else {
                    alert(req.info);
                }
            }
        })
    }
}



function classCompile(homeworkId, doc, docChange) {
    let data = new FormData();
    data.append("homeworkId", homeworkId);
    data.append("topModuleName", $("#"+doc).val())
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/experiment/course_compile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("文件编译成功！");
                var text = "<div class=\"input-group\" id=\"classFile_"+req.trueFileName+"\">\n" +
                        "            <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
                        // "            <div class=\"input-group-btn\">\n" +
                        // "              <button type=\"button\" class=\"btn btn-default\">\n" +
                        // "                <a href=\"/home/downloadclassfile/"+req.fileId+"\">\n" +
                        // "                下载</a>\n" +
                        // "              </button>\n" +
                        // "              <button type=\"button\" class=\"btn btn-default\"\n" +
                        // "                      onclick=\"deleteClassFile(\'"+homeworkId+"\', \'"+req.fileId+"\',\n" +
                        // "                              'classFile_"+req.trueFileName+"\')\">\n" +
                        // "                删除\n" +
                        // "              </button>\n" +
                        // "            </div>\n" +
                        "          </div>"
                    $("#" + docChange).append(text);
            } else{
                alert(req.info);
            }
        }
    })
}




function deleteClassFile(homeworkId, classFileId, docChange) {
    let data = new FormData();
    data.append("homeworkId", homeworkId);
    data.append("classFileId", classFileId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: '/file/delete_homework/',
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

function openOrCloseByClassNameAndId(className, id) {
    let content = document.getElementsByClassName(className);
    for(let i=0; i<content.length; i+=1){
        if(content[i].id !== id){
          content[i].style.display="none";
        }
        else{
          if(content[i].style.display === "block") {
              openWelcome();
              content[i].style.display = "none";
          }
          else if(content[i].style.display === "none") {
              closeWelcome();
              content[i].style.display = "block";
          }
        }
    }
}

function closeByClassName(className) {
    let content = document.getElementsByClassName(className);
    for(let i=0; i<content.length; i+=1){
        content[i].style.display="none";
    }
    closeWelcome();
}

function openWelcome() {
    document.getElementById('defaultStudentHome').style.display="block";
}

function closeWelcome() {
    document.getElementById('defaultStudentHome').style.display="none";
}



// 暂时没有使用
function createExpFile(expId, expType, fileList) {
    let newFileName;
    if(expType === 'free')
         newFileName = $("#newFreeFileName"+expId).val();
    else if(expType === 'class')
        newFileName = $("#newClassFileName"+expId).val();
    console.log(expId);
    console.log(newFileName);
    let data = new FormData();
    data.append("newFileName", newFileName);
    data.append("expType", expType);
    data.append("expId", expId);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: 'newExpFile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("文件创建成功");
                var txt2="<div class=\"input-group\">\n" +
                    "  <span id=\"lineInfo\">"+req.trueFileName+"</span>\n" +
                    "  <div class=\"input-group-btn\">\n" +
                    "    <button type=\"button\" class=\"btn btn-default\">修改</button>\n" +
                    "    <button type=\"button\" class=\"btn btn-default\">删除</button>\n" +
                    "  </div>\n" +
                    "</div>";
                $("#"+fileList).append(txt2);
            } else{
                alert(req.info);
            }
        }
    })
}
function modifyFile(expId, fileName, expType) {
    console.log(expId);
    console.log(fileName);
    console.log(expType);
    let data = new FormData();
    data.append("expId", expId);
    data.append("fileName", fileName);
    data.append("expType", expType);
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: 'modifyFile/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            console.log(req)
            if(req.state !== "ERROR") {
                alert("文件修改成功！");
            } else{
                alert("实验创建失败，请检查名字长度不能过长，实验不能重名");
            }
        }
    })
}

function getCookie(cname) {
     var name = cname + "=";
     var ca = document.cookie.split(';');
     for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if(c.indexOf(name) == 0)
           return c.substring(name.length,c.length);
     }
     return "";
}
