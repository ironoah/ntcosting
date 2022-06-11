/**
 * 設定確認画面
 */
function confirmMode() {
    // ボタンセットを切り替える
    $('#ButtonSection')
        .find('section')
        .addClass('d-none')
        .filter('#SectionConfirm')
        .removeClass('d-none');

    $('#InputSection')
        .find('section div input')
        .prop('readOnly', true)
        .attr('tabindex', -1)
        .addClass('label-text');
}

/**
 * 設定変更画面
 */
function editMode() {
    // ボタンセットを切り替える
    $('#ButtonSection')
        .find('section')
        .addClass('d-none')
        .filter('#SectionEdit')
        .removeClass('d-none');

    $('#InputSection')
        .find('section div input')
        .prop('readOnly', false)
        .attr('tabindex', 0)
        .removeClass('label-text');
}

/**
 * キャンセルボタン押下処理
 * @param {*} obj 
 */
function onCancel(obj) {
    // TOP画面へ遷移
    location.href = '/top';
}

/**
 * 確認ボタン押下処理(一般設定)
 * @param {*} obj 
 * @returns 
 */
function onConfirmGeneral(obj) {
    const ERR_REQUIRED_JOB_PAGE = '1ページ表示数(TOP画面)が未入力です。';
    const ERR_REQUIRED_TIMEOUT = '情報取得タイムアウト(秒)が未入力です。';
    const ERR_REQUIRED_MACFLAP = 'MACFLAP数取得基準時間(分)が未入力です。';
    const ERR_REQUIRED_BROAD_CAST = 'ブロードキャスト数取得基準時間(分)が未入力です。';
    const ERR_REQUIRED_BCAST_TIME = '使用BCAST時間初期値(現時刻-N分)が未入力です。';
    const ERR_REQUIRED_JOB_TITLE = 'ジョブタイトル初期値が未入力です。';
    const ERR_REQUIRED_AUTO_JOB_TITLE = 'ジョブタイトル(自動実行)が未入力です。';
    const ERR_REQUIRED_LOG_LVL = '出力ログレベルが未選択です。';
    const ERR_REQUIRED_STOCK_TERM = '保存期間(日)が未入力です。';
    const ERR_REQUIRED_LOG_PAGE = '1ページ表示数(ログ画面)が未入力です。';
    const ERR_REQUIRED_BRUTE_FORCE = 'ブルートフォースアタック検知ログ閾値が未入力です。';
    const ERR_REQUIRED_REGULAR_JOB_TITLE = 'ジョブタイトル(定期実行)が未入力です。';
    const ERR_REQUIRED_REGULAR_TERM = '定期実行間隔(日)が未入力です。';
    const ERR_REQUIRED_REGULAR_TIME = '定期実行時間に有効な値が入力されていません。';
    const ERR_REQUIRED_PASSWORD_MOD_TERM = 'パスワード変更期間(日)が未入力です。';
    const ERR_REQUIRED_FROM_MAIL_ADDRESS = '送信元メールアドレスが未入力です。';
    const ERR_REQUIRED_TO_MAIL_ADDRESS = '送信先メールアドレスが未入力です。';

    $validation = $('input').filter(function() {
        return $(this).data("validation") == true;
    });
    // エラーが存在する場合は処理を中止
    if ($validation.length != 0) {
        return false;
    }

    // エラー背景色を通常色へ戻す
    $("input").removeClass("validation-error");
    $("select").removeClass("validation-error");

    // 入力値取得
    let jobLinesPage = $('#jobLinesPage').val();
    let dataGetTimeout = $('#dataGetTimeout').val();
    let macflapGetTime = $('#macflapGetTime').val();
    let broadcastGetTime = $('#broadcastGetTime').val();
    let defaultBcastTime = $('#defaultBcastTime').val();
    let defaultJobTitle = $('#defaultJobTitle').val();
    let autoJobTitle = $('#autoJobTitle').val();
    let outputLogLvl = $('#outputLogLvl').val();
    let stockTerm = $('#stockTerm').val();
    let logLinesPage = $('#logLinesPage').val();
    let loginFailCount = $('#loginFailCount').val();
    let regularJobTitle = $('#regularJobTitle').val();
    let regularExecuteCycle = $('#regularExecuteCycle').val();
    let regularExecuteTime = $('#regularExecuteTime').val();
    let passwordModTerm = $('#passwordModTerm').val();
    let fromMailAddress = $('#fromMailAddress').val();
    let toMailAddress = $('#toMailAddress').val();

    // 1ページ表示数(TOP)
    if (!jobLinesPage) {
        $("#jobLinesPage").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_JOB_PAGE);
        return false;
    }
    // 情報取得タイムアウト(秒)
    if (!dataGetTimeout) {
        $("#dataGetTimeout").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TIMEOUT);
        return false;
    }
    // 使用BCAST時間初期値(現時刻-N分)
    if (!defaultBcastTime) {
        $("#defaultBcastTime").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_BCAST_TIME);
        return false;
    }
    // MACFLAP数取得基準時間(分)
    if (!macflapGetTime) {
        $("#macflapGetTime").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_MACFLAP);
        return false;
    }
    // ブロードキャスト数取得基準時間(分)
    if (!broadcastGetTime) {
        $("#broadcastGetTime").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_BROAD_CAST);
        return false;
    }
    // ジョブタイトル初期値
    if (!defaultJobTitle) {
        $("#defaultJobTitle").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_JOB_TITLE);
        return false;
    }
    // ジョブタイトル(自動実行)
    if (!autoJobTitle) {
        $("#autoJobTitle").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_AUTO_JOB_TITLE);
        return false;
    }
    // 出力ログレベル
    if (!outputLogLvl || outputLogLvl == "000") {
        $("#outputLogLvl").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_LOG_LVL);
        return false;
    }
    // 保存期間(日)
    if (!stockTerm) {
        $("#stockTerm").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_STOCK_TERM);
        return false;
    }
    // 1ページ表示数(ログ)
    if (!logLinesPage) {
        $("#logLinesPage").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_LOG_PAGE);
        return false;
    }
    // ブルートフォースアタック検知ログ閾値
    if (!loginFailCount) {
        $("#loginFailCount").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_BRUTE_FORCE);
        return false;
    }
    // ジョブタイトル(定期実行)
    if (!regularJobTitle) {
        $("#regularJobTitle").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_REGULAR_JOB_TITLE);
        return false;
    }
    // 定期実行間隔(日)
    if (!regularExecuteCycle) {
        $("#regularExecuteCycle").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_REGULAR_TERM);
        return false;
    }
    // 定期実行時間
    if (!regularExecuteTime) {
        $("#regularExecuteTime").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_REGULAR_TIME);
        return false;
    }
    // パスワード変更期間(日)
    if (!passwordModTerm) {
        $("#passwordModTerm").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_PASSWORD_MOD_TERM);
        return false;
    }
    // 送信元メールアドレス
    if (!fromMailAddress) {
        $("#fromMailAddress").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_FROM_MAIL_ADDRESS);
        return false;
    }
    // 送信先メールアドレス
    if (!toMailAddress) {
        $("#toMailAddress").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_TO_MAIL_ADDRESS);
        return false;
    }

    // select → label
    changeSelectTag(true);

    // 設定確認モードへ
    confirmMode();
}

