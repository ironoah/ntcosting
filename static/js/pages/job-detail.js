$(function(){
    if ($('#loopTable').length){
        var loopTable = $('#loopTable').DataTable({
            // 件数切替機能 無効
            lengthChange: false,
            // 検索機能 無効
            searching: false,
            // ソート機能 無効
            ordering: false,
            // 検索情報表示 無効
            info: false,
            // ページング機能 無効
            paging: false,
            // 横スクロールバーを有効にする
            scrollX: true,
            // 縦スクロールバーを有効にする
            scrollY: '30vh',
            // 件数に応じて高さを調節する
            scrollCollapse: true,
            // 列設定
            columnDefs: [
                { "width": "150px", "targets": [0] },
                { "width": "100px", "targets": [1] },
                { "width": "90px", "targets": [2] },
                { "width": "90px", "targets": [3] },
                { "width": "130px", "targets": [4] },
                { "width": "325px", "targets": [5] },
                { "width": "325px", "targets": [6] },
                { "width": "70px", "targets": [7] },
                { "width": "70px", "targets": [8] },
            ],
            "language": {
                "emptyTable": "表示するデータがありません。",
            }
        });
    
        setTimeout(function (){
            loopTable.columns.adjust();
        }, 100);
    }

    if ($('#machineTable').length){
        var machineTable = $('#machineTable').DataTable({
            // 件数切替機能 無効
            lengthChange: false,
            // 検索機能 無効
            searching: false,
            // ソート機能 無効
            ordering: false,
            // 検索情報表示 無効
            info: false,
            // ページング機能 無効
            paging: false,
            // 横スクロールバーを有効にする
            scrollX: true,
            // 縦スクロールバーを有効にする
            scrollY: '30vh',
            // 件数に応じて高さを調節する
            scrollCollapse: true,
            // 列設定
            columnDefs: [
                { "width": "150px", "targets": [0] },
                { "width": "100px", "targets": [1] },
                { "width": "90px", "targets": [2] },
                { "width": "90px", "targets": [3] },
                { "width": "130px", "targets": [4] },
                { "width": "325px", "targets": [5] },
                { "width": "325px", "targets": [6] },
                { "width": "70px", "targets": [7] },
                { "width": "70px", "targets": [8] },
            ],
            "language": {
                "emptyTable": "表示するデータがありません。",
            }
        });

        setTimeout(function (){
            machineTable.columns.adjust();
        }, 100);
    }

    if ($('#disconnectTable').length){
        var disconnectTable = $('#disconnectTable').DataTable({
            // 件数切替機能 無効
            lengthChange: false,
            // 検索機能 無効
            searching: false,
            // ソート機能 無効
            ordering: false,
            // 検索情報表示 無効
            info: false,
            // ページング機能 無効
            paging: false,
            // 横スクロールバーを有効にする
            scrollX: true,
            // 縦スクロールバーを有効にする
            scrollY: '30vh',
            // 件数に応じて高さを調節する
            scrollCollapse: true,
            // 列設定
            columnDefs: [
                { "width": "150px", "targets": [0] },
                { "width": "100px", "targets": [1] },
                { "width": "90px", "targets": [2] },
            ],
            "language": {
                "emptyTable": "表示するデータがありません。",
            }
        });

        setTimeout(function (){
            disconnectTable.columns.adjust();
        }, 100);
    }
});

/**
 * 編集ボタン押下処理
 */
function onEditJob() {
    // 画面遷移
    let action = '/top/job-edit';
    $('#frmJobDetail').attr('action', action).submit();
}

/**
 * 強制終了ボタン押下処理
 */
function onTerminationJob() {
    const INF_TERMINATION_JOB = 'ジョブを強制終了してもよろしいですか？'
    showModal(INF_TERMINATION_JOB, '強制終了', onExecute);
}

/**
 * 実行処理
 */
function onExecute() {
    let action = "/top/job-detail/execute";
    let formData = $('#frmJobDetail').serialize();

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
        alertError('ジョブ強制終了エラー');
    }).always(function() {
        hideLoading();
    });
}

/**
 * CSVで保存ボタン押下処理
 */
function onOutputCsv() {
    // CSVダウウンロード
    let action = '/top/job-detail/download';
    $('#frmJobDetail').attr('action', action).submit();
}

/**
 * キャンセルボタン押下処理
 * @param {*} obj 
 */
function onCancel(obj) {
    // TOP画面へ遷移
    location.href = '/top/back';
}