copyBtn = document.getElementById('copy-btn');

copyBtn.addEventListener('click', copy_func);

function copy_func() {
    var copyText = document.getElementById("shorten-link-field");
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
    document.execCommand("copy");
}