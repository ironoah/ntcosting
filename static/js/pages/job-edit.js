/**
 * キャンセルボタン押下処理
 * @param {*} obj 
 */
function onCancel(obj) {
    // TOP画面へ遷移
    location.href = '/top/back';
}

/**
 * 更新ボタン押下処理
 * @param {*} obj 
 */
function onUpdateJob(obj) {
    const INF_UPDATE_JOB = 'ジョブ内容の編集を確定してよろしいですか？'

    // 入力チェック
    if (!validationCheck()) return false;

    // 確認ダイアログ表示
    showModal(INF_UPDATE_JOB, '更新', onUpdate);
}

/**
 * 更新処理
 */
function onUpdate() {
    let action = "/top/job-edit/update";
    let formData = $('#frmJobEdit').serialize();

    $.ajax({
        url: action,
        type: 'POST',
        dataType:'json',
        data: formData,
        beforeSend: function(){
            showLoading();
        },
    }).done(function(res) {
        if (res.result == '0') {
            // 0:正常終了
            location.href = res.route;
        } else if (res.result == '1') {
            // 1:エラー
            alertError(res.message);
        } else {
            // 9:異常終了
            location.href = res.route;
        }
    }).fail(function(e) {
        alertError('ジョブ編集エラー');
    }).always(function() {
        hideLoading();
    });
}

/**
 * 入力チェック
 * @returns 
 */
function validationCheck() {
    // メッセージ
    const ERR_REQUIRED_TITLE = 'タイトルが入力されていません。';
    const ERR_REQUIRED_CREATER = '作成者が入力されていません。';

    // エラー背景色を通常色へ戻す
    $("input").removeClass("validation-error");
    alertClose();

    // 入力値取得
    let title = $('#title').val();
    let creater = $('#creater').val();

    if (!title) {
        $("#title").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TITLE);
        return false;
    }

    if (!creater) {
        $("#creater").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_CREATER);
        return false;
    }

    // エラーのクラスが存在する場合は更新処理を中止
    if ($('.validation-error').length) {
        return false;
    }

    return true;
}