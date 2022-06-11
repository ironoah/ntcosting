/**
 * ローディング表示処理
 * @returns 
 */
function showLoading() {
    // 多重起動回避
    if ($('#loading').length) return;

    $('body').append('<div id="loading"><img src=""></div>');
    $('#loading').children('img').attr('src', path);
}

/**
 * ローディング非表示処理
 */
function hideLoading() {
    $('#loading').remove();
}

/**
 * エラーメッセージ表示
 * @param {*} message 
 */
function alertError(message){

    // 多重表示防止
    if ($('.alert-danger').length) $(".alert-danger").alert('close');

    const element = $('<div class="alert alert-danger alert-dismissible">' + message +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
    $(".alert-area").append(element);
}

/**
 * エラーメッセージ表示(フッター)
 * @param {*} message 
 */
function alertFooterError(message){

    // 多重表示防止
    if ($('.alert-danger').length) $(".alert-danger").alert('close');

    const element = $('<div class="alert alert-danger alert-dismissible">' + message +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
    $(".alert-footer-area").append(element);
}

/**
 * メッセージ非表示
 */
function alertClose() {
    if ($('.alert-danger').length) $(".alert-danger").alert('close');
    if ($('.alert-success').length) $(".alert-success").alert('close');
}

/**
 * モーダル表示処理
 * @param {*} message 
 * @param {*} btnName 
 * @param {*} callback 
 */
function showModal(message, btnName, callback) {
    var modal = $('#appModal');
    _callback = callback;

    if (typeof btnName !== "undefined") {
        modal.find('#btnCommit').text(btnName);
    }
    modal.modal('show');
    modal.find('.modal-body').html(message);
};

/**
 * モーダル - 確定ボタン押下処理
 * @param {*} obj 
 */
function onCommit(obj) {
    $('#appModal').modal('hide');
    _callback();
}