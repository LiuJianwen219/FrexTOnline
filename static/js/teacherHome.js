function showExp(index){
  // console.log(index);
  // 隐藏默认信息，课程信息，班级信息，实验信息
  document.getElementById("teacherDefaultInfo").style.display = "none";
  document.getElementById("coursewareBlock").style.display = "none";
  document.getElementById("experimentBlock").style.display = "none";
  document.getElementById("classBlock").style.display = "none";

  // 显示实验文件列表的时候，隐藏班级列表
  closeByClassName("classList");
  openOrCloseByClassNameAndId("fileList", index);
}
function showExpFile(index){
  // console.log(index);
  // 隐藏欢迎界面、课件列表、学生列表
  document.getElementById("teacherDefaultInfo").style.display = "none";
  document.getElementById("coursewareBlock").style.display = "none";
  document.getElementById("classBlock").style.display = "none";

  // 显示实验文件
  document.getElementById("experimentBlock").style.display = "block";

  openOrCloseByClassNameAndId("fileGroup", index);
}
function showClass(index){
  if (ifDebugex) console.log(index);

  // 隐藏欢迎界面、课件列表、学生列表
  document.getElementById("teacherDefaultInfo").style.display = "none";
  document.getElementById("experimentBlock").style.display = "none";
  document.getElementById("classBlock").style.display = "none";

  // 显示实验文件
  document.getElementById("coursewareBlock").style.display = "block";

  // 显示班级列表的时候，隐藏实验文件列表和已经打开的模板文件
  closeByClassName("fileList");
  openOrCloseByClassNameAndId("classList", index);
  closeByClassName("templateFiles");
  closeByClassName("templateExpList");

  // 显示课程模板
  openOrCloseByClassNameAndId("templateGroup", index);
  // document.getElementById("templateOverview").style.display = "block";
}
function showClassStudent(index){
  // console.log(index);
  // 隐藏欢迎界面、课件页面、实验信息
  document.getElementById("teacherDefaultInfo").style.display = "none";
  document.getElementById("coursewareBlock").style.display = "none";
  document.getElementById("experimentBlock").style.display = "none";

  // 显示班级文件
  document.getElementById("classBlock").style.display = "block";

  openOrCloseByClassNameAndId("studentGroup", index);
}
function showTemplateInfo(index) {
  document.getElementById("templateOverview").style.display = "none";
  openOrCloseByClassNameAndId("templateExpList", index);
}


function createFreeExpProj(doc) {
    let data = new FormData();
    data.append("freeExpName", $("#"+doc).val());
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        url: 'newFreeExpProject/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            if (ifDebugex) console.log(req)
            if(req.state !== "ERROR") {
                alert("实验创建成功，点击关闭刷新");
                location.reload();
            } else{
                alert(req.info);
            }
        }
    })
}

// function uploadFreeFile(freeExpId, doc, docChange) {
//     let obj = $("#"+doc);
//     if (obj.get(0).files.length !== 0) {
//         let data = new FormData();                                      //创建formdata对象，便于将文件传输到后端
//         data.append('freeExpId', freeExpId);
//         for(let i = 0; i<obj.get(0).files.length; i+=1){
//           let f_obj = obj.get(0).files[i];                       //获取上传文件信息
//           console.log("文件对象：", f_obj);
//           console.log("文件名称是：", f_obj.name);
//           console.log("文件大小是：", f_obj.size);
//           data.append('uploadFile', f_obj);
//         }
//         data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());//在formdata对象中添加(封装)文件对象
//
//         $.ajax({
//             url: '/home/studenthome/uploadfreeexpfile/',
//             type: 'POST',
//             data: data,
//             cache: false,                                               //上传文件无需缓存
//             processData: false,                                          //不对数据做序列化操作
//             contentType: false,                                          //不定义特殊连接类型
//             success: function (req) {
//                 if(req.state !== "ERROR") {
//                     alert("文件已经上传成功，点击确定刷新页面");
//                     //location.reload();
//                     let text = "<div class=\"input-group\" id=\"freeFile_"+req.trueFileName+"\">\n" +
//                         "              <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
//                         "              <div class=\"input-group-btn\">\n" +
//                         "                <button type=\"button\" class=\"btn btn-default\"\n" +
//                         "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
//                         "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
//                         "                  删除\n" +
//                         "                </button>\n" +
//                         "              </div>\n" +
//                         "            </div>"
//                     $("#" + docChange).append(text);
//                 } else {
//                     alert(req.info);
//                 }
//             }
//         })
//     }
// }

// function deleteFreeFile(freeExpId, freeFileId, docChange) {
//     let data = new FormData();
//     data.append("freeExpId", freeExpId);
//     data.append("freeFileId", freeFileId);
//     data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
//     $.ajax({
//         url: '/home/studenthome/deletefreefile/',
//         type: 'POST',
//         data: data,
//         cache: false,                                               //上传文件无需缓存
//         processData: false,                                          //不对数据做序列化操作
//         contentType: false,                                          //不定义特殊连接类型
//         success: function (req) {
//             console.log(req)
//             if(req.state !== "ERROR") {
//                 alert("文件删除成功！");
//                 var idObject = document.getElementById(docChange);
//                 if (idObject != null) {
//                     console.log("delete");
//                     idObject.parentNode.removeChild(idObject);
//                 }
//             } else{
//                 alert(req.info);
//             }
//         }
//     })
// }

function newCourseTemplate(courseId, doc) {
    let data = new FormData();
    data.append('courseId', courseId);
    data.append('templateName', $("#"+doc).val())
    data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());//在formdata对象中添加(封装)文件对象
    $.ajax({
        url: '/course/create_template/',
        type: 'POST',
        data: data,
        cache: false,                                               //上传文件无需缓存
        processData: false,                                          //不对数据做序列化操作
        contentType: false,                                          //不定义特殊连接类型
        success: function (req) {
            if(req.state !== "ERROR") {
                alert("实验创建成功，点击确定刷新页面");
                location.reload();
            } else {
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
        if(content[i].style.display === "block")
          content[i].style.display="none";
        else if(content[i].style.display === "none")
          content[i].style.display = "block";
      }
  }
}
function closeByClassName(className) {
    let content = document.getElementsByClassName(className);
    for(let i=0; i<content.length; i+=1){
        content[i].style.display="none";
    }
}



//---------------
// function freeCompile(freeExpId, docChange) {
//     let data = new FormData();
//     data.append("freeExpId", freeExpId);
//     data.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());
//     $.ajax({
//         url: 'freecompile/',
//         type: 'POST',
//         data: data,
//         cache: false,                                               //上传文件无需缓存
//         processData: false,                                          //不对数据做序列化操作
//         contentType: false,                                          //不定义特殊连接类型
//         success: function (req) {
//             console.log(req)
//             if(req.state !== "ERROR") {
//                 alert("文件编译成功！");
//                 let text = "<div class=\"input-group\" id=\"freeFile_"+req.trueFileName+"\">\n" +
//                         "              <span id=\"lineInfo\">" + req.trueFileName + "</span>\n" +
//                         "              <div class=\"input-group-btn\">\n" +
//                         "                <button type=\"button\" class=\"btn btn-default\"\n" +
//                         "                        onclick=\"deleteFreeFile(\'"+freeExpId+"\', \'"+req.fileId+"\'," +
//                         "                                    \'freeFile_"+req.trueFileName+"\')\">\n" +
//                         "                  删除\n" +
//                         "                </button>\n" +
//                         "              </div>\n" +
//                         "            </div>"
//                 $("#" + docChange).append(text);
//             } else{
//                 alert(req.info);
//             }
//         }
//     })
// }
