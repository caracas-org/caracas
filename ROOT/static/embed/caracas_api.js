
// needs jquery

var CARACAS_BASE_URL = 'http://caracas.gladis.org/';
var show_popup;

(function() {

    _show_popup = function(name, icon_url, xp_gained) {

        popup = $('<div id="caracas-achievement-popup" style="font-size: 200%; height: 3em; width: 12em;' +
            'position: absolute; bottom: 0em; right: 0;' +
            'margin: 0; padding: 0; overflow: hidden;' +
            '"><div style="background-color: black; height: 3em; width: 12em; position: absolute; right: 0; bottom: -3em;">' +
            '<img src="' + icon_url + '" style="height: 3em; width: 3em;" >' +
            '<div style="color: white; position: absolute; left: 3.5em; top: 0.3em; width: 9em; height: 1.2em; margin: 0; padding: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">' +
            '' + name + '</div>' +
            '<div style="color: white; position: absolute; left: 3.5em; top: 1.6em; width: 9em; height: 1.2em; margin: 0; padding: 0; overflow: hidden;">' +
            '<div style="float: right; font-size: 75%; margin-right: 1em;"><a style="color: white;" href="' + CARACAS_BASE_URL +
            '">Show now &gt;&gt;&gt;</a></div>' +
            '<div style="font-size: 75%;">' + xp_gained + ' XP</div>' +
            '</div></div>');

        console.log();
        $('body').append(popup);
        var el = $('div#caracas-achievement-popup > div');
        el.animate(
            {'bottom': 0}, 1000, 'swing', function() {
                setTimeout(function() {
                    el.animate({'bottom': '-3em'}, 1000, 'swing', function() {
                        el.remove();
                    })
                }, 2000);
            }
        );
    };

    /**
     * Mark progress made on an achievement.
     *
     * You will receive information about the achievement and its progress for this user.
     *
     * An example: the achievement is to host 10 guests. The user has just hosted his/her 7th guest. You would then call
     * ``achievement_progress('your_id', 'user_id', 8, 'your auth token');``
     * If the progress leads to the user fulfilling 25%, 50% or 75% of the achievement, a notice will pop up in the
     * lower right corner. If the progress leads to fulfilling the achievement, a notice about this fact will pop up in
     * the lower right corner.
     *
     * The given callback will be called as soon as the API request was finished, so the popup will usually still be
     * active at the time.
     *
     * @param achievement_id The achievement ID the user just progressed on.
     * @param user_id        The ID of the user that just fulfilled the achievement.
     * @param progress       The number of "progress" made on this achievement. The meaning of progress depends on the
     *                       specific achievement.
     * @param auth_token     Your API auth token.
     * @param callback       A function that will be called with achievement information when the request has finished.
     *                       Will receive an object that contains information about the achievement progress.
     */
    var achievement_progress = function(achievement_id, user_id, progress, auth_token, callback) {

    };

    /**
     * Mark an achievement fulfilled.
     *
     * The given callback will be called as soon as the API request was finished, so the popup will usually still be
     * active at the time.
     *
     * @param achievement_id The achievement ID that the user just fulfilled.
     * @param user_id        The user ID for the current user.
     * @param auth_token     Your auth token
     * @param callback       A function that will be called with achievement information when the request has finished.
     *                       Will receive an object that contains information about the achievement progress.
     * @param callback_err   A callback that will get the status and error message in case the request failed.
     */
    var achievement_unlocked = function(achievement_id, user_id, auth_token, callback, callback_err) {

        callback = callback || function() {};
        callback_err = callback_err || function() {};

        $.ajax(CARACAS_BASE_URL + 'a/api/unlock/', {
            method: 'POST',
            data: {
                achievement_id: achievement_id,
                user_id: user_id,
                auth_token: auth_token,
                fulfilled: true
            },
            success: function(data) {
                console.log('data');
                console.log(data);

                _show_popup(data.achievement_name, data.achievement_image, data.xp_gained);

                callback(data);
            },
            error: function(xhr, textStatus, error) {
                callback_err(textStatus, error);
            }
        });

        return;
    };

    /**
     * Find the user ID for a given username (or undefined if no user exists).
     * @param username The user name you want to search for.
     * @param callback Your function to be called with user_id or undefined after the request finishes.
     */
    var find_user_id = function(username, callback) {

    };

    $.achievement_unlocked = achievement_unlocked;

    show_popup = _show_popup;

}());
