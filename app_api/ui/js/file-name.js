$("form").on("change", ".file-upload-field", function(){ 
    $("#input-form-label").children("span").text($(this).val().replace(/.*(\/|\\)/, ''));
});



// dragover and dragenter events need to have 'preventDefault' called
// in order for the 'drop' event to register. 
// See: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Drag_operations#droptargets
$("#input-form-label").on('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log('over trigger');
});

$('#input-form-label').on('dragenter', function(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log('enter trigger');
});

$('#input-form-label').on('drop', function(e){
    console.log(e);
    if(e.originalEvent.dataTransfer && e.originalEvent.dataTransfer.files.length) {
        e.preventDefault();
        e.stopPropagation();
        /*UPLOAD FILES HERE*/
        $("#input-form").prop("files", e.originalEvent.dataTransfer.files);
        console.log(e.originalEvent.dataTransfer.files[0].name);
        $("#input-form-label").children("span").text(e.originalEvent.dataTransfer.files[0].name);
        console.log($("#input-form"));
    }
});
