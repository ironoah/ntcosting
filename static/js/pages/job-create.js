/**
 * ページロード
 */
$(function() {
    // 今日の日付を設定
    let date = new Date();
    let year = date.getFullYear();
    let month = ("0" + (date.getMonth() + 1)).slice(-2);
    let day = ("0" + date.getDate()).slice(-2);
    let today = year + "-" +  month + "-" + day;
    document.getElementById("bcastDate").value = today;
    
    // 現在時刻-30minを設定
    let defaultTime = document.getElementById("defaultTime").value;
    // let defaultDate = date.getTime() - (defaultTime * 60 * 1000);
    date.setMinutes(date.getMinutes() - defaultTime);
    let hour = ("0" + date.getHours()).slice(-2);
    let minutes = ("0" + date.getMinutes()).slice(-2);
    let now = hour + ":" + minutes;
    document.getElementById("bcastTime").value = now;
});

/**
 * キャンセルボタン押下処理
 * @param {*} obj 
 */
function onCancel(obj) {
    // TOP画面へ遷移
    location.href='/top/back';
}

/**
 * 実行ボタン押下処理
 * @param {*} obj 
 */
function onExecuteJob(obj) {
    const INF_EXECUTE_JOB = 'ジョブの新規登録を実施してよろしいですか。<br>ループ箇所特定ジョブが即時実行されます。'

    // 入力チェック
    if (!validationCheck()) return false;

    // 確認ダイアログ表示
    showModal(INF_EXECUTE_JOB, '登録', onRegist);
}

/**
 * 登録処理
 */
function onRegist() {
    let action = "/top/job-create/regist";
    let formData = $('#frmJobCreate').serialize();

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
        alertError("ジョブ新規登録エラーが発生しました。");
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
    const ERR_REQUIRED_BCAST_DATE = '使用BCASTデータ日に有効な値が入力されていません。';
    const ERR_REQUIRED_BCAST_TIME = '使用BCASTデータ時間に有効な値が入力されていません。';

    // エラー背景色を通常色へ戻す
    $("input").removeClass("validation-error");
    alertClose(); 

    // 入力値取得
    let title = $('#title').val();
    let creater = $('#creater').val();
    let bcastDate = $('#bcastDate').val();
    let bcastTime = $('#bcastTime').val();

    // タイトル
    if (!title) {
        $("#title").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TITLE);
        return false;
    }
    // 作成者
    if (!creater) {
        $("#creater").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_CREATER);
        return false;
    }
    // 使用BCASTデータ日
    if (!bcastDate) {
        $("#bcastDate").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_BCAST_DATE);
        return false;
    }
    // 使用BCASTデータ時間
    if (!bcastTime) {
        $("#bcastTime").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_BCAST_TIME);
        return false;
    }

    // エラーのクラスが存在する場合は更新処理を中止
    if ($('.validation-error').length) {
        return false;
    }

    return true;
}