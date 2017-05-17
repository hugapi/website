// The main client-side logic for the hug website
var first_tab = null;


function nav_clicked(event) {
    var view = $(event.target)[0].id;
    change_view(view, true);
}

function change_view(view, update_history) {
    if (update_history) {
        window.history.pushState({'tab': view}, view, '/website/' + view);
    }
    $('#main_content').load('/' + view, function on_load() {

;
    })
    $('header').find('a').removeClass('selected');
    $('#' + view).addClass('selected');
}

function navigate_history(event, date) {
    if (!event.originalEvent.state) {
        return change_view(first_tab);
    }
    change_view(event.originalEvent.state['tab']);
}



function main() {
    first_tab = $('header').find('.selected')[0].id;
    $('nav').find('a').click(nav_clicked);
    $(window).bind('popstate', navigate_history);
}

$(document).ready(main);
