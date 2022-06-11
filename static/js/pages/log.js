/******************************
 * メッセージ                  *
 ******************************/
const ERR_REQUIRED_FROM_DATE = '発生日(FROM)に有効な値が入力されていません。';
const ERR_REQUIRED_TO_DATE = '発生日(TO)に有効な値が入力されていません。';
const ERR_COMPARE_DATE = '発生日(FROM)が発生日(TO)以降となっています。';
var logPageLength = 0;

/**
 * ページロード
 */
$(function() {
    // ページの表示数設定
    logPageLength = $('#pageLength').val();
    // 今日の日付を設定
    let date = new Date();
    let year = date.getFullYear();
    let month = ("0" + (date.getMonth() + 1)).slice(-2);
    let day = ("0" + date.getDate()).slice(-2);
    let today = year + "-" +  month + "-" + day;
    document.getElementById("fromDate").value = today;
    document.getElementById("toDate").value = today;

    // テーブル設定
    onSettingLogTable();
});

/**
 * ログテーブル設定
 */
function onSettingLogTable() {
    var logTable = $('#logTable').DataTable({
        // 件数切替機能 無効
        lengthChange: false,
        // 検索機能 無効
        searching: false,
        // ソート機能 無効
        ordering: false,
        // 検索情報表示 無効
        info: false,
        // ページング機能 有効
        paging: true,
        // ページングタイプ
        pagingType: "full_numbers",
        // ページ内件数
        pageLength: Number(logPageLength),
        // 横スクロールバーを有効にする
        scrollX: true,
        // 縦スクロールバーを有効にする
        scrollY: '50vh',
        // 件数に応じて高さを調節する
        scrollCollapse: true,
        // 列設定
        columnDefs: [
            { "width": "90px", "targets": [0] },
            { "width": "70px", "targets": [1] },
            { "width": "50px", "targets": [2] },
            { "width": "90px", "targets": [3] },
            { "width": "90px", "targets": [4] },
            { "width": "200px", "targets": [5] },
            { "width": "70px", "targets": [6] },
            { "width": "300px", "targets": [7] },
        ],
        "language": {
            "emptyTable": "表示するログがありません。",
            "paginate": {
                "first": "≪",
                "last": "≫",
                "next": "＞",
                "previous": "＜"
            },
        }
    });

    // データなしの場合、pagingを非表示
    if ($('#logTable tbody tr td').hasClass("dataTables_empty")) {
        $('#logTable_paginate').addClass('d-none');
    }

    setTimeout(function (){
        logTable.columns.adjust();
    }, 100);
}

/**
 * 検索ボタン押下処理
 * @param {*} obj 
 */
function onSearchLog(obj) {
    // 入力チェック
    if (!validationCheck()) return false;

    // 検索
    onSearch();
}

/**
 * 検索処理
 */
function onSearch() {
    let action = "/top/log/search";
    let formData = $('#frmLog').serialize();

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
            $('#logInfo').html(res.template);
            onSettingLogTable();
        } else if (res.result == '1') {
            // 1:エラー
            alertError(res.message);
        } else {
            // 9:異常終了
            location.href = res.route;
        }
    }).fail(function(e) {
        alertError('ログ検索でエラーが発生しました。');
    }).always(function() {
        hideLoading();
    });
}

/**
 * CSV保存ボタン押下処理
 * @param {*} obj
 */
function onOutputCsv(obj) {
    // 入力チェック
    if (!validationCheck()) return false;

    // CSVダウウンロード
    let action = '/top/log/csv-download';
    $('#frmLog').attr('action', action).submit();
}

/**
 * Text保存ボタン押下処理
 * @param {*} obj 
 */
function onOutputTxt(obj) {
    // 入力チェック
    if (!validationCheck()) return false;

    // Txtダウウンロード
    let action = '/top/log/txt-download';
    $('#frmLog').attr('action', action).submit();
}

/**
 * 入力チェック
 * @returns 
 */
function validationCheck() {

    // エラー背景色を通常色へ戻す
    $("input").removeClass("validation-error");
    alertClose();

    // 入力値取得
    let fromDate = $('#fromDate').val();
    let toDate = $('#toDate').val();

    // 発生日(FROM)：入力チェック
    if (!fromDate) {
        $("#fromDate").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_FROM_DATE);
        return false;
    }
    // 発生日(TO)：入力チェック
    if (!toDate) {
        $("#toDate").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TO_DATE);
        return false;
    }
    // 発生日(FROM, TO)の大小比較
    if (new Date(fromDate) > new Date(toDate)) {
        $("#fromDate").addClass("validation-error").focus();
        $("#toDate").addClass("validation-error");
        alertError(ERR_COMPARE_DATE);
        return false;
    }

    // エラーのクラスが存在する場合は更新処理を中止
    if ($('.validation-error').length) {
        return false;
    }

    return true;
}

/**
 * 発生日(FROM)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurFromDate(obj) {
    // エラー背景色を通常色へ戻す
    $("#fromDate").removeClass("validation-error");
    alertClose();

    // 入力値取得
    let fromDate = $(obj).val();

    // 発生日(FROM)：入力チェック
    if (!fromDate) {
        $("#fromDate").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_FROM_DATE);
        return false;
    }
}

/**
 * 発生日(TO)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurToDate(obj) {

    // エラー背景色を通常色へ戻す
    $("#toDate").removeClass("validation-error");
    alertClose();

    // 入力値取得
    let toDate = $(obj).val();

    // 発生日(TO)：入力チェック
    if (!toDate) {
        $("#toDate").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TO_DATE);
        return false;
    }
}

/**
 * ジョブIDリンクボタン押下処理
 * @param {*} obj 
 */
function onTransitionDetail(obj) {
    $tr = $(obj).parents('tr');
    $jobId = $tr.find('td a[data-col="job_id"]').text();

    $('#jobId').val($jobId);
    
    // 画面遷移
    let action = '/top/job-detail';
    $('#frmLog').attr('action', action).submit();
}