/**
 * 変更ボタン押下処理(一般設定)
 * @param {*} obj 
 */
function onChangeGeneral(obj) {
    let action = "/top/setting/general/update";
    let formData = $('#frmSettingGeneral').serialize();

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
        alertError('一般設定更新エラー');
    }).always(function() {
        hideLoading();
    });
}

/**
 * 編集画面へ戻るボタン押下処理(一般設定)
 * @param {*} obj 
 */
function onEditGeneral(obj) {
    try {
        showLoading();
        // label → select
        changeSelectTag(false);
        // 編集画面
        editMode();
    }
    catch(e) {
    }
    finally {
        hideLoading();
    }
}

/**
 * 確認ボタン押下処理(アカウント)
 * @param {*} obj 
 */
function onConfirmAccount(obj) {
    const ERR_REQUIRED_USER = 'ユーザ名が未入力です。';
    const ERR_REQUIRED_PASSWORD = 'パスワードが未入力です。';
    const ERR_REQUIRED_RECONF_PASSWORD = 'パスワード(再入力)が未入力です。';
    const ERR_MISMATCH_PASSWORD = 'パスワードとパスワード(再入力)が一致しません。';

    $validation = $('input').filter(function() {
        return $(this).data("validation") == true;
    });
    // エラーが存在する場合は処理を中止
    if ($validation.length != 0) {
        return false;
    }

    // エラー背景色を通常色へ戻す
    $("input").removeClass("validation-error");
    alertClose();

    // 入力値取得
    let user = $('#user').val();
    let password = $('#password').val();
    let reconfPassword = $('#reconfPassword').val();

    // ユーザ
    if (!user) {
        $("#user").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_USER);
        return false;
    }
    // パスワード
    if (!password) {
        $("#password").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_PASSWORD);
        return false;
    }
    // パスワード(再入力)
    if (!reconfPassword) {
        $("#reconfPassword").addClass("validation-error").focus();
        alertError(ERR_REQUIRED_RECONF_PASSWORD);
        return false;
    }
    // パスワード同値チェック
    if (password != reconfPassword) {
        $("#password").addClass("validation-error").focus();
        $("#reconfPassword").addClass("validation-error");
        alertError(ERR_MISMATCH_PASSWORD);
        return false;
    }

    // 設定確認モードへ
    confirmMode();
}

