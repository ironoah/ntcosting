/**
 * ボタン制御処理
 */
function onBtnLoginCtrl(){

    let user = $('#userId').val();
    let pass = $('#password').val();
    let lenUser = $.trim(user.replace(/\r?\n/g, "")).length;
    let lenPass = $.trim(pass.replace(/\r?\n/g, "")).length;

    // ボタン非活性
    $('#btnLogin').prop('disabled', true);

    // 入力がある場合ボタン活性
    if (lenUser !== 0 && lenPass !== 0) $('#btnLogin').prop('disabled', false);
}

/**
 * ログイン
 * @param {*} obj 
 */
function onLogin(obj) {

    // submit
    showLoading();
    $('#frmLogin').submit();
}
