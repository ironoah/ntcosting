var jobPageLength = 0;

/**
 * ページロード
 */
$(function() {
    // ページの表示数設定
    jobPageLength = $('#pageLength').val();
    // テーブル設定
    onSettingJobTable();
});

/**
 * ジョブテーブル設定
 */
function onSettingJobTable() {
    var jobTable = $('#jobTable').DataTable({
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
        // 1ページの件数
        pageLength: Number(jobPageLength),
        // 横スクロールバーを有効にする
        scrollX: true,
        // 縦スクロールバーを有効にする
        scrollY: false,
        // 件数に応じて高さを調節する
        scrollCollapse: true,
        // 列設定
        columnDefs: [
            { "width": "40px", "targets": [0] },
            { "width": "50px", "targets": [1] },
            { "width": "300px", "targets": [3] },
            { "width": "200px", "targets": [4] },
            { "width": "200px", "targets": [5] },
            { "width": "50px", "targets": [6] },
        ],
        "language": {
            "emptyTable": "実行されたジョブがありません。",
            "paginate": {
                "first": "≪",
                "last": "≫",
                "next": "＞",
                "previous": "＜"
            },
        }
    });

    // データなしの場合、pagingを非表示
    if ($('#jobTable tbody tr td').hasClass("dataTables_empty")) {
        $('#jobTable_paginate').addClass('d-none');
    }

    setTimeout(function (){
        jobTable.columns.adjust();
    }, 100);
}

/**
 * ジョブ新規作成ボタン押下処理
 * @param {*} obj 
 */
function onCreateJob(obj) {
    let action = $(obj).data('action');
    $.ajax({
        type: 'GET',
        url: action,
        beforeSend: function(){
            showLoading();
        },
    }).done(function(res) {
        if (res.count >= 2) {
            alertError(res.message);
        } else {
            location.href = '/top/job-create';
        }
    }).fail(function(e) {
        alertError('ジョブ作成判定にてエラーが発生しました。');
    }).always(function() {
        hideLoading();
    });
}

/**
 * 検索ボタン押下処理
 * @param {*} obj 
 */
function onSearchJob(obj) {
    // 入力チェック
    if (!validationCheck()) return false;

    // 検索
    onSearch();
}

/**
 * 検索処理
 */
function onSearch() {
    let action = "/top/search";
    let formData = $('#frmTop').serialize();

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
            $('#jobInfo').html(res.template);
            onSettingJobTable();
        } else if (res.result == '1') {
            // 1:エラー
            alertError(res.message);
        } else {
            // 9:異常終了
            location.href = res.route;
        }
    }).fail(function(e) {
        alertError('ジョブ検索でエラーが発生しました。');
    }).always(function() {
        hideLoading();
    });
}

/**
 * ジョブIDリンクボタン押下処理
 * @param {*} obj 
 */
function onTransitionEdit(obj) {
    $tr = $(obj).parents('tr');
    $jobId = $tr.find('input[data-col="job_id"]').val();
    $status = $tr.find('input[data-col="status"]').val();

    $('#jobId').val($jobId);
    $('#status').val($status);
    
    // 画面遷移
    let action = '/top/job-edit';
    $('#frmTop').attr('action', action).submit();
}

/**
 * 詳細リンクボタン押下処理
 * @param {*} obj 
 */
function onTransitionDetail(obj) {
    $tr = $(obj).parents('tr');
    $jobId = $tr.find('input[data-col="job_id"]').val();
    $status = $tr.find('input[data-col="status"]').val();

    $('#jobId').val($jobId);
    $('#status').val($status);
    
    // 画面遷移
    let action = '/top/job-detail';
    $('#frmTop').attr('action', action).submit();
}

/**
 * 実行ボタン押下処理
 * @param {*} obj 
 */
function onExecuteJob(obj) {
    const INF_TERMINATION_JOB = '選択されているジョブを強制終了してもよろしいですか？'
    const INF_DELETE_JOB = '選択されているジョブを削除してもよろしいですか？'
    let process = $('#selectProcess').val();

    // ステータスチェック
    if (!checkStatus(process)) return false;

    // 確認ダイアログ表示
    if (process == "1") {
        showModal(INF_TERMINATION_JOB, '強制終了', onExecute);
    } else if (process == "2") {
        showModal(INF_DELETE_JOB, '削除', onExecute);
    }
}

/**
 * 実行処理
 */
function onExecute() {
    // 更新処理
    let dict = [];
    let action = "/top/execute";
    let process = $('#selectProcess').val();

    $('#jobTable td input[type="checkbox"]:checked').each(function() {
        $tr = $(this).parents('tr');
        $jobId = $tr.find('input[data-col="job_id"]').val();
        $modTime = $tr.find('input[data-col="mod_time"]').val();
        dict.push({ 'job_id':$jobId, 'mod_time':$modTime });
    });

    $.ajax({
        url: action,
        type: 'POST',
        dataType:'json',
        data: { 
            process: process,
            jobs: JSON.stringify(dict)
        },
        beforeSend: function(){
            showLoading();
        },
    }).done(function(res) {
        if (res.result == '0') {
            // 0:正常終了
            location.href = res.route;
        } else if (res.result == '1') {
            // 1:エラー
            alertFooterError(res.message);
        } else {
            // 9:異常終了
            location.href = res.route;
        }
    }).fail(function(e) {
        alertFooterError('ジョブ実行処理でエラーが発生しました。');
    }).always(function() {
        hideLoading();
    });
}

/**
 * ステータス判定処理
 * @param {*} process 操作 
 * @returns 
 */
function checkStatus(process) {
    const ERR_NOT_SELECT_JOB = 'ジョブが選択されていません。'
    const ERR_NOT_DELETE_JOB = '実行中のジョブは削除できません。'
    const ERR_NOT_TERMINATION_JOB = '実行中でないジョブは強制終了できません。'
    // エラーメッセージ非表示
    alertClose();

    $data = $('#jobTable td input[type="checkbox"]:checked');

    // 未選択チェック
    if ($data.length == 0) {
        alertFooterError(ERR_NOT_SELECT_JOB);
        return false;
    }

    // 実行中のジョブを抽出
    $select = $data.parents('tr')
    .filter(function(){
        $status = $(this).find('input[data-col="status"]').val();
        return $status == "010"; // 010:実行中
    });

    // 強制終了
    if (process == "1") {
        if ($select.length == 0) {
            alertFooterError(ERR_NOT_TERMINATION_JOB);
            return false;
        }
    // 削除
    } else if (process == "2") {
        if ($select.length != 0) {
            alertFooterError(ERR_NOT_DELETE_JOB);
            return false;
        }
    }

    return true;
}

/**
 * 操作選択値変更処理
 * @param {*} obj 
 */
function onChangeProcess(obj)
{
    let process = $(obj).val();
    if (process === "0"){
        $('#btnExecute').prop('disabled', true);
    } else {
        $('#btnExecute').prop('disabled', false);
    }
}

/**
 * 入力チェック
 * @returns 
 */
function validationCheck() {
    // メッセージ
    const ERR_REQUIRED_FROM_DATE = '開始日時(FROM)に有効な値が入力されていません。';
    const ERR_REQUIRED_TO_DATE = '開始日時(TO)に有効な値が入力されていません。';
    const ERR_COMPARE_DATE = '開始日時(FROM)が開始日時(TO)以降となっています。';

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
        $("#fromDate").addClass("validation-error").focus();;
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