/**
 * 変更ボタン押下処理(アカウント)
 * @param {*} obj 
 */
function onChangeAccount(obj) {
    let action = "/top/setting/account/update";
    let formData = $('#frmSettingAccount').serialize();

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
        alertError('アカウント設定更新エラー');
    }).always(function() {
        hideLoading();
    });
}

/**
 * 編集画面へ戻るボタン押下処理(アカウント)
 * @param {*} obj 
 */
function onEditAccount(obj) {
    try {
        showLoading();
        // 編集画面
        editMode();
    }
    catch(e) {
    }
    finally {
        hideLoading();
    }
}

/**
 * 設定情報出力ボタン押下処理
 * @param {*} obj 
 */
function onOutputSetting(obj) {
    // CSV出力
    let action = '/top/setting/general/download';
    $('#frmSettingGeneral').attr('action', action).submit();
}

/**
 * デフォルトボタン押下処理
 * @param {*} obj 
 */
function onDefaultSetting(obj) {
    // メッセージ非表示
    alertClose();

    $.ajax({
        type: 'GET',
        url: '/top/setting/general/default',
        beforeSend: function(){
            showLoading();
        },
    }).done(function(res) {
        if (res.result == '0') {
            // 0:正常終了
            defaultValueSetting(res.setting);
        } else {
            // 9:異常終了
            location.href = res.route;
        }
    }).fail(function(e) {
        alertError('設定ファイル情報取得エラー');
    }).always(function() {
        hideLoading();
    });
}

/**
 * デフォルト値設定処理
 * @param {*} obj 
 */
function defaultValueSetting(obj) {
    // 既定値設定
    $('#jobLinesPage').val(obj.job_lines_page);
    $('#dataGetTimeout').val(obj.data_get_timeout);
    $('#defaultBcastTime').val(obj.default_bcast_time);
    $('#macflapGetTime').val(obj.macflap_get_time);
    $('#broadcastGetTime').val(obj.broadcast_get_time);
    $('#defaultJobTitle').val(obj.default_job_title);
    $('#autoJobTitle').val(obj.auto_job_title);
    $('#outputLogLvl').val(obj.output_log_lvl_cd);
    $('#stockTerm').val(obj.stock_term);
    $('#logLinesPage').val(obj.log_lines_page);
    $('#loginFailCount').val(obj.login_fail_count);
    $('#regularJobTitle').val(obj.regular_job_title);
    $('#regularExecuteCycle').val(obj.regular_execute_cycle);
    $('#regularExecuteTime').val(obj.regular_execute_time);
    $('#passwordModTerm').val(obj.password_mod_term);
}

