/**
 * Created with PyCharm.
 * User: Zhipeng Zhang
 * Date: 14-9-25
 * Time: 下午5:19
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    $(".stripe tr").mouseover(function () {
        $(this).addClass("over");
    }).mouseout(function () {
            $(this).removeClass("over");
        })
    $(".stripe tr:even").addClass("alt");
});
function table_color()
{
    $(".stripe tr").mouseover(function () {
        $(this).addClass("over");
    }).mouseout(function () {
            $(this).removeClass("over");
        })
    $(".stripe tr:even").addClass("alt");

}
