function ValidateFileUpload() {
    var fuData = document.getElementById('fileUpload');
    var FileUploadPath = fuData.value;

    //To check if user upload any file
    if (FileUploadPath == '') {
        return true;

    } else {
        var Extension = FileUploadPath.substring(FileUploadPath.lastIndexOf('.') + 1).toLowerCase();

        //The file uploaded is an image
        if (Extension == "gif" || Extension == "png" || Extension == "bmp" || Extension == "jpeg" || Extension == "jpg") {
            return true;
        } 

        //The file upload is NOT an image
        else {
            alert("Picture only allows file types of GIF, PNG, JPG, JPEG and BMP. ");
            return false;
        }
    }
}

function form_submit() {
    if(ValidateFileUpload()) {
        alert("Form berhasil disubmit!");
        document.getElementById("broadcast_form").submit();
    } 
}