/**
 * タグ表示入替処理(select)
 * @param {*} flap true:ON, false:OFF
 */
function changeSelectTag(flap) {
    if (flap) {
        // select ⇒ label
        // 出力ログレベル
        let outputLogText = $('#outputLogLvl option:selected').text();
        $('#outputLogLvl').addClass("d-none");
        $('#labelOutputLogLvl').removeClass("d-none").text(outputLogText);
    }
    else {
        // label ⇒ select
        // 出力ログレベル
        $('#outputLogLvl').removeClass("d-none");
        $('#labelOutputLogLvl').addClass("d-none");
    }
}

/**
 * 1ページ表示数(ログ)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurJobLinesPage(obj) {
    const ERR_NOT_NUMERIC = '1ページ表示数(TOP)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '1ページ表示数(TOP)は、500まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '1ページ表示数(TOP)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (500 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 情報取得タイムアウト(秒)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurDataTimeout(obj) {
    const ERR_NOT_NUMERIC = '情報取得タイムアウト(秒)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '情報取得タイムアウト(秒)は、60まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '情報取得タイムアウト(秒)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (60 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * MACFLAP数取得基準時間(分)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurMacflapTime(obj) {
    const ERR_NOT_NUMERIC = 'MACFLAP数取得基準時間(分)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = 'MACFLAP数取得基準時間(分)は、1440まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = 'MACFLAP数取得基準時間(分)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (1440 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * ブロードキャスト数取得基準時間(分)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurBroadcastTime(obj) {
    const ERR_NOT_NUMERIC = 'ブロードキャスト数取得基準時間(分)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = 'ブロードキャスト数取得基準時間(分)は、1440まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = 'ブロードキャスト数取得基準時間(分)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (1440 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 使用BCAST時間初期値(分)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurBcastTime(obj) {
    const ERR_NOT_NUMERIC = '使用BCAST時間初期値(分)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '使用BCAST時間初期値(分)は、10080まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '使用BCAST時間初期値(分)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (10080 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 保存期間(日)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurStockTerm(obj) {
    const ERR_NOT_NUMERIC = '保存期間(日)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '保存期間(日)は、9999まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '保存期間(日)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (10000 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 1ページ表示数(ログ)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurLogLinesPage(obj) {
    const ERR_NOT_NUMERIC = '1ページ表示数(ログ)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '1ページ表示数(TOP)は、500まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '1ページ表示数(TOP)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (500 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * ブルートフォースアタック検知ログ閾値フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurLoginFailCount(obj) {
    const ERR_NOT_NUMERIC = 'ブルートフォースアタック検知ログ閾値は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = 'ブルートフォースアタック検知ログ閾値は、9999まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = 'ブルートフォースアタック検知ログ閾値は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (10000 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 定期実行間隔(日)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurExecuteCycle(obj) {
    const ERR_NOT_NUMERIC = '定期実行間隔(日)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = '定期実行間隔(日)は、9999まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = '定期実行間隔(日)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (10000 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * パスワード変更期間(日)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurPasswordModTerm(obj) {
    const ERR_NOT_NUMERIC = 'パスワード変更期間(日)は、数値のみ入力可能です。';
    const ERR_MAX_VALUE_OVER = 'パスワード変更期間(日)は、9999まで入力可能でです。';
    const ERR_MIN_VALUE_UNDER = 'パスワード変更期間(日)は、1以上が入力可能です。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 数値チェック
    if (!value.match(/^([1-9]\d*|0)$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_NUMERIC);
        return false;
    }
    // 最大値チェック
    if (10000 < value) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAX_VALUE_OVER);
        return false;
    }
    // 最小値チェック
    if (value < 1) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MIN_VALUE_UNDER);
        return false;
    }
}

/**
 * 送信元メールアドレスフォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurFromMailAddress(obj) {
    const ERR_MAIL_FORMAT = '送信元メールアドレスのメールアドレスが正しい形式ではありません。';
    const REGEX = /^([a-zA-Z0-9])+([a-zA-Z0-9._-])*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/;
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 正規表現チェック
    if (!REGEX.test(value)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAIL_FORMAT);
        return false;
    }
}

/**
 * 送信先メールアドレスフォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurToMailAddress(obj) {
    const ERR_MAIL_FORMAT = '送信先メールアドレスのメールアドレスが正しい形式ではありません。';
    const REGEX = /^([a-zA-Z0-9])+([a-zA-Z0-9._-])*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/;
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 正規表現チェック
    if (!REGEX.test(value)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_MAIL_FORMAT);
        return false;
    }
}

/**
 * ユーザ名フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurUser(obj) {
    const ERR_INPUT_DIGITS = 'ユーザ名は、6桁から10桁の文字数を入力してください。';
    const ERR_NOT_ALPHANUMERIC = 'ユーザ名へ半角英数字以外が入力されています。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 桁数チェック
    if (!((6 <= value.length) && (value.length <= 10 ))) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_INPUT_DIGITS);
        return false;
    }
    // 半角英数字チェック
    if (!value.match(/^[a-zA-Z0-9]+$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_ALPHANUMERIC);
        return false;
    }
}

/**
 * パスワードフォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurPassword(obj) {
    const ERR_INPUT_DIGITS = 'パスワードは、6桁から10桁の文字数を入力してください。';
    const ERR_NOT_ALPHANUMERIC = 'パスワードへ半角英数字以外が入力されています。';
    const ERR_NOT_INCLUDE = 'パスワードは、英字と数字をどちらも含めてください。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 桁数チェック
    if (!((6 <= value.length) && (value.length <= 10 ))) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_INPUT_DIGITS);
        return false;
    }
    // 半角英数字チェック
    if (!value.match(/^[a-zA-Z0-9]+$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_ALPHANUMERIC);
        return false;
    }
    // 半角英数字包含チェック
    if (!value.match(/^(?=.*?[a-zA-Z])(?=.*?[0-9])[a-zA-Z0-9]{6,10}$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_INCLUDE);
        return false;
    }
}

/**
 * パスワード(再入力)フォーカスアウトイベント
 * @param {*} obj 
 * @returns 
 */
function onBlurRePassword(obj) {
    const ERR_INPUT_DIGITS = 'パスワード(再入力)は、6桁から10桁の文字数を入力してください。';
    const ERR_NOT_ALPHANUMERIC = 'パスワード(再入力)へ半角英数字以外が入力されています。';
    const ERR_NOT_INCLUDE = 'パスワード(再入力)は、英字と数字をどちらも含めてください。';
    const value = $(obj).val();

    // エラー背景色を通常色へ戻す
    $(obj).removeClass("validation-error").data("validation",false);
    alertClose();

    // 空白の場合、スキップ
    if (!value) return;

    // 桁数チェック
    if (!((6 <= value.length) && (value.length <= 10 ))) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_INPUT_DIGITS);
        return false;
    }
    // 半角英数字チェック
    if (!value.match(/^[a-zA-Z0-9]+$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_ALPHANUMERIC);
        return false;
    }
    // 半角英数字包含チェック
    if (!value.match(/^(?=.*?[a-zA-Z])(?=.*?[0-9])[a-zA-Z0-9]{6,10}$/)) {
        $(obj).addClass("validation-error").data("validation",true).select();
        alertError(ERR_NOT_INCLUDE);
        return false;
    }
}