var AcademicCard = {
    name: 'AcademicCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(AcademicCard.render_upon_data, AcademicCard.show_error);
    },

    render_upon_data: function() {
        if (!AcademicCard._has_all_data()) {
            return;
        }
        AcademicCard._render(WSData.profile_data());
    },

    _render: function (academic_data) {
        var source = $("#academic_card_content").html();
        var template = Handlebars.compile(source);
        AcademicCard.dom_target.html(template(academic_data));
        AcademicCard.add_events();
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    add_events: function() {
        $("#toggle_academic_card_resources").on("click", function(ev) {
            ev.preventDefault();
            $("#academic_card_resources").toggleClass("slide-show");

            if ($("#academic_card_resources").hasClass("slide-show")) {
                $("#toggle_academic_card_resources").text("SHOW LESS");
                $("#toggle_academic_card_resources").attr("title", "Hide additional academics resources");
                $("#academic_card_resources").attr("aria-hidden", "false");
                WSData.log_interaction("show_academic_card_resources");
            }
            else {
                $("#toggle_academic_card_resources").text("SHOW MORE");
                $("#toggle_academic_card_resources").attr("title", "Expand to show additional academics resources");
                $("#academic_card_resources").attr("aria-hidden", "true");

                setTimeout(function() {
                    $("#toggle_academic_card_resources").text("SHOW MORE");
                }, 700);
            }
        });
    },

    show_error: function() {
        // don't show card if no account
        AcademicCard.dom_target.html('');
    }

    
